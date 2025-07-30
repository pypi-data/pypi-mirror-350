import ctypes
import os
import io
from .native_base import _NativeBase

class _StreamAdapter:
    def __init__(self, py_stream):
        self.stream = py_stream  # Stream initialization

    def get_length(self, handle):
        # Get length of stream in bytes
        try:
            iPos = self.stream.tell()
            self.stream.seek(0, os.SEEK_END)
            nLen = self.stream.tell()
            self.stream.seek(iPos, os.SEEK_SET)
            return nLen
        except OSError:
            return -1

    def seek(self, handle, iPos):
        # Set position
        try:
            if iPos == -1:
                self.stream.seek(0, os.SEEK_END)
            else :
                self.stream.seek(iPos, os.SEEK_SET)
            return 1
        except (OSError, ValueError):
            return 0

    def tell(self, handle):
        # Get current byte position
        try:
            return self.stream.tell()
        except OSError:
            return -1

    def read(self, handle, pData, nSize):
        # Read nSize bytes from stream
        try:
            data = self.stream.read(nSize)
            length = len(data)
            ctypes.memmove(pData, data, length)
            return length  # Return number of bytes read
        except (OSError, ValueError) as e:
            return -1

    def write(self, handle, pData, nSize):
        # Write nSize bytes to stream
        try:
            data = (ctypes.c_char * nSize).from_address(pData)
            written = self.stream.write(data)
            if written != nSize:
                return -1
            return written  # Return number of bytes written
        except (OSError, ValueError):
            return -1

    def release(self, handle):
        return # i.e. close stream explicitly using the "with statement"

# Define the _StreamDescriptor struct
class _StreamDescriptor(ctypes.Structure):
    _fields_ = [("pfGetLength", ctypes.CFUNCTYPE(ctypes.c_longlong, ctypes.c_void_p)),
                ("pfSeek", ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_longlong)),
                ("pfTell", ctypes.CFUNCTYPE(ctypes.c_longlong, ctypes.c_void_p)),
                ("pfRead", ctypes.CFUNCTYPE(ctypes.c_size_t, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)),
                ("pfWrite", ctypes.CFUNCTYPE(ctypes.c_size_t, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)),
                ("pfRelease", ctypes.CFUNCTYPE(None, ctypes.c_void_p)),
                ("m_handle", ctypes.c_void_p)]

    def __init__(self, py_stream = None):
        if py_stream is not None:
            adapter = _StreamAdapter(py_stream)
            py_stream.descriptor = self
            super().__init__(
                pfGetLength=ctypes.CFUNCTYPE(ctypes.c_longlong, ctypes.c_void_p)(adapter.get_length),
                pfSeek=ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_longlong)(adapter.seek),
                pfTell=ctypes.CFUNCTYPE(ctypes.c_longlong, ctypes.c_void_p)(adapter.tell),
                pfRead=ctypes.CFUNCTYPE(ctypes.c_size_t, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)(adapter.read),
                pfWrite=ctypes.CFUNCTYPE(ctypes.c_size_t, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)(adapter.write),
                pfRelease=ctypes.CFUNCTYPE(None, ctypes.c_void_p)(adapter.release),
                m_handle=ctypes.cast(ctypes.pointer(ctypes.py_object(adapter)), ctypes.c_void_p)
            )
        else:
            super().__init__(
                pfGetLength=ctypes.CFUNCTYPE(ctypes.c_longlong, ctypes.c_void_p)(),
                pfSeek=ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_longlong)(),
                pfTell=ctypes.CFUNCTYPE(ctypes.c_longlong, ctypes.c_void_p)(),
                pfRead=ctypes.CFUNCTYPE(ctypes.c_size_t, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)(),
                pfWrite=ctypes.CFUNCTYPE(ctypes.c_size_t, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)(),
                pfRelease=ctypes.CFUNCTYPE(None, ctypes.c_void_p)(),
                m_handle=None,
            )

# Stream class type when returning a stream from C as property getter or as method return
class _NativeStream(io.IOBase):
    def __init__(self, stream_descriptor):
        """
        Wrap a C `StreamDescriptor` into a Python stream.
        :param stream_descriptor: A StreamDescriptor instance
        """
        if not isinstance(stream_descriptor, _StreamDescriptor):
            raise TypeError("stream_descriptor must be an instance of _StreamDescriptor")

        self._stream_desc = stream_descriptor
        self._disposed = False

    def _check_disposed(self):
        if self._disposed:
            raise ValueError("I/O operation on a closed file.")

    def read(self, size=-1):
        """
        Read up to `size` bytes from the stream.
        """
        self._check_disposed()

        if size < 0:
            # Read the remaining bytes by seeking to the end and subtracting the position
            current_pos = self.tell()
            self.seek(0, io.SEEK_END)
            size = self.tell() - current_pos
            self.seek(current_pos, io.SEEK_SET)

        buffer = (ctypes.c_char * size)()
        bytes_read = self._stream_desc.pfRead(self._stream_desc.m_handle, ctypes.byref(buffer), size)

        if bytes_read == -1:
            _NativeBase._throw_last_error(False)

        return bytes(buffer[:bytes_read])

    def write(self, b):
        """
        Write the given bytes to the stream.
        """
        self._check_disposed()

        if not isinstance(b, (bytes, bytearray)):
            raise TypeError("a bytes-like object is required, not '{}'".format(type(b).__name__))

        size = len(b)
        buffer = (ctypes.c_char * size).from_buffer_copy(b)
        bytes_written = self._stream_desc.pfWrite(self._stream_desc.m_handle, ctypes.byref(buffer), size)

        if bytes_written == -1 or bytes_written == 0:
            _NativeBase._throw_last_error(False)

        return bytes_written

    def seek(self, offset, whence=io.SEEK_SET):
        """
        Seek to a specific position in the stream.
        """
        self._check_disposed()

        # Determine the new seek position based on 'whence'
        if whence == io.SEEK_SET:
            seek_position = offset
        elif whence == io.SEEK_CUR:
            seek_position = offset + self.tell()
        elif whence == io.SEEK_END:
            seek_position = offset + self.length()
        else:
            raise ValueError("Invalid 'whence' value. Must be SEEK_SET, SEEK_CUR, or SEEK_END.")

        # Perform the seek operation
        result = self._stream_desc.pfSeek(self._stream_desc.m_handle, seek_position)
        if result == 0:
            _NativeBase._throw_last_error(False)

        return self.tell()

    def tell(self):
        """
        Get the current stream position.
        """
        self._check_disposed()

        position = self._stream_desc.pfTell(self._stream_desc.m_handle)
        if position == -1:
            _NativeBase._throw_last_error(False)

        return position

    def close(self):
        """
        Release the stream.
        """
        if not self._disposed:
            self._stream_desc.pfRelease(self._stream_desc.m_handle)
            self._disposed = True

    def __del__(self):
        if not self._disposed:
            self.close()

    def readable(self):
        """
        Return True if the stream supports reading.
        """
        return self._stream_desc.pfRead is not None

    def writable(self):
        """
        Return True if the stream supports writing.
        """
        return self._stream_desc.pfWrite is not None

    def seekable(self):
        """
        Return True if the stream supports seeking.
        """
        return self._stream_desc.pfSeek is not None and self._stream_desc.pfGetLength(self._stream_desc.m_handle) != -1

    def flush(self):
        """
        Flush the stream. Not supported in this implementation.
        """
        raise NotImplementedError("Flush is not implemented for this stream.")

    def length(self):
        """
        Get the length of the stream.
        """
        self._check_disposed()

        length = self._stream_desc.pfGetLength(self._stream_desc.m_handle)
        if length == -1:
            _NativeBase._throw_last_error(False)

        return length
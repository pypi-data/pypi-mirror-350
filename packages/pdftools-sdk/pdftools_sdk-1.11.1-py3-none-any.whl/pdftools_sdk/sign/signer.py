from __future__ import annotations
import io
from typing import List, Iterator, Tuple, Optional, Any, TYPE_CHECKING, Callable
from ctypes import *
from datetime import datetime
from numbers import Number
from pdftools_sdk.internal import _lib
from pdftools_sdk.internal.utils import _string_to_utf16, _utf16_to_string
from pdftools_sdk.internal.streams import _StreamDescriptor, _NativeStream
from pdftools_sdk.internal.native_base import _NativeBase
from pdftools_sdk.internal.native_object import _NativeObject

import pdftools_sdk.internal

if TYPE_CHECKING:
    from pdftools_sdk.pdf.document import Document
    from pdftools_sdk.sign.signature_configuration import SignatureConfiguration
    from pdftools_sdk.sign.output_options import OutputOptions
    from pdftools_sdk.sign.mdp_permission_options import MdpPermissionOptions
    from pdftools_sdk.sign.timestamp_configuration import TimestampConfiguration
    from pdftools_sdk.sign.signature_field_options import SignatureFieldOptions
    from pdftools_sdk.sign.prepared_document import PreparedDocument
    from pdftools_sdk.crypto.providers.provider import Provider
    from pdftools_sdk.sign.warning_category import WarningCategory

else:
    Document = "pdftools_sdk.pdf.document.Document"
    SignatureConfiguration = "pdftools_sdk.sign.signature_configuration.SignatureConfiguration"
    OutputOptions = "pdftools_sdk.sign.output_options.OutputOptions"
    MdpPermissionOptions = "pdftools_sdk.sign.mdp_permission_options.MdpPermissionOptions"
    TimestampConfiguration = "pdftools_sdk.sign.timestamp_configuration.TimestampConfiguration"
    SignatureFieldOptions = "pdftools_sdk.sign.signature_field_options.SignatureFieldOptions"
    PreparedDocument = "pdftools_sdk.sign.prepared_document.PreparedDocument"
    Provider = "pdftools_sdk.crypto.providers.provider.Provider"
    WarningCategory = "pdftools_sdk.sign.warning_category.WarningCategory"


if not TYPE_CHECKING:
    WarningCategory = "WarningCategory"

WarningFunc = Callable[[str, WarningCategory, str], None]
"""
Event for non-critical errors occurring during signature processing



Args:
    message (str): 
        The message describing the warning

    category (pdftools_sdk.sign.warning_category.WarningCategory): 
        The category of the warning

    context (str): 
        A description of the context where the warning occurred


"""

class Signer(_NativeObject):
    """
    Process signatures and signature fields


    """
    # Event definition
    _WarningFunc = CFUNCTYPE(None, c_void_p, c_wchar_p, c_int, c_wchar_p)
    def _wrap_warning_func(self, py_callback: WarningFunc) -> Signer._WarningFunc:

        def _c_callback(event_context, message, category, context):
            from pdftools_sdk.sign.warning_category import WarningCategory

            # Call the Python callback
            py_callback(_utf16_to_string(message), WarningCategory(category), _utf16_to_string(context))

        # Wrap the callback in CFUNCTYPE so it becomes a valid C function pointer
        return Signer._WarningFunc(_c_callback)


    def __init__(self):
        """


        """
        _lib.PdfToolsSign_Signer_New.argtypes = []
        _lib.PdfToolsSign_Signer_New.restype = c_void_p
        ret_val = _lib.PdfToolsSign_Signer_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)
        self._warning_callback_map = {}


    def sign(self, document: Document, configuration: SignatureConfiguration, stream: io.IOBase, output_options: Optional[OutputOptions] = None) -> Document:
        """
        Add a document signature

         
        Document signatures are sometimes also called approval signatures.
        This type of signature lets you verify the integrity of the signed part of the document and authenticate the signer’s identity.
         
        The features and format of the signature are defined by the :class:`pdftools_sdk.crypto.providers.provider.Provider`  and the `configuration`.
         
        Non-critical processing errors raise a :func:`pdftools_sdk.sign.signer.WarningFunc` .
        It is recommended to review the :class:`pdftools_sdk.sign.warning_category.WarningCategory`  and handle them if necessary for the application.



        Args:
            document (pdftools_sdk.pdf.document.Document): 
                The input document to sign

            configuration (pdftools_sdk.sign.signature_configuration.SignatureConfiguration): 
                The signature configuration

            stream (io.IOBase): 
                The stream where the signed document is written

            outputOptions (Optional[pdftools_sdk.sign.output_options.OutputOptions]): 
                Document-level output options not directly related to the signature



        Returns:
            pdftools_sdk.pdf.document.Document: 
                The signed document



        Raises:
            pdftools_sdk.license_error.LicenseError:
                The license check has failed.

            OSError:
                Writing to the `stream` failed.

            pdftools_sdk.unsupported_feature_error.UnsupportedFeatureError:
                The input PDF contains unrendered XFA form fields.
                See :attr:`pdftools_sdk.pdf.document.Document.xfa`  for more information on how to detect and handle XFA documents.

            ValueError:
                If the `configuration` is invalid, e.g. because the creating provider has been closed.

            ValueError:
                If the `configuration` is invalid, e.g. because it has been revoked.

            pdftools_sdk.not_found_error.NotFoundError:
                If the :attr:`pdftools_sdk.sign.signature_configuration.SignatureConfiguration.field_name`  does not exist in `document`.

            pdftools_sdk.not_found_error.NotFoundError:
                If an image, a PDF or a font file for the visual appearance could not be found.

            pdftools_sdk.retry_error.RetryError:
                If an unexpected error occurs that can be resolved by retrying the operation.
                For example, if a signature service returns an unexpectedly large signature.

            pdftools_sdk.retry_error.RetryError:
                If a resource required by the cryptographic provider is temporarily unavailable.

            pdftools_sdk.http_error.HttpError:
                If a network error occurs, e.g. downloading revocation information (OCSP, CRL) or a time-stamp.

            pdftools_sdk.unsupported_feature_error.UnsupportedFeatureError:
                If the cryptographic provider does not support the requested signing algorithm.

            pdftools_sdk.permission_error.PermissionError:
                If the cryptographic provider does not allow the signing operation.


        """
        from pdftools_sdk.pdf.document import Document
        from pdftools_sdk.sign.signature_configuration import SignatureConfiguration
        from pdftools_sdk.sign.output_options import OutputOptions

        if not isinstance(document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(document).__name__}.")
        if not isinstance(configuration, SignatureConfiguration):
            raise TypeError(f"Expected type {SignatureConfiguration.__name__}, but got {type(configuration).__name__}.")
        if not isinstance(stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(stream).__name__}.")
        if output_options is not None and not isinstance(output_options, OutputOptions):
            raise TypeError(f"Expected type {OutputOptions.__name__} or None, but got {type(output_options).__name__}.")

        _lib.PdfToolsSign_Signer_Sign.argtypes = [c_void_p, c_void_p, c_void_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor), c_void_p]
        _lib.PdfToolsSign_Signer_Sign.restype = c_void_p
        ret_val = _lib.PdfToolsSign_Signer_Sign(self._handle, document._handle, configuration._handle, _StreamDescriptor(stream), output_options._handle if output_options is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Document._create_dynamic_type(ret_val)


    def certify(self, document: Document, configuration: SignatureConfiguration, stream: io.IOBase, permissions: Optional[MdpPermissionOptions] = None, output_options: Optional[OutputOptions] = None) -> Document:
        """
        Add a document certification signature

         
        This type of signature lets you detect rejected changes specified by the author.
        These signatures are also called Modification Detection and Prevention (MDP) signatures.
        The allowed permissions are defined by `permissions`.
         
        The features and format of the signature are defined by the :class:`pdftools_sdk.crypto.providers.provider.Provider`  and the
        `configuration`.
         
        Non-critical processing errors raise a :func:`pdftools_sdk.sign.signer.WarningFunc` .
        It is recommended to review the :class:`pdftools_sdk.sign.warning_category.WarningCategory`  and handle them if necessary for the application.



        Args:
            document (pdftools_sdk.pdf.document.Document): 
                The input document to certify

            configuration (pdftools_sdk.sign.signature_configuration.SignatureConfiguration): 
                The signature configuration

            stream (io.IOBase): 
                The stream where the certified document is written

            permissions (Optional[pdftools_sdk.sign.mdp_permission_options.MdpPermissionOptions]): 
                The permissions allowed. The default is :attr:`pdftools_sdk.pdf.mdp_permissions.MdpPermissions.NOCHANGES` .

            outputOptions (Optional[pdftools_sdk.sign.output_options.OutputOptions]): 
                Document-level output options not directly related to the document certification



        Returns:
            pdftools_sdk.pdf.document.Document: 


        Raises:
            pdftools_sdk.license_error.LicenseError:
                The license check has failed.

            OSError:
                Writing to the `stream` failed.

            pdftools_sdk.unsupported_feature_error.UnsupportedFeatureError:
                The input PDF contains unrendered XFA form fields.
                See :attr:`pdftools_sdk.pdf.document.Document.xfa`  for more information on how to detect and handle XFA documents.

            ValueError:
                If the `configuration` is invalid, e.g. because the creating provider has been closed.

            pdftools_sdk.not_found_error.NotFoundError:
                If the :attr:`pdftools_sdk.sign.signature_configuration.SignatureConfiguration.field_name`  does not exist in `document`.

            pdftools_sdk.retry_error.RetryError:
                If an unexpected error occurs that can be resolved by retrying the operation.
                For example, if a signature service returns an unexpectedly large signature.

            pdftools_sdk.retry_error.RetryError:
                If a resource required by the cryptographic provider is temporarily unavailable.

            pdftools_sdk.http_error.HttpError:
                If a network error occurs, e.g. downloading revocation information (OCSP, CRL) or a time-stamp.

            pdftools_sdk.unsupported_feature_error.UnsupportedFeatureError:
                If the cryptographic provider does not support the requested signing algorithm.

            pdftools_sdk.permission_error.PermissionError:
                If the cryptographic provider does not allow the signing operation.


        """
        from pdftools_sdk.pdf.document import Document
        from pdftools_sdk.sign.signature_configuration import SignatureConfiguration
        from pdftools_sdk.sign.mdp_permission_options import MdpPermissionOptions
        from pdftools_sdk.sign.output_options import OutputOptions

        if not isinstance(document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(document).__name__}.")
        if not isinstance(configuration, SignatureConfiguration):
            raise TypeError(f"Expected type {SignatureConfiguration.__name__}, but got {type(configuration).__name__}.")
        if not isinstance(stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(stream).__name__}.")
        if permissions is not None and not isinstance(permissions, MdpPermissionOptions):
            raise TypeError(f"Expected type {MdpPermissionOptions.__name__} or None, but got {type(permissions).__name__}.")
        if output_options is not None and not isinstance(output_options, OutputOptions):
            raise TypeError(f"Expected type {OutputOptions.__name__} or None, but got {type(output_options).__name__}.")

        _lib.PdfToolsSign_Signer_Certify.argtypes = [c_void_p, c_void_p, c_void_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor), c_void_p, c_void_p]
        _lib.PdfToolsSign_Signer_Certify.restype = c_void_p
        ret_val = _lib.PdfToolsSign_Signer_Certify(self._handle, document._handle, configuration._handle, _StreamDescriptor(stream), permissions._handle if permissions is not None else None, output_options._handle if output_options is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Document._create_dynamic_type(ret_val)


    def add_timestamp(self, document: Document, configuration: TimestampConfiguration, stream: io.IOBase, output_options: Optional[OutputOptions] = None) -> Document:
        """
        Add a document time-stamp

         
        This type of signature provides evidence that the document existed at a specific time and protects the document’s integrity.
         
        The features and format of the signature are defined by the :class:`pdftools_sdk.crypto.providers.provider.Provider`  and the
        `configuration`.
         
        Non-critical processing errors raise a :func:`pdftools_sdk.sign.signer.WarningFunc` .
        It is recommended to review the :class:`pdftools_sdk.sign.warning_category.WarningCategory`  and handle them if necessary for the application.



        Args:
            document (pdftools_sdk.pdf.document.Document): 
                The input document to add a time-stamp to

            configuration (pdftools_sdk.sign.timestamp_configuration.TimestampConfiguration): 
                The time-stamp configuration

            stream (io.IOBase): 
                The stream where the output document is written

            outputOptions (Optional[pdftools_sdk.sign.output_options.OutputOptions]): 
                Document-level output options not directly related to the document time-stamp



        Returns:
            pdftools_sdk.pdf.document.Document: 


        Raises:
            pdftools_sdk.license_error.LicenseError:
                The license check has failed.

            OSError:
                Writing to the `stream` failed.

            pdftools_sdk.unsupported_feature_error.UnsupportedFeatureError:
                The input PDF contains unrendered XFA form fields.
                See :attr:`pdftools_sdk.pdf.document.Document.xfa`  for more information on how to detect and handle XFA documents.

            ValueError:
                If the `configuration` is invalid, e.g. because the creating provider has been closed.

            pdftools_sdk.not_found_error.NotFoundError:
                If the :attr:`pdftools_sdk.sign.signature_configuration.SignatureConfiguration.field_name`  does not exist in `document`.

            pdftools_sdk.retry_error.RetryError:
                If an unexpected error occurs that can be resolved by retrying the operation.
                For example, if a signature service returns an unexpectedly large signature.

            pdftools_sdk.retry_error.RetryError:
                If a resource required by the cryptographic provider is temporarily unavailable.

            pdftools_sdk.http_error.HttpError:
                If a network error occurs, e.g. downloading revocation information (OCSP, CRL) or a time-stamp.

            pdftools_sdk.unsupported_feature_error.UnsupportedFeatureError:
                If the cryptographic provider does not support the requested signing algorithm.

            pdftools_sdk.permission_error.PermissionError:
                If the cryptographic provider does not allow the signing operation.


        """
        from pdftools_sdk.pdf.document import Document
        from pdftools_sdk.sign.timestamp_configuration import TimestampConfiguration
        from pdftools_sdk.sign.output_options import OutputOptions

        if not isinstance(document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(document).__name__}.")
        if not isinstance(configuration, TimestampConfiguration):
            raise TypeError(f"Expected type {TimestampConfiguration.__name__}, but got {type(configuration).__name__}.")
        if not isinstance(stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(stream).__name__}.")
        if output_options is not None and not isinstance(output_options, OutputOptions):
            raise TypeError(f"Expected type {OutputOptions.__name__} or None, but got {type(output_options).__name__}.")

        _lib.PdfToolsSign_Signer_AddTimestamp.argtypes = [c_void_p, c_void_p, c_void_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor), c_void_p]
        _lib.PdfToolsSign_Signer_AddTimestamp.restype = c_void_p
        ret_val = _lib.PdfToolsSign_Signer_AddTimestamp(self._handle, document._handle, configuration._handle, _StreamDescriptor(stream), output_options._handle if output_options is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Document._create_dynamic_type(ret_val)


    def add_signature_field(self, document: Document, options: SignatureFieldOptions, stream: io.IOBase, output_options: Optional[OutputOptions] = None) -> Document:
        """
        Add an unsigned signature field

         
        Add an unsigned signature field that can later be signed (see :class:`pdftools_sdk.pdf.unsigned_signature_field.UnsignedSignatureField` ).
         
        Non-critical processing errors raise a :func:`pdftools_sdk.sign.signer.WarningFunc` .
        It is recommended to review the :class:`pdftools_sdk.sign.warning_category.WarningCategory`  and handle them if necessary for the application.



        Args:
            document (pdftools_sdk.pdf.document.Document): 
                The input document to add the signature field to

            options (pdftools_sdk.sign.signature_field_options.SignatureFieldOptions): 
                The options for the unsigned signature field

            stream (io.IOBase): 
                The stream where the output document is written

            outputOptions (Optional[pdftools_sdk.sign.output_options.OutputOptions]): 
                Document-level output options not directly related to the signature field



        Returns:
            pdftools_sdk.pdf.document.Document: 


        Raises:
            pdftools_sdk.license_error.LicenseError:
                The license check has failed.

            OSError:
                Writing to the `stream` failed.

            pdftools_sdk.unsupported_feature_error.UnsupportedFeatureError:
                The input PDF contains unrendered XFA form fields.
                See :attr:`pdftools_sdk.pdf.document.Document.xfa`  for more information on how to detect and handle XFA documents.

            pdftools_sdk.exists_error.ExistsError:
                The :attr:`pdftools_sdk.sign.signature_field_options.SignatureFieldOptions.field_name`  exists already in the input document.


        """
        from pdftools_sdk.pdf.document import Document
        from pdftools_sdk.sign.signature_field_options import SignatureFieldOptions
        from pdftools_sdk.sign.output_options import OutputOptions

        if not isinstance(document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(document).__name__}.")
        if not isinstance(options, SignatureFieldOptions):
            raise TypeError(f"Expected type {SignatureFieldOptions.__name__}, but got {type(options).__name__}.")
        if not isinstance(stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(stream).__name__}.")
        if output_options is not None and not isinstance(output_options, OutputOptions):
            raise TypeError(f"Expected type {OutputOptions.__name__} or None, but got {type(output_options).__name__}.")

        _lib.PdfToolsSign_Signer_AddSignatureField.argtypes = [c_void_p, c_void_p, c_void_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor), c_void_p]
        _lib.PdfToolsSign_Signer_AddSignatureField.restype = c_void_p
        ret_val = _lib.PdfToolsSign_Signer_AddSignatureField(self._handle, document._handle, options._handle, _StreamDescriptor(stream), output_options._handle if output_options is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Document._create_dynamic_type(ret_val)


    def add_prepared_signature(self, document: Document, configuration: SignatureConfiguration, stream: io.IOBase, output_options: Optional[OutputOptions] = None) -> PreparedDocument:
        """
        Add a prepared signature

         
        Adding a prepared signature is only required in very particular or specialized use cases.
        This method is the same as :meth:`pdftools_sdk.sign.signer.Signer.sign` , but without actually creating the cryptographic signature.
        The cryptographic signature can be inserted later using :meth:`pdftools_sdk.sign.signer.Signer.sign_prepared_signature` .
         
        While the `configuration` can be created by any :class:`pdftools_sdk.crypto.providers.provider.Provider` ,
        it is typically created by :meth:`pdftools_sdk.crypto.providers.built_in.provider.Provider.create_prepared_signature` .



        Args:
            document (pdftools_sdk.pdf.document.Document): 
                The input document to add the prepared signature

            configuration (pdftools_sdk.sign.signature_configuration.SignatureConfiguration): 
                The signature configuration

            stream (io.IOBase): 
                The stream where the output document is written

            outputOptions (Optional[pdftools_sdk.sign.output_options.OutputOptions]): 
                Document-level output options not directly related to preparing the signature



        Returns:
            pdftools_sdk.sign.prepared_document.PreparedDocument: 


        Raises:
            pdftools_sdk.license_error.LicenseError:
                The license check has failed.

            OSError:
                Writing to the `stream` failed.

            pdftools_sdk.unsupported_feature_error.UnsupportedFeatureError:
                The input PDF contains unrendered XFA form fields.
                See :attr:`pdftools_sdk.pdf.document.Document.xfa`  for more information on how to detect and handle XFA documents.

            ValueError:
                If the `configuration` is invalid, e.g. because the creating provider has been closed

            pdftools_sdk.not_found_error.NotFoundError:
                If the :attr:`pdftools_sdk.sign.signature_configuration.SignatureConfiguration.field_name`  does not exist in `document`.

            pdftools_sdk.unsupported_feature_error.UnsupportedFeatureError:
                If the cryptographic provider does not support the requested signing algorithm.

            pdftools_sdk.http_error.HttpError:
                If a network error occurs, e.g. downloading revocation information (OCSP, CRL).


        """
        from pdftools_sdk.pdf.document import Document
        from pdftools_sdk.sign.signature_configuration import SignatureConfiguration
        from pdftools_sdk.sign.output_options import OutputOptions
        from pdftools_sdk.sign.prepared_document import PreparedDocument

        if not isinstance(document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(document).__name__}.")
        if not isinstance(configuration, SignatureConfiguration):
            raise TypeError(f"Expected type {SignatureConfiguration.__name__}, but got {type(configuration).__name__}.")
        if not isinstance(stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(stream).__name__}.")
        if output_options is not None and not isinstance(output_options, OutputOptions):
            raise TypeError(f"Expected type {OutputOptions.__name__} or None, but got {type(output_options).__name__}.")

        _lib.PdfToolsSign_Signer_AddPreparedSignature.argtypes = [c_void_p, c_void_p, c_void_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor), c_void_p]
        _lib.PdfToolsSign_Signer_AddPreparedSignature.restype = c_void_p
        ret_val = _lib.PdfToolsSign_Signer_AddPreparedSignature(self._handle, document._handle, configuration._handle, _StreamDescriptor(stream), output_options._handle if output_options is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return PreparedDocument._create_dynamic_type(ret_val)


    def sign_prepared_signature(self, document: Document, configuration: SignatureConfiguration, stream: io.IOBase) -> Document:
        """
        Sign a prepared signature

        Sign a document that contains a prepared signature created using :meth:`pdftools_sdk.sign.signer.Signer.add_prepared_signature` .
        Note that the `configuration` must be compatible to the configuration used when preparing the signature.



        Args:
            document (pdftools_sdk.pdf.document.Document): 
                The input document to sign

            configuration (pdftools_sdk.sign.signature_configuration.SignatureConfiguration): 
                The signature configuration

            stream (io.IOBase): 
                The stream where the signed document is written



        Returns:
            pdftools_sdk.pdf.document.Document: 


        Raises:
            pdftools_sdk.license_error.LicenseError:
                The license check has failed.

            OSError:
                Writing to the `stream` failed.

            ValueError:
                If the `document` does not contain a prepared signature created by :meth:`pdftools_sdk.sign.signer.Signer.add_prepared_signature` 

            ValueError:
                If the `configuration` is invalid, e.g. because the creating provider has been closed.

            pdftools_sdk.retry_error.RetryError:
                If an unexpected error occurs that can be resolved by retrying the operation.
                For example, if a signature service returns an unexpectedly large signature.

            pdftools_sdk.retry_error.RetryError:
                If a resource required by the cryptographic provider is temporarily unavailable.

            pdftools_sdk.http_error.HttpError:
                If a network error occurs, e.g. downloading revocation information (OCSP, CRL) or a time-stamp.

            pdftools_sdk.unsupported_feature_error.UnsupportedFeatureError:
                If the cryptographic provider does not support the requested signing algorithm.

            pdftools_sdk.permission_error.PermissionError:
                If the cryptographic provider does not allow the signing operation.


        """
        from pdftools_sdk.pdf.document import Document
        from pdftools_sdk.sign.signature_configuration import SignatureConfiguration

        if not isinstance(document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(document).__name__}.")
        if not isinstance(configuration, SignatureConfiguration):
            raise TypeError(f"Expected type {SignatureConfiguration.__name__}, but got {type(configuration).__name__}.")
        if not isinstance(stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(stream).__name__}.")

        _lib.PdfToolsSign_Signer_SignPreparedSignature.argtypes = [c_void_p, c_void_p, c_void_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor)]
        _lib.PdfToolsSign_Signer_SignPreparedSignature.restype = c_void_p
        ret_val = _lib.PdfToolsSign_Signer_SignPreparedSignature(self._handle, document._handle, configuration._handle, _StreamDescriptor(stream))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Document._create_dynamic_type(ret_val)


    def process(self, document: Document, stream: io.IOBase, output_options: Optional[OutputOptions] = None, provider: Optional[Provider] = None) -> Document:
        """
        Process a document

         
        Apply document-level processing options without any signature operation.
        For example:
         
        - To encrypt or decrypt PDF documents that may be signed (see the samples "Encrypt" and "Decrypt").
        - To remove signatures and unsigned signature fields (see :attr:`pdftools_sdk.sign.output_options.OutputOptions.remove_signatures` ).
        - To add validation information to existing signatures (see :attr:`pdftools_sdk.sign.output_options.OutputOptions.add_validation_information` ).
         
         
        Non-critical processing errors raise a :func:`pdftools_sdk.sign.signer.WarningFunc` .
        It is recommended to review the :class:`pdftools_sdk.sign.warning_category.WarningCategory`  and handle them if necessary for the application.



        Args:
            document (pdftools_sdk.pdf.document.Document): 
                The input document to process

            stream (io.IOBase): 
                The stream where the output document is written

            outputOptions (Optional[pdftools_sdk.sign.output_options.OutputOptions]): 
                The document-level processing options

            provider (Optional[pdftools_sdk.crypto.providers.provider.Provider]): 
                The cryptographic provider to use to add validation information to existing signatures of input document
                (see :attr:`pdftools_sdk.sign.output_options.OutputOptions.add_validation_information` ).
                Can be `None` if no validation information is added or to use the default provider.



        Returns:
            pdftools_sdk.pdf.document.Document: 


        Raises:
            pdftools_sdk.license_error.LicenseError:
                The license check has failed.

            OSError:
                Writing to the `stream` failed.

            pdftools_sdk.unsupported_feature_error.UnsupportedFeatureError:
                The input PDF contains unrendered XFA form fields.
                See :attr:`pdftools_sdk.pdf.document.Document.xfa`  for more information on how to detect and handle XFA documents.

            pdftools_sdk.http_error.HttpError:
                If a network error occurs, e.g. downloading revocation information (OCSP, CRL).


        """
        from pdftools_sdk.pdf.document import Document
        from pdftools_sdk.sign.output_options import OutputOptions
        from pdftools_sdk.crypto.providers.provider import Provider

        if not isinstance(document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(document).__name__}.")
        if not isinstance(stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(stream).__name__}.")
        if output_options is not None and not isinstance(output_options, OutputOptions):
            raise TypeError(f"Expected type {OutputOptions.__name__} or None, but got {type(output_options).__name__}.")
        if provider is not None and not isinstance(provider, Provider):
            raise TypeError(f"Expected type {Provider.__name__} or None, but got {type(provider).__name__}.")

        _lib.PdfToolsSign_Signer_Process.argtypes = [c_void_p, c_void_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor), c_void_p, c_void_p]
        _lib.PdfToolsSign_Signer_Process.restype = c_void_p
        ret_val = _lib.PdfToolsSign_Signer_Process(self._handle, document._handle, _StreamDescriptor(stream), output_options._handle if output_options is not None else None, provider._handle if provider is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Document._create_dynamic_type(ret_val)



    def add_warning_handler(self, handler: WarningFunc) -> None:
        """
        Add handler for the :func:`WarningFunc` event.

        Args:
            handler: Event handler. If a handler is added that is already registered, it is ignored.
        """
        _lib.PdfToolsSign_Signer_AddWarningHandlerW.argtypes = [c_void_p, c_void_p, self._WarningFunc]
        _lib.PdfToolsSign_Signer_AddWarningHandlerW.restype = c_bool

        # Wrap the handler with the C callback
        _c_callback = self._wrap_warning_func(handler)

        # Now pass the callback function as a proper C function type instance
        if not _lib.PdfToolsSign_Signer_AddWarningHandlerW(self._handle, None, _c_callback):
            _NativeBase._throw_last_error()

        # Add to the class-level callback map (increase count if already added)
        if handler in self._warning_callback_map:
            self._warning_callback_map[handler]['count'] += 1
        else:
            self._warning_callback_map[handler] = {'callback': _c_callback, 'count': 1}

    def remove_warning_handler(self, handler: WarningFunc) -> None:
        """
        Remove registered handler of the :func:`WarningFunc` event.

        Args:
            handler: Event handler that shall be removed. If a handler is not registered, it is ignored.
        """
        _lib.PdfToolsSign_Signer_RemoveWarningHandlerW.argtypes = [c_void_p, c_void_p, self._WarningFunc]
        _lib.PdfToolsSign_Signer_RemoveWarningHandlerW.restype = c_bool

        # Check if the handler exists in the class-level map
        if handler in self._warning_callback_map:
            from pdftools_sdk.not_found_error import NotFoundError
            _c_callback = self._warning_callback_map[handler]['callback']
            try:
                if not _lib.PdfToolsSign_Signer_RemoveWarningHandlerW(self._handle, None, _c_callback):
                    _NativeBase._throw_last_error()
            except pdftools_sdk.NotFoundError as e:
                del self._warning_callback_map[handler]

            # Decrease the count or remove the callback entirely
            if self._warning_callback_map[handler]['count'] > 1:
                self._warning_callback_map[handler]['count'] -= 1
            else:
                del self._warning_callback_map[handler]


    @staticmethod
    def _create_dynamic_type(handle):
        return Signer._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Signer.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
        self._warning_callback_map = {}

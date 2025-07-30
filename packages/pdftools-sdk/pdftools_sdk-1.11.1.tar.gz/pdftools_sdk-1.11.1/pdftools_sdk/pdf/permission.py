from ctypes import *
from enum import Flag

class Permission(Flag):
    """
    The permissions allowed by a PDF document

     
    - See :attr:`pdftools_sdk.pdf.document.Document.permissions`  to read the permissions of a PDF document.
    - See :attr:`pdftools_sdk.pdf.output_options.OutputOptions.encryption`  to set the permissions when encrypting a PDF document.
     


    """
    NONE = 0
    PRINT = 4
    MODIFY = 8
    COPY = 16
    ANNOTATE = 32
    FILL_FORMS = 256
    SUPPORT_DISABILITIES = 512
    ASSEMBLE = 1024
    DIGITAL_PRINT = 2048

    ALL = 3900

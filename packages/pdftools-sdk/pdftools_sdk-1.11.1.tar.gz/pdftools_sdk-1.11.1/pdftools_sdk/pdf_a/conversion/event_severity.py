from ctypes import *
from enum import IntEnum

class EventSeverity(IntEnum):
    """
    The severity of conversion events

    See :func:`pdftools_sdk.pdf_a.conversion.converter.ConversionEventFunc`  for more information on conversion events.



    Attributes:
        INFORMATION (int):
             
            An informational event requires no further action.
             
            By default events of the following :class:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory`  are classified as :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.INFORMATION` :
             
            - :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.MANAGEDCOLORS`
            - :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.CHANGEDCOLORANT`
            - :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDEXTERNALCONTENT`
            - :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.CONVERTEDFONT`
            - :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.SUBSTITUTEDFONT`
            - :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDANNOTATION`
            - :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDMULTIMEDIA`
            - :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDACTION`
            - :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDMETADATA`
            - :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDSTRUCTURE`
            - :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.CONVERTEDEMBEDDEDFILE`
            - :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDSIGNATURE`
             

        WARNING (int):
             
            An warning that might require further actions.
             
            By default events of the following :class:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory`  are classified as :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.WARNING` :
             
            - :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.VISUALDIFFERENCES`
            - :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REPAIREDCORRUPTION`
            - :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDTRANSPARENCY`  (PDF/A-1 only)
            - :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDEMBEDDEDFILE`   (PDF/A-1 and PDF/A-2 only)
            - :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDOPTIONALCONTENT`  (PDF/A-1 only)
             

        ERROR (int):
             
            A critical issue for which the conversion must be considered as failed.
             
            By default no event uses this severity.


    """
    INFORMATION = 1
    WARNING = 2
    ERROR = 3


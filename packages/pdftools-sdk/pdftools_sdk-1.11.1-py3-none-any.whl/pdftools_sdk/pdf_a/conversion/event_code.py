from ctypes import *
from enum import IntEnum

class EventCode(IntEnum):
    """
    The code identifying particular conversion events

    See :func:`pdftools_sdk.pdf_a.conversion.converter.ConversionEventFunc`  for more information on conversion events.



    Attributes:
        GENERIC (int):
            Code for events that do not have a specific code associated.

        REMOVED_XFA (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.VISUALDIFFERENCES` 

        FONT_NON_EMBEDDED_ORDERING_IDENTITY (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.VISUALDIFFERENCES` 

        FONT_NO_ROTATE (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.VISUALDIFFERENCES` 

        FONT_NO_ITALIC_SIMULATION (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.VISUALDIFFERENCES` 

        CLIPPED_NUMBER_VALUE (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.VISUALDIFFERENCES` 

        RECOVERED_IMAGE_SIZE (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REPAIREDCORRUPTION` 

        REPAIRED_FONT (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REPAIREDCORRUPTION` 

        COPIED_OUTPUT_INTENT (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.MANAGEDCOLORS` 

        SET_OUTPUT_INTENT (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.MANAGEDCOLORS` 

        GENERATED_OUTPUT_INTENT (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.MANAGEDCOLORS` 

        SET_COLOR_PROFILE (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.MANAGEDCOLORS` 

        GENERATED_COLOR_PROFILE (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.MANAGEDCOLORS` 

        CREATED_CALIBRATED (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.MANAGEDCOLORS` 

        RENAMED_COLORANT (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.CHANGEDCOLORANT` 

        RESOLVED_COLORANT_COLLISION (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.CHANGEDCOLORANT` 

        EMBEDED_FONT (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.CONVERTEDFONT` 

        SUBSTITUTED_FONT (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.SUBSTITUTEDFONT` 

        SUBSTITUTED_MULTIPLE_MASTER (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.SUBSTITUTEDFONT` 

        CONVERTED_TO_STAMP (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDANNOTATION` 

        REMOVED_DOCUMENT_METADATA (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDMETADATA` 

        COPIED_EMBEDDED_FILE (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.CONVERTEDEMBEDDEDFILE` 

        CONVERTING_EMBEDDED_FILE_START (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.CONVERTEDEMBEDDEDFILE` 

        CONVERTING_EMBEDDED_FILE_SUCCESS (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.CONVERTEDEMBEDDEDFILE` 

        CHANGED_TO_INITIAL_DOCUMENT (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDEMBEDDEDFILE` 

        CONVERTING_EMBEDDED_FILE_ERROR (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDEMBEDDEDFILE` 

        REMOVED_EMBEDDED_FILE (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDEMBEDDEDFILE` 

        REMOVED_FILE_ATTACHMENT_ANNOTATION (int):
            see :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDEMBEDDEDFILE` 


    """
    GENERIC = 0x00000001
    REMOVED_XFA = 0x01000000
    FONT_NON_EMBEDDED_ORDERING_IDENTITY = 0x01000001
    FONT_NO_ROTATE = 0x01000002
    FONT_NO_ITALIC_SIMULATION = 0x01000003
    CLIPPED_NUMBER_VALUE = 0x01000004
    RECOVERED_IMAGE_SIZE = 0x02000000
    REPAIRED_FONT = 0x02000001
    COPIED_OUTPUT_INTENT = 0x03000000
    SET_OUTPUT_INTENT = 0x03000001
    GENERATED_OUTPUT_INTENT = 0x03000002
    SET_COLOR_PROFILE = 0x03000003
    GENERATED_COLOR_PROFILE = 0x03000004
    CREATED_CALIBRATED = 0x03000005
    RENAMED_COLORANT = 0x04000000
    RESOLVED_COLORANT_COLLISION = 0x04000001
    EMBEDED_FONT = 0x06000000
    SUBSTITUTED_FONT = 0x07000000
    SUBSTITUTED_MULTIPLE_MASTER = 0x07000001
    CONVERTED_TO_STAMP = 0x09000000
    REMOVED_DOCUMENT_METADATA = 0x0C000000
    COPIED_EMBEDDED_FILE = 0x0F000000
    CONVERTING_EMBEDDED_FILE_START = 0x0F000001
    CONVERTING_EMBEDDED_FILE_SUCCESS = 0x0F000002
    CHANGED_TO_INITIAL_DOCUMENT = 0x10000000
    CONVERTING_EMBEDDED_FILE_ERROR = 0x10000001
    REMOVED_EMBEDDED_FILE = 0x10000002
    REMOVED_FILE_ATTACHMENT_ANNOTATION = 0x10000003


def _import_types():
    global Converter
    from pdftools_sdk.pdf_a.conversion.converter import Converter
    global ConversionOptions
    from pdftools_sdk.pdf_a.conversion.conversion_options import ConversionOptions

    global EventSeverity
    from pdftools_sdk.pdf_a.conversion.event_severity import EventSeverity
    global EventCategory
    from pdftools_sdk.pdf_a.conversion.event_category import EventCategory
    global EventCode
    from pdftools_sdk.pdf_a.conversion.event_code import EventCode
    global InvoiceType
    from pdftools_sdk.pdf_a.conversion.invoice_type import InvoiceType
    global AFRelationship
    from pdftools_sdk.pdf_a.conversion.a_f_relationship import AFRelationship


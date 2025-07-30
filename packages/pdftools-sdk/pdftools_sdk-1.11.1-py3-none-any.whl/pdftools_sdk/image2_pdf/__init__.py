import pdftools_sdk.image2_pdf.profiles

def _import_types():
    global ImageMapping
    from pdftools_sdk.image2_pdf.image_mapping import ImageMapping
    global Auto
    from pdftools_sdk.image2_pdf.auto import Auto
    global ShrinkToPage
    from pdftools_sdk.image2_pdf.shrink_to_page import ShrinkToPage
    global ShrinkToFit
    from pdftools_sdk.image2_pdf.shrink_to_fit import ShrinkToFit
    global ShrinkToPortrait
    from pdftools_sdk.image2_pdf.shrink_to_portrait import ShrinkToPortrait
    global ImageOptions
    from pdftools_sdk.image2_pdf.image_options import ImageOptions
    global Converter
    from pdftools_sdk.image2_pdf.converter import Converter

    pdftools_sdk.image2_pdf.profiles._import_types()


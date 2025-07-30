import pdftools_sdk.internal
import pdftools_sdk.pdf
import pdftools_sdk.image
import pdftools_sdk.document_assembly
import pdftools_sdk.optimization
import pdftools_sdk.pdf2_image
import pdftools_sdk.image2_pdf
import pdftools_sdk.pdf_a
import pdftools_sdk.sign
import pdftools_sdk.crypto
import pdftools_sdk.signature_validation
import pdftools_sdk.extraction
import pdftools_sdk.sys
import pdftools_sdk.geometry

def _import_types():
    global ConsumptionData
    from pdftools_sdk.consumption_data import ConsumptionData
    global LicenseInfo
    from pdftools_sdk.license_info import LicenseInfo
    global Sdk
    from pdftools_sdk.sdk import Sdk
    global StringList
    from pdftools_sdk.string_list import StringList
    global MetadataDictionary
    from pdftools_sdk.metadata_dictionary import MetadataDictionary
    global HttpClientHandler
    from pdftools_sdk.http_client_handler import HttpClientHandler

    pdftools_sdk.pdf._import_types()
    pdftools_sdk.image._import_types()
    pdftools_sdk.document_assembly._import_types()
    pdftools_sdk.optimization._import_types()
    pdftools_sdk.pdf2_image._import_types()
    pdftools_sdk.image2_pdf._import_types()
    pdftools_sdk.pdf_a._import_types()
    pdftools_sdk.sign._import_types()
    pdftools_sdk.crypto._import_types()
    pdftools_sdk.signature_validation._import_types()
    pdftools_sdk.extraction._import_types()
    pdftools_sdk.sys._import_types()
    pdftools_sdk.geometry._import_types()


_import_types()
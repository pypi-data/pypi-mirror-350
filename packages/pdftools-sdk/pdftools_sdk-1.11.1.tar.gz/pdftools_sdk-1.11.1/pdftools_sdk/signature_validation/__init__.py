import pdftools_sdk.signature_validation.profiles

def _import_types():
    global ConstraintResult
    from pdftools_sdk.signature_validation.constraint_result import ConstraintResult
    global Validator
    from pdftools_sdk.signature_validation.validator import Validator
    global Certificate
    from pdftools_sdk.signature_validation.certificate import Certificate
    global CertificateChain
    from pdftools_sdk.signature_validation.certificate_chain import CertificateChain
    global ValidationResults
    from pdftools_sdk.signature_validation.validation_results import ValidationResults
    global ValidationResult
    from pdftools_sdk.signature_validation.validation_result import ValidationResult
    global SignatureContent
    from pdftools_sdk.signature_validation.signature_content import SignatureContent
    global UnsupportedSignatureContent
    from pdftools_sdk.signature_validation.unsupported_signature_content import UnsupportedSignatureContent
    global CmsSignatureContent
    from pdftools_sdk.signature_validation.cms_signature_content import CmsSignatureContent
    global TimeStampContent
    from pdftools_sdk.signature_validation.time_stamp_content import TimeStampContent
    global CustomTrustList
    from pdftools_sdk.signature_validation.custom_trust_list import CustomTrustList

    global Indication
    from pdftools_sdk.signature_validation.indication import Indication
    global SubIndication
    from pdftools_sdk.signature_validation.sub_indication import SubIndication
    global SignatureSelector
    from pdftools_sdk.signature_validation.signature_selector import SignatureSelector
    global TimeSource
    from pdftools_sdk.signature_validation.time_source import TimeSource
    global DataSource
    from pdftools_sdk.signature_validation.data_source import DataSource

    pdftools_sdk.signature_validation.profiles._import_types()


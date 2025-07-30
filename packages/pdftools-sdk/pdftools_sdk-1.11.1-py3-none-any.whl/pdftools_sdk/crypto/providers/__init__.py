import pdftools_sdk.crypto.providers.global_sign_dss
import pdftools_sdk.crypto.providers.swisscom_sig_srv
import pdftools_sdk.crypto.providers.pkcs11
import pdftools_sdk.crypto.providers.built_in

def _import_types():
    global Provider
    from pdftools_sdk.crypto.providers.provider import Provider
    global Certificate
    from pdftools_sdk.crypto.providers.certificate import Certificate
    global CertificateList
    from pdftools_sdk.crypto.providers.certificate_list import CertificateList

    pdftools_sdk.crypto.providers.global_sign_dss._import_types()
    pdftools_sdk.crypto.providers.swisscom_sig_srv._import_types()
    pdftools_sdk.crypto.providers.pkcs11._import_types()
    pdftools_sdk.crypto.providers.built_in._import_types()


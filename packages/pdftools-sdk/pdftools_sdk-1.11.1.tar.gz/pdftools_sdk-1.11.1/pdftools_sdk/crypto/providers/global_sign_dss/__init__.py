def _import_types():
    global SignatureConfiguration
    from pdftools_sdk.crypto.providers.global_sign_dss.signature_configuration import SignatureConfiguration
    global TimestampConfiguration
    from pdftools_sdk.crypto.providers.global_sign_dss.timestamp_configuration import TimestampConfiguration
    global Session
    from pdftools_sdk.crypto.providers.global_sign_dss.session import Session


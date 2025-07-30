def _import_types():
    global SignatureConfiguration
    from pdftools_sdk.crypto.providers.swisscom_sig_srv.signature_configuration import SignatureConfiguration
    global TimestampConfiguration
    from pdftools_sdk.crypto.providers.swisscom_sig_srv.timestamp_configuration import TimestampConfiguration
    global StepUp
    from pdftools_sdk.crypto.providers.swisscom_sig_srv.step_up import StepUp
    global Session
    from pdftools_sdk.crypto.providers.swisscom_sig_srv.session import Session


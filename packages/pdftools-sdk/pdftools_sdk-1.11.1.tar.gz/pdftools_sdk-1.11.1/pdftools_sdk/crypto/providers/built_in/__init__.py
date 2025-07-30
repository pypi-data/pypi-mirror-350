def _import_types():
    global SignatureConfiguration
    from pdftools_sdk.crypto.providers.built_in.signature_configuration import SignatureConfiguration
    global TimestampConfiguration
    from pdftools_sdk.crypto.providers.built_in.timestamp_configuration import TimestampConfiguration
    global Provider
    from pdftools_sdk.crypto.providers.built_in.provider import Provider


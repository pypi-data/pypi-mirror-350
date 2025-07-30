def _import_types():
    global SignatureConfiguration
    from pdftools_sdk.crypto.providers.pkcs11.signature_configuration import SignatureConfiguration
    global TimestampConfiguration
    from pdftools_sdk.crypto.providers.pkcs11.timestamp_configuration import TimestampConfiguration
    global Module
    from pdftools_sdk.crypto.providers.pkcs11.module import Module
    global Device
    from pdftools_sdk.crypto.providers.pkcs11.device import Device
    global Session
    from pdftools_sdk.crypto.providers.pkcs11.session import Session
    global DeviceList
    from pdftools_sdk.crypto.providers.pkcs11.device_list import DeviceList


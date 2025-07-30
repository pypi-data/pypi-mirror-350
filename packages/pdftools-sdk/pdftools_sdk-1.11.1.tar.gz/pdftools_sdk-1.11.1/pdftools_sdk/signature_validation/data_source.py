from ctypes import *
from enum import Flag

class DataSource(Flag):
    """
    The source of data such as certificates, OCRPs or CRLs


    """
    EMBED_IN_SIGNATURE = 0x0001
    EMBED_IN_DOCUMENT = 0x0002
    DOWNLOAD = 0x0004
    SYSTEM = 0x0008
    AATL = 0x0100
    EUTL = 0x0200
    CUSTOM_TRUST_LIST = 0x0400


from ctypes import *
from enum import Flag

class TimeSource(Flag):
    """
    The source of the validation time


    """
    PROOF_OF_EXISTENCE = 0x0001
    EXPIRED_TIME_STAMP = 0x0002
    SIGNATURE_TIME = 0x0004


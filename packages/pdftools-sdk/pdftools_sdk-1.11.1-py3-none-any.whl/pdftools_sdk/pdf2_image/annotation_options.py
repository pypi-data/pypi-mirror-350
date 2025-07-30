from ctypes import *
from enum import IntEnum

class AnnotationOptions(IntEnum):
    """
    Defines how to render annotations and their popups

     
    Annotations associate an object such as a sticky note, link or rich media
    with a location on a PDF page; they may also provide user interaction
    by means of the mouse and keyboard.
     
    Some annotations have an associated popup.



    Attributes:
        SHOW_ANNOTATIONS (int):
        SHOW_ANNOTATIONS_AND_POPUPS (int):

    """
    SHOW_ANNOTATIONS = 1
    SHOW_ANNOTATIONS_AND_POPUPS = 2


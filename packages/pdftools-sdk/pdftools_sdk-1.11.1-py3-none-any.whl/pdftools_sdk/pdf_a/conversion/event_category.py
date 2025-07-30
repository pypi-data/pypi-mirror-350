from ctypes import *
from enum import IntEnum

class EventCategory(IntEnum):
    """
    The category of conversion events

    See :func:`pdftools_sdk.pdf_a.conversion.converter.ConversionEventFunc`  for more information on conversion events.



    Attributes:
        VISUAL_DIFFERENCES (int):
             
            The conversion is optimized to preserve the visual appearance of documents.
            However, under some circumstances visual differences cannot be avoided.
            This is typically the case for low quality and erroneous input documents.
             
            Examples:
             
            - The visual appearance of a proprietary annotation type could not be generated.
            - Numbers that exceed the allowed value range have been clipped.
            - Text of an invalid font is unclear because its mapping to glyphs is ambiguous.
             
             
            Suggested severity: :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.WARNING` 
             
            It is not possible for the SDK to gauge the effect of the visual differences on the document's content.
            Therefore, it is recommended to let a user assess, whether or not the conversion result is acceptable.
            If a manual review is not feasible, events of this category should be classified as an :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.ERROR` .

        REPAIRED_CORRUPTION (int):
             
            Corrupt documents are repaired automatically.
            Since the specification does not define how corrupt documents should be repaired, each viewer has its own heuristics for doing so.
            Therefore, the repaired document might have visual differences to the input document in your viewer.
            For that reason, an event is generated such that the repaired document can be reviewed, similarly to :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.VISUALDIFFERENCES` .
             
            Examples for documents that must be repaired:
             
            - The document has been damaged, e.g. during an incomplete file upload.
            - The document has been created by an erroneous application.
             
             
            Suggested severity: :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.WARNING` 

        MANAGED_COLORS (int):
             
            Purely informational messages related to color management.
             
            Examples:
             
            - Copied PDF/A output intent from input file.
            - Embedded ICC color profile.
             
             
            Suggested severity: :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.INFORMATION` 

        CHANGED_COLORANT (int):
             
            Colorants are special inks used in addition to the process colors (e.g. red, green, and blue in the RGB color space or cyan, magenta, yellow and black in the CMYK color space).
            Popular colorants are PANTONE colors typically used in printing; or also metallic or fluorescent inks.
             
            Colorants in PDF documents contain a description that is required to paint a good approximation of the intended color in case the colorant is unavailable.
            Within the same document all descriptions for the same colorant should be equal.
            This warning is generated if conflicting descriptions must be harmonized, for example during PDF/A conversion.
             
            This has no effect on output devices where the colorant is available, e.g. on certain printers.
            For other output devices this warning may indicate visual differences.
            However, for well-formed documents (i.e. not maliciously created documents), the visual differences are not noticeable.
             
            Suggested severity: :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.INFORMATION` 

        REMOVED_EXTERNAL_CONTENT (int):
             
            Examples:
             
            - Removed references to external files containing stream data used in the document.
             
             
            Suggested severity: :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.INFORMATION` 

        CONVERTED_FONT (int):
             
            Purely informational messages related to font management.
             
            Examples:
             
            - Embedded a font.
             
             
            Suggested severity: :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.INFORMATION` 

        SUBSTITUTED_FONT (int):
             
            If a required font is not embedded and not available in the installed fonts, a similar font must be chosen and used.
            This is a commonly performed when viewing or printing a PDF document.
            While this may lead to minor visual differences, all text is preserved.
             
            It is important that the installed fonts contain all fonts that are not embedded in the input documents.
            See the product's installation documentation for a list of fonts that are recommended to install.
             
            Examples:
             
            - Substituted font 'GothicBBB-Medium' with 'MS-Gothic'.
             
             
            Suggested severity: :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.INFORMATION` 

        REMOVED_TRANSPARENCY (int):
             
            Because transparency is not allowed in PDF/A-1, transparent objects have to be converted to opaque when converting a document to PDF/A-1.
            This can lead to visual differences.
            Even though the conversion has been optimized to reduce visual differences, they might be noticeable.
            Therefore, it is highly recommended to convert documents to PDF/A-2 or higher.
            These versions of the standard allow transparency, which results in a higher conversion quality.
             
            This conversion event should be handled similarly to :attr:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory.VISUALDIFFERENCES` .
             
            Suggested severity: :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.WARNING` 

        REMOVED_ANNOTATION (int):
             
            Removing annotations does not lead to visual differences, but merely removes the interactivity of the elements.
             
            Examples:
             
            - Removed proprietary annotation types.
            - Removed forbidden annotation types, e.g. 3D.
             
             
            Suggested severity: :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.INFORMATION` 

        REMOVED_MULTIMEDIA (int):
             
             
            Suggested severity: :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.INFORMATION` 

        REMOVED_ACTION (int):
             
            Removing actions does not lead to visual differences.
             
            Examples:
             
            - Removed JavaScript actions in interactive form fields.
             
             
            Suggested severity: :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.INFORMATION` 

        REMOVED_METADATA (int):
             
            This event indicates that metadata properties have been removed during conversion.
            This includes any kind of metadata like e.g. the XMP metadata of a PDF document.
             
            Examples:
             
            - Parts of the XMP metadata of a PDF did not conform to the PDF/A standard and had to be removed.
             
             
            Suggested severity: :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.INFORMATION` 

        REMOVED_STRUCTURE (int):
             
            The logical structure of the document is a description of the content of its pages.
            This description has to be provided by the creator of the document.
            It consists of a fine granular hierarchical tagging that distinguishes between the actual content and artifacts (such as page numbers, layout artifacts, etc.).
            The tagging provides a meaningful description, for example "This is a header", "This color image shows a small sailing boat at sunset", etc.
            This information can be used e.g. to read the document to the visually impaired.
             
            The SDK has been optimized to preserve tagging information.
            Typically, tagging information only has to be removed if it is invalid or corrupt.
             
            Suggested severity: :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.INFORMATION` 

        REMOVED_OPTIONAL_CONTENT (int):
             
            Because optional content is not allowed in PDF/A-1, it has to be removed when converting a document to PDF/A-1.
            Removing layers does not change the initial appearance of pages.
            However, the visibility of content cannot be changed anymore.
            Therefore, it is highly recommended to convert documents to PDF/A-2 or higher.
            These versions of the standard allow optional content, which results in a higher conversion quality.
             
            Suggested severity: :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.WARNING` 

        CONVERTED_EMBEDDED_FILE (int):
             
            Purely informational messages related to the conversion of embedded files.
             
            Examples:
             
            - Copied an embedded file.
            - Embedded a file that has successfully been converted to PDF/A.
             
             
            Suggested severity: :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.INFORMATION` 

        REMOVED_EMBEDDED_FILE (int):
             
            Whether embedded files have to be removed depends on the conformance:
             
            - *PDF/A-1:*
              Embedded files are not allowed.
              All embedded files have to be removed.
            - *PDF/A-2:*
              Only embedded files are allowed, that conform to PDF/A.
              All embedded PDF documents are converted to PDF/A.
              All other files have to be removed.
              The Conversion Service can be used to convert PDF documents with other types of embedded files, e.g. Microsoft Office documents, images, and mails, to PDF/A-2.
            - *PDF/A-3:*
              All types of embedded files are allowed and copied as-is.
              The Conversion Service can be used, if a more fine-grained control over the conversion and copying of embedded files is required.
             
             
            Suggested severity: :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.WARNING` 

        REMOVED_SIGNATURE (int):
             
            Converting a signed document invalidates its signatures.
            For that reason, the cryptographic parts of the signatures are removed while their visual appearances are preserved.
             
            Note that we generally recommend to sign PDF/A documents only for two reasons.
            First, this ensures that the file is not corrupt and its visual appearance is well defined, such than it can be reproduced flawlessly and authentically in any environment.
            Second, PDF/A conformance is typically required if the file is to be archived, e.g. by the recipient.
            Because signed files cannot be converted to PDF/A without breaking the signature, the signature must be removed before the file can be archived.
            By converting files to PDF/A before applying the signature, this dilemma can be avoided.
             
            Suggested severity: :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.INFORMATION` 


    """
    VISUAL_DIFFERENCES = 0x00000001
    REPAIRED_CORRUPTION = 0x00000002
    MANAGED_COLORS = 0x00000004
    CHANGED_COLORANT = 0x00000008
    REMOVED_EXTERNAL_CONTENT = 0x00000010
    CONVERTED_FONT = 0x00000020
    SUBSTITUTED_FONT = 0x00000040
    REMOVED_TRANSPARENCY = 0x00000080
    REMOVED_ANNOTATION = 0x00000100
    REMOVED_MULTIMEDIA = 0x00000200
    REMOVED_ACTION = 0x00000400
    REMOVED_METADATA = 0x00000800
    REMOVED_STRUCTURE = 0x00001000
    REMOVED_OPTIONAL_CONTENT = 0x00002000
    CONVERTED_EMBEDDED_FILE = 0x00004000
    REMOVED_EMBEDDED_FILE = 0x00008000
    REMOVED_SIGNATURE = 0x00010000


def _import_types():
    global PageCopyOptions
    from pdftools_sdk.document_assembly.page_copy_options import PageCopyOptions
    global DocumentCopyOptions
    from pdftools_sdk.document_assembly.document_copy_options import DocumentCopyOptions
    global DocumentAssembler
    from pdftools_sdk.document_assembly.document_assembler import DocumentAssembler

    global CopyStrategy
    from pdftools_sdk.document_assembly.copy_strategy import CopyStrategy
    global RemovalStrategy
    from pdftools_sdk.document_assembly.removal_strategy import RemovalStrategy
    global NamedDestinationCopyStrategy
    from pdftools_sdk.document_assembly.named_destination_copy_strategy import NamedDestinationCopyStrategy
    global NameConflictResolution
    from pdftools_sdk.document_assembly.name_conflict_resolution import NameConflictResolution
    global PageRotation
    from pdftools_sdk.document_assembly.page_rotation import PageRotation


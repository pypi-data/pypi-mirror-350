def _import_types():
    global Profile
    from pdftools_sdk.optimization.profiles.profile import Profile
    global Web
    from pdftools_sdk.optimization.profiles.web import Web
    global Print
    from pdftools_sdk.optimization.profiles.print import Print
    global Archive
    from pdftools_sdk.optimization.profiles.archive import Archive
    global MinimalFileSize
    from pdftools_sdk.optimization.profiles.minimal_file_size import MinimalFileSize
    global Mrc
    from pdftools_sdk.optimization.profiles.mrc import Mrc


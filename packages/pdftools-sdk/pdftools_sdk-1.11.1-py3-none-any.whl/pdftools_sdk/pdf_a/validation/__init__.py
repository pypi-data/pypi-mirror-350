def _import_types():
    global Validator
    from pdftools_sdk.pdf_a.validation.validator import Validator
    global ValidationOptions
    from pdftools_sdk.pdf_a.validation.validation_options import ValidationOptions
    global ValidationResult
    from pdftools_sdk.pdf_a.validation.validation_result import ValidationResult
    global AnalysisOptions
    from pdftools_sdk.pdf_a.validation.analysis_options import AnalysisOptions
    global AnalysisResult
    from pdftools_sdk.pdf_a.validation.analysis_result import AnalysisResult

    global ErrorCategory
    from pdftools_sdk.pdf_a.validation.error_category import ErrorCategory


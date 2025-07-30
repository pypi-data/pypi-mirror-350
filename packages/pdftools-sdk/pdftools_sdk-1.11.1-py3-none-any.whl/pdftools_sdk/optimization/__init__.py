import pdftools_sdk.optimization.profiles

def _import_types():
    global ImageRecompressionOptions
    from pdftools_sdk.optimization.image_recompression_options import ImageRecompressionOptions
    global FontOptions
    from pdftools_sdk.optimization.font_options import FontOptions
    global RemovalOptions
    from pdftools_sdk.optimization.removal_options import RemovalOptions
    global Optimizer
    from pdftools_sdk.optimization.optimizer import Optimizer

    global ConversionStrategy
    from pdftools_sdk.optimization.conversion_strategy import ConversionStrategy
    global RemovalStrategy
    from pdftools_sdk.optimization.removal_strategy import RemovalStrategy
    global CompressionAlgorithmSelection
    from pdftools_sdk.optimization.compression_algorithm_selection import CompressionAlgorithmSelection

    pdftools_sdk.optimization.profiles._import_types()


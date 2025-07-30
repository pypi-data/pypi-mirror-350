import pdftools_sdk.pdf2_image.profiles

def _import_types():
    global ContentOptions
    from pdftools_sdk.pdf2_image.content_options import ContentOptions
    global ImageOptions
    from pdftools_sdk.pdf2_image.image_options import ImageOptions
    global FaxImageOptions
    from pdftools_sdk.pdf2_image.fax_image_options import FaxImageOptions
    global TiffJpegImageOptions
    from pdftools_sdk.pdf2_image.tiff_jpeg_image_options import TiffJpegImageOptions
    global TiffLzwImageOptions
    from pdftools_sdk.pdf2_image.tiff_lzw_image_options import TiffLzwImageOptions
    global TiffFlateImageOptions
    from pdftools_sdk.pdf2_image.tiff_flate_image_options import TiffFlateImageOptions
    global PngImageOptions
    from pdftools_sdk.pdf2_image.png_image_options import PngImageOptions
    global JpegImageOptions
    from pdftools_sdk.pdf2_image.jpeg_image_options import JpegImageOptions
    global ImageSectionMapping
    from pdftools_sdk.pdf2_image.image_section_mapping import ImageSectionMapping
    global RenderPageAsFax
    from pdftools_sdk.pdf2_image.render_page_as_fax import RenderPageAsFax
    global RenderPageAtResolution
    from pdftools_sdk.pdf2_image.render_page_at_resolution import RenderPageAtResolution
    global RenderPageToMaxImageSize
    from pdftools_sdk.pdf2_image.render_page_to_max_image_size import RenderPageToMaxImageSize
    global Converter
    from pdftools_sdk.pdf2_image.converter import Converter

    global FaxVerticalResolution
    from pdftools_sdk.pdf2_image.fax_vertical_resolution import FaxVerticalResolution
    global TiffBitonalCompressionType
    from pdftools_sdk.pdf2_image.tiff_bitonal_compression_type import TiffBitonalCompressionType
    global BackgroundType
    from pdftools_sdk.pdf2_image.background_type import BackgroundType
    global PngColorSpace
    from pdftools_sdk.pdf2_image.png_color_space import PngColorSpace
    global JpegColorSpace
    from pdftools_sdk.pdf2_image.jpeg_color_space import JpegColorSpace
    global ColorSpace
    from pdftools_sdk.pdf2_image.color_space import ColorSpace
    global AnnotationOptions
    from pdftools_sdk.pdf2_image.annotation_options import AnnotationOptions

    pdftools_sdk.pdf2_image.profiles._import_types()


from .pdf_mark_image_model import PdfMarkImageModel
from .pades_visual_rectangle_model import PadesVisualRectangleModel
from .pdf_mark_element_type import PdfMarkElementType
from .pdf_mark_element_model import PdfMarkElementModel
from .pdf_text_style import PdfTextStyle
from .pdf_container_definition import PdfContainerDefinition
from .pdf_text_section_model import PdfTextSectionModel
from .pdf_mark_model import PdfMarkModel

class PdfHelper(object):

    @staticmethod
    def mark():
        return PdfMarkModel(
            container=PadesVisualRectangleModel(), 
            elements=list()
        )

    @staticmethod
    def container():
        return PdfContainerDefinition.Initial()

    @staticmethod
    def text_element():
        return PdfMarkElementModel(
            elementType=PdfMarkElementType.TEXT,
            textSections=list()
        )

    @staticmethod
    def image_element():
        return PdfMarkElementModel(
            elementType=PdfMarkElementType.IMAGE,
            image=PdfMarkImageModel()
            )

    @staticmethod
    def qr_code_element():
        return PdfMarkElementModel(elementType=PdfMarkElementType.QRCODE)

    @staticmethod
    def text_section():
        return PdfTextSectionModel(text="TEXT SECTION")

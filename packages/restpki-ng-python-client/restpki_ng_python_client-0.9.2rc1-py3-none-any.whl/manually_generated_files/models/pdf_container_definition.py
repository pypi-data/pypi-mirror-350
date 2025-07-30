from .pades_visual_rectangle_model import PadesVisualRectangleModel


class PdfContainerDefinition:

    class VarWidthAndHeight:

        def __init__(self, container: PadesVisualRectangleModel):
            self.__container = container

        def margins(self,
                    top_margin,
                    right_margin=None,
                    bottom_margin=None,
                    left_margin=None):
            self.__container.top = top_margin
            self.__container.right = right_margin \
                if right_margin is not None else top_margin
            self.__container.bottom = bottom_margin \
                if bottom_margin is not None else top_margin
            self.__container.left = left_margin \
                if left_margin is not None else self.__container.right
            return self.__container

    class HeightDefinedVarWidth:

        def __init__(self, container: PadesVisualRectangleModel):
            self.__container = container

        def margins(self, left_margin, right_margin=None):
            self.__container.left = left_margin
            self.__container.right = right_margin \
                if right_margin is not None else left_margin
            return self.__container

    class HeightDefinedFixedWidth:

        def __init__(self, container: PadesVisualRectangleModel):
            self.__container = container

        def anchor_left(self, margin=0.0):
            self.__container.left = margin
            return self.__container

        def anchor_right(self, margin=0.0):
            self.__container.right = margin
            return self.__container

        def center(self):
            return self.__container

    class WidthDefinedVarHeight:

        def __init__(self, container: PadesVisualRectangleModel):
            self.__container = container

        def margins(self, top_margin, bottom_margin=None):
            self.__container.top = top_margin
            self.__container.bottom = bottom_margin \
                if bottom_margin is not None else top_margin
            return self.__container

    class WidthDefinedFixedHeight:

        def __init__(self, container: PadesVisualRectangleModel):
            self.__container = container

        def anchor_top(self, margin=0.0):
            self.__container.top = margin
            return self.__container

        def anchor_bottom(self, margin=0.0):
            self.__container.bottom = margin
            return self.__container

        def center(self):
            return self.__container

    class HeightDefined:

        def __init__(self, container: PadesVisualRectangleModel):
            self.__container = container

        def width(self, value):
            self.__container.width = value
            return PdfContainerDefinition.\
                HeightDefinedFixedWidth(self.__container)

        def var_width(self):
            return PdfContainerDefinition.\
                HeightDefinedVarWidth(self.__container)

        def full_width(self):
            self.__container.left = 0.0
            self.__container.right = 0.0
            return self.__container

    class WidthDefined:

        def __init__(self, container: PadesVisualRectangleModel):
            self.__container = container

        def height(self, value):
            self.__container.height = value
            return PdfContainerDefinition.\
                WidthDefinedFixedHeight(self.__container)

        def var_height(self):
            return PdfContainerDefinition.\
                WidthDefinedVarHeight(self.__container)

        def full_height(self):
            self.__container.top = 0.0
            self.__container.bottom = 0.0
            return self.__container

    class VarHeight:

        def __init__(self, container: PadesVisualRectangleModel):
            self.__container = container

        def margins(self, top_margin, bottom_margin=None):
            self.__container.top = top_margin
            self.__container.bottom = bottom_margin \
                if bottom_margin is not None else top_margin
            return PdfContainerDefinition.HeightDefined(self.__container)

    class FixedHeight:

        def __init__(self, container: PadesVisualRectangleModel):
            self.__container = container

        def anchor_top(self, margin=0.0):
            self.__container.top = margin
            return PdfContainerDefinition.HeightDefined(self.__container)

        def anchor_bottom(self, margin=0.0):
            self.__container.bottom = margin
            return PdfContainerDefinition.HeightDefined(self.__container)

        def center(self):
            return PdfContainerDefinition.HeightDefined(self.__container)

    class VarWidth:

        def __init__(self, container: PadesVisualRectangleModel):
            self.__container = container

        def margins(self, left_margin, right_margin=None):
            self.__container.left = left_margin
            self.__container.right = right_margin \
                if right_margin is not None else left_margin
            return PdfContainerDefinition.WidthDefined(self.__container)

    class FixedWidth:

        def __init__(self, container: PadesVisualRectangleModel):
            self.__container = container

        def anchor_left(self, margin=0.0):
            self.__container.left = margin
            return PdfContainerDefinition.WidthDefined(self.__container)

        def anchor_right(self, margin=0.0):
            self.__container.right = margin
            return PdfContainerDefinition.WidthDefined(self.__container)

        def center(self):
            return PdfContainerDefinition.WidthDefined(self.__container)

    class Initial:

        def __init__(self):
            self.__container = PadesVisualRectangleModel()

        def width(self, value):
            self.__container.width = value
            return PdfContainerDefinition.FixedWidth(self.__container)

        def var_width(self):
            return PdfContainerDefinition.VarWidth(self.__container)

        def full_width(self):
            self.__container.left = 0.0
            self.__container.right = 0.0
            return PdfContainerDefinition.WidthDefined(self.__container)

        def height(self, value):
            self.__container.height = value
            return PdfContainerDefinition.FixedHeight(self.__container)

        def var_height(self):
            return PdfContainerDefinition.VarHeight(self.__container)

        def full_height(self):
            self.__container.top = 0.0
            self.__container.bottom = 0.0
            return PdfContainerDefinition.HeightDefined(self.__container)

        def var_width_and_height(self):
            return PdfContainerDefinition.VarWidthAndHeight(self.__container)

        def full(self):
            self.__container.top = 0.0
            self.__container.right = 0.0
            self.__container.bottom = 0.0
            self.__container.left = 0.0
            return self.__container

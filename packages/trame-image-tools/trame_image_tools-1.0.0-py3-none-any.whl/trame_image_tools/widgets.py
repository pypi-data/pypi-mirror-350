from trame_client.widgets.core import AbstractElement

from trame_image_tools import module

__all__ = ["TrameImage", "TrameImageRoi"]


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)


class TrameImage(HtmlElement):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            "trame-image",
            **kwargs,
        )

        named_models = [
            "scale",
            "center",
        ]

        self._attr_names += [
            "src",
            "size",
            ("border_color", "borderColor"),
            ("border_size", "borderSize"),
            *named_models,
        ]

        self._event_names += []

        for named_model in named_models:
            if isinstance(named_model, tuple):
                python_name, js_name = named_model
            else:
                python_name = named_model
                js_name = named_model

            self._attr_names.append((f"v_model_{python_name}", f"v-model:{js_name}"))

            self._event_names.append((f"update_{python_name}", f"update:{js_name}"))

        slot_props = [
            "imageSize",
            "viewPortSize",
            "imageRatio",
            "viewPortRatio",
            "widthRatio",
            "heightRatio",
            "pixelRatio",
            "viewBox",
            "center",
            "scale",
        ]
        self._attributes["slot"] = f'v-slot="{{ { ", ".join(slot_props) } }}"'


class TrameImageInnerWidget(HtmlElement):
    def __init__(self, tag_name, **kwargs):
        super().__init__(
            tag_name,
            image_size=("imageSize",),
            viewport_size=("viewPortSize",),
            image_ratio=("imageRatio",),
            view_port_ratio=("viewPortRatio",),
            width_ratio=("widthRatio",),
            height_ratio=("heightRatio",),
            pixel_ratio=("pixelRatio",),
            view_box=("viewBox",),
            center=("center",),
            scale=("scale",),
            **kwargs,
        )

        self._attr_names += [
            ("image_size", "imageSize"),
            ("viewport_size", "viewPortSize"),
            ("image_ratio", "imageRatio"),
            ("view_port_ratio", "viewPortRatio"),
            ("width_ratio", "widthRatio"),
            ("height_ratio", "heightRatio"),
            ("pixel_ratio", "pixelRatio"),
            ("view_box", "viewBox"),
            "center",
            "scale",
        ]


class TrameImageRoi(TrameImageInnerWidget):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            "trame-image-roi",
            **kwargs,
        )

        self._attr_names += [
            ("border_color", "borderColor"),
            ("border_size", "borderSize"),
            ("fill_color", "fillColor"),
            ("handle_size", "handleSize"),
            ("handle_fill_color", "handleFillColor"),
            ("handle_border_color", "handleBorderColor"),
            ("handle_border_size", "handleBorderSize"),
            ("v_model", "v-model"),
            ("model_value", "modelValue"),
        ]

        self._event_names += [
            ("update_model_value", "update:modelValue"),
        ]


class TrameImageLine(TrameImageInnerWidget):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            "trame-image-line",
            **kwargs,
        )

        self._attr_names += [
            "color",
            "thickness",
            ("handle_size", "handleSize"),
            ("handle_fill_color", "handleFillColor"),
            ("handle_border_color", "handleBorderColor"),
            ("handle_border_size", "handleBorderSize"),
            ("v_model", "v-model"),
            ("model_value", "modelValue"),
        ]

        self._event_names += [
            ("update_model_value", "update:modelValue"),
        ]


class TrameImageCircle(TrameImageInnerWidget):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            "trame-image-circle",
            **kwargs,
        )

        self._attr_names += [
            ("border_color", "borderColor"),
            ("border_size", "borderSize"),
            ("fill_color", "fillColor"),
            ("handle_size", "handleSize"),
            ("handle_fill_color", "handleFillColor"),
            ("handle_border_color", "handleBorderColor"),
            ("handle_border_size", "handleBorderSize"),
            ("v_model", "v-model"),
            ("model_value", "modelValue"),
        ]

        self._event_names += [
            ("update_model_value", "update:modelValue"),
        ]


class TrameImagePolygon(TrameImageInnerWidget):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            "trame-image-polygon",
            **kwargs,
        )

        self._attr_names += [
            ("border_color", "borderColor"),
            ("border_size", "borderSize"),
            ("fill_color", "fillColor"),
            ("handle_size", "handleSize"),
            ("handle_fill_color", "handleFillColor"),
            ("handle_border_color", "handleBorderColor"),
            ("handle_border_size", "handleBorderSize"),
            ("v_model", "v-model"),
            ("model_value", "modelValue"),
        ]

        self._event_names += [
            ("update_model_value", "update:modelValue"),
        ]


class TrameImageGrid(TrameImageInnerWidget):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            "trame-image-grid",
            **kwargs,
        )

        self._attr_names += [
            "spacing",
            "color",
            "thickness",
            ("font_family", "fontFamily"),
            ("font_size", "fontSize"),
        ]

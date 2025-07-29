import dataclasses as dc
from ..enum.vis_enums import *
from typing import Tuple, Optional


@dc.dataclass
class Field:
    """
    The field controls the field displayed on the object. If the field doesn't
    exist, we show a solid color.

    .. warning:: This feature is experimental and may change or be removed in the future.

    """

    quantity: VisQuantity = VisQuantity.ABSOLUTE_PRESSURE
    """The quantity to color by."""
    component: FieldComponent = FieldComponent.X
    """
    The component of the field to use, applicable to vector fields. If the field is a
    scalar, use the default X component.
    """

    def __hash__(self) -> int:
        return hash((self.quantity, self.component))


@dc.dataclass
class DisplayAttributes:
    """
    Display attributes specify how objects such as meshes, geometries, and
    filters appear in the scene.

    .. warning:: This feature is experimental and may change or be removed in the future.

    """

    visible: bool = True
    """If the object is visible or not. Default: True"""
    # TODO(matt): opacity not hooked up yet.
    opacity: float = 1.0
    """
    How opaque the object is. This is a normalized number between
    0 (i.e., fully transparent) and 1 (i.e., fully opaque). Default: 1
    """
    field: Field = dc.field(default_factory=Field)
    """What field quantity/component to color by, if applicable."""
    representation: Representation = Representation.SURFACE
    """
    how the object is represented in the scene (e.g., surface, surface with
    edges, wireframe or points). Default: surface.
    """

    def _to_proto(self) -> vis_pb2.DisplayAttributes:
        attrs = vis_pb2.DisplayAttributes()
        attrs.visible = self.visible
        attrs.representation = self.representation.value
        attrs.field.component = self.field.component.value
        attrs.field.quantity_typ = self.field.quantity.value
        return attrs


@dc.dataclass
class DataRange:
    """
    The data range represents a range of values. Ranges are only valid if the
    max value is greater than the or equal to the min_value. The default is
    invalid.

    .. warning:: This feature is experimental and may change or be removed in the future.

    """

    min_value: float = float("inf")
    """The minimum value of the range."""
    max_value: float = float("-inf")
    """The maximum value of the range."""

    def is_valid(self) -> bool:
        return self.max_value >= self.min_value


@dc.dataclass
class ColorMapAppearance:
    """
    ColorMapAppearance controls how the color maps appear in the image, including
    visibility, position and size.

    The width, height, and the lower left position of the color map are
    specified in normalized device coordinates. These are values in the [0,1]
    range. For example, the lower left hand coordinate of the image is [0,0], and the
    top right coordinate of the image is [1,1].

    .. warning:: This feature is experimental and may change or be removed in the future.

    """

    visible: bool = True
    """Controls if the color map is displayed or not. Default: True"""
    width: float = 0.034
    """The width of the color map in normalized device coordinates. Default: 0.034"""
    height: float = 0.146
    """The height of the color map in normalized device coordinates. Default: 0.146"""
    text_size: int = 36
    """The text size for the color map legend in pixels. Default: 36"""
    lower_left_x: float = 0.8
    """
    The lower left x position of the color map in normalized device
    coordinates. Default: 0.8
    """
    lower_left_y: float = 0.8
    """
    The lower left y position of the color map in normalized device
    coordinates. Default: 0.8
    """


@dc.dataclass
class ColorMap:
    """
    The color map allows user control over how field values are mapped to
    colors. Color maps are assigned to fields (e.g., the quantity and component)
    and not individual display attributes. This means that there can only ever
    be one color map per field/component combination (e.g., velocity-magnitude
    or velocity-x). Any display attribute in the scene (i.e., filter display
    attributes or global display attributes) that maps to this color map will be
    color in the same manner.

    .. warning:: This feature is experimental and may change or be removed in the future.

    """

    field: Field = dc.field(default_factory=Field)
    """The field and component this color map applies to."""
    preset: ColorMapPreset = ColorMapPreset.JET
    """
    The color map preset to use. This defines the colors used in the color
    map. Default is 'JET'.
    """
    data_range: DataRange = dc.field(default_factory=DataRange)
    """
    An optional data range to use for the color map. The user must explicity
    set the data ranges. If not set explicitly, the fields global data range
    is used. For comparing multiple results, either with different solutions
    in the same simulation or with different simulations, its highly
    recommended that a range is provided so the color scales are the same
    between the resulting images. Default: is an invalid data range.
    """
    discretize: bool = False
    """
    Use discrete color bins instead of a continuous range. When True,
    'n_colors' indicates how many discrete bins to use. Default: False.
    """
    n_colors: int = 8
    """
    How many discrete bins to use when discretize is True. Valid n_colors
    values are [1, 256]. Default: 8.
    """
    appearance: Optional[ColorMapAppearance] = None
    """
    This attribute controls how the color map annotation appears in the image, including
    location, size, and visibility. When the scene is set to automatic color maps, these
    attributes are automatically populated unless overridden. When setting the appearance,
    the user is responsible for setting all values.
    """

    def _to_proto(self) -> vis_pb2.ColorMap:
        res: vis_pb2.ColorMap = vis_pb2.ColorMap()
        res.field.component = self.field.component.value
        res.field.quantity_typ = self.field.quantity.value
        res.name = self.preset.value
        res.discretize = self.discretize
        res.n_colors = self.n_colors
        if self.data_range.is_valid():
            res.range.max = self.data_range.max_value
            res.range.min = self.data_range.min_value

        if not self.appearance:
            res.visible = True
        elif not isinstance(self.appearance, ColorMapAppearance):
            raise TypeError(f"Expected 'ColorMapAppearance', got {type(self.appearance).__name__}")
        else:
            res.visible = self.appearance.visible
            res.width = self.appearance.width
            res.height = self.appearance.height
            res.lower_left_anchor_location.x = self.appearance.lower_left_x
            res.lower_left_anchor_location.y = self.appearance.lower_left_y
            res.text_size = self.appearance.text_size
        return res

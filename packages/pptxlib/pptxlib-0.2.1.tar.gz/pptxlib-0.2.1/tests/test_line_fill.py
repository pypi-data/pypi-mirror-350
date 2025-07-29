import pytest
from win32com.client import constants

from pptxlib.app import is_app_available
from pptxlib.shape import Line, Shape, Shapes

pytestmark = pytest.mark.skipif(
    not is_app_available(),
    reason="PowerPoint is not available",
)


@pytest.fixture
def shape(shapes: Shapes):
    shape = shapes.add("Oval", 100, 100, 40, 60)
    yield shape
    shape.delete()


def test_color_fill(shape: Shape):
    shape.fill.color = (0, 255, 0)
    assert shape.fill.color == 255 * 256


def test_color_line(shape: Shape):
    shape.line.color = (0, 0, 255)
    assert shape.line.color == 256 * 256 * 255


def test_alpha(shape: Shape):
    shape.line.alpha = 0.5
    assert shape.line.alpha == 0.5


def test_weight(shape: Shape):
    shape.line.weight = 2
    assert shape.line.weight == 2


def test_set_fill(shape: Shape):
    x = shape.fill.set(color="red", alpha=0.2)
    assert x.color == 255
    assert 0.199 < x.alpha <= 0.2


def test_set_fill_visible(shape: Shape):
    x = shape.fill.set(visible=False)
    assert x.visible is False


def test_set_line(shape: Shape):
    x = shape.line.set(color="red", alpha=0.2, weight=3)
    assert x.color == 255
    assert 0.199 < x.alpha <= 0.2
    assert x.weight == 3


def test_update_fill(shape: Shape, shapes: Shapes):
    x = shape.fill.set(color="blue", alpha=0.5)
    shape = shapes.add("Rectangle", 100, 100, 40, 60)
    shape.fill.update(x)
    assert shape.fill.color == 256 * 256 * 255
    assert shape.fill.alpha == 0.5
    shape.delete()


def test_update_line(shape: Shape, shapes: Shapes):
    x = shape.line.set(color="blue", alpha=0.5, weight=4)
    shape = shapes.add("Rectangle", 100, 100, 40, 60)
    shape.line.update(x)
    assert shape.line.color == 256 * 256 * 255
    assert shape.line.alpha == 0.5
    assert shape.line.weight == 4
    shape.delete()


@pytest.fixture
def line(shapes: Shapes):
    shape = shapes.add_line(10, 20, 140, 160)
    yield shape.line
    shape.delete()


def test_line_dash(line: Line):
    line.dash("DashDot")
    assert line.dash_style == constants.msoLineDashDot


def test_line_arrow(line: Line):
    line.begin_arrow("Open", "Long", "Wide")
    assert line.begin_arrowhead_style == constants.msoArrowheadOpen
    assert line.begin_arrowhead_length == constants.msoArrowheadLong
    assert line.begin_arrowhead_width == constants.msoArrowheadWide

    line.end_arrow("Stealth", "Short", "Narrow")
    assert line.end_arrowhead_style == constants.msoArrowheadStealth
    assert line.end_arrowhead_length == constants.msoArrowheadShort
    assert line.end_arrowhead_width == constants.msoArrowheadNarrow

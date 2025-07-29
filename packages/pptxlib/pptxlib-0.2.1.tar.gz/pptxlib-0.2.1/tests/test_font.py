import pytest

from pptxlib.app import is_app_available
from pptxlib.font import Font
from pptxlib.presentation import Presentations
from pptxlib.shape import Shape, Shapes

pytestmark = pytest.mark.skipif(
    not is_app_available(),
    reason="PowerPoint is not available",
)


@pytest.fixture(scope="module")
def shape(prs: Presentations):
    pr = prs.add()
    slide = pr.slides.add()
    yield slide.shapes[0]
    pr.delete()


@pytest.fixture
def font(shape: Shape):
    return shape.font


def test_repr(font: Font):
    assert repr(font).startswith("<Font '")


def test_name(font: Font):
    font.name = "Meiryo"
    assert font.name == "Meiryo"


def test_size(font: Font):
    font.size = 32
    assert font.size == 32


def test_bold(font: Font):
    font.bold = True
    assert font.bold is True
    font.bold = False
    assert font.bold is False


def test_italic(font: Font):
    font.italic = True
    assert font.italic is True
    font.italic = False
    assert font.italic is False


def test_color(font: Font):
    font.color = (255, 0, 0)
    assert font.color == 255
    font.color = "green"
    assert font.color == 32768


def test_set(font: Font):
    font.set(
        name="Meiryo",
        size=32,
        bold=True,
        italic=True,
        color="green",
    )
    assert font.name == "Meiryo"
    assert font.size == 32
    assert font.bold is True
    assert font.italic is True
    assert font.color == 32768


def test_update(font: Font, shapes: Shapes):
    shape = shapes.add_label("text", 100, 100)
    font.set(
        name="Meiryo",
        size=12,
        bold=False,
        italic=True,
        color="red",
    )
    shape.font.update(font)
    assert shape.font.name == "Meiryo"
    assert shape.font.size == 12
    assert shape.font.bold is False
    assert shape.font.italic is True
    assert shape.font.color == 255
    shape.delete()

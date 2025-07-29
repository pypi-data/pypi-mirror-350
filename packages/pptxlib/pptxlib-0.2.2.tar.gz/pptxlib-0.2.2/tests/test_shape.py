from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import PIL.Image
import pytest
from win32com.client import DispatchBaseClass

from pptxlib.app import is_app_available
from pptxlib.base import Collection, Element
from pptxlib.shape import Shape, ShapeRange, Shapes
from pptxlib.slide import Slide
from pptxlib.table import Table

pytestmark = pytest.mark.skipif(
    not is_app_available(),
    reason="PowerPoint is not available",
)


def test_shapes(shapes: Shapes):
    assert isinstance(shapes, Collection)
    assert isinstance(shapes, Shapes)
    assert isinstance(shapes.api, DispatchBaseClass)


def test_shapes_repr(shapes: Shapes):
    assert repr(shapes).startswith("<Shapes")


@pytest.fixture
def shape(shapes: Shapes):
    return shapes[0]


def test_select(shape: Shape):
    rng = shape.select()
    assert isinstance(rng, ShapeRange)
    assert rng.parent is shape.parent
    assert rng.collection is shape.collection


def test_title(shapes: Shapes, shape: Shape):
    assert shapes.title.name == shape.name


def test_shape(shape: Shape):
    assert isinstance(shape, Element)
    assert isinstance(shape, Shape)
    assert isinstance(shape.api, DispatchBaseClass)


def test_text_range(shape: Shape):
    assert isinstance(shape.text_range, DispatchBaseClass)


def test_text(shape: Shape):
    assert shape.text == ""
    shape.text = "Title"
    assert shape.text == "Title"


def test_parent(slide: Slide):
    shape = slide.shapes.add("Oval", 100, 100, 40, 60)
    assert shape.parent is slide
    shape.delete()


def test_left(shape: Shape):
    shape.left = 50
    assert shape.left == 50


def test_left_center(shape: Shape, slide: Slide):
    shape.left = "center"
    assert round(shape.left + shape.width / 2) == round(slide.width / 2)  # type: ignore


def test_left_neg(shape: Shape, slide: Slide):
    shape.left = -50
    assert round(shape.left + shape.width) == round(slide.width - 50)


def test_top(shape: Shape):
    shape.top = 50
    assert shape.top == 50


def test_top_center(shape: Shape, slide: Slide):
    shape.top = "center"
    assert round(shape.top + shape.height / 2) == round(slide.height / 2)  # type: ignore


def test_top_neg(shape: Shape, slide: Slide):
    shape.top = -100
    assert round(shape.top + shape.height) == round(slide.height - 100)


def test_width(shape: Shape):
    assert shape.width > 0
    shape.width = 250
    assert shape.width == 250


def test_height(shape: Shape):
    assert shape.height > 0
    shape.height = 250
    assert shape.height == 250


def test_add(shapes: Shapes):
    shape = shapes.add("Oval", 100, 100, 40, 60)
    assert shape.text == ""
    assert shape.left == 100
    assert shape.top == 100
    assert shape.width == 40
    assert shape.height == 60
    assert shape.api.Parent.__class__.__name__ == "_Slide"
    assert shape.parent.__class__.__name__ == "Slide"
    shape.delete()


def test_add_label(shapes: Shapes):
    shape = shapes.add_label("ABC", 100, 100)
    assert shape.text == "ABC"
    assert shape.left == 100
    assert shape.top == 100
    width = shape.width
    height = shape.height
    shape.text = "ABC ABC"
    assert width < shape.width
    assert height == shape.height
    assert shape.api.Parent.__class__.__name__ == "_Slide"
    assert shape.parent.__class__.__name__ == "Slide"
    shape.delete()


def test_add_label_auto_size_false(shapes: Shapes):
    shape = shapes.add_label("ABC", 100, 100, 200, 300, auto_size=False)
    assert shape.width == 200
    assert shape.height == 300
    shape.delete()


def test_add_table(shapes: Shapes):
    table = shapes.add_table(2, 3, 100, 100, 240, 360)
    assert isinstance(table, Table)
    table.delete()


def test_shape_oval_repr(shapes: Shapes):
    shape = shapes.add("Oval", 100, 100, 40, 60)
    assert repr(shape).startswith("<Shape [Oval")
    shape.delete()


def test_shapes_parent(shapes: Shapes):
    assert shapes.api.Parent.__class__.__name__ == "_Slide"
    assert shapes.parent.__class__.__name__ == "Slide"


def test_shape_parent(shape: Shape, shapes: Shapes):
    assert shape.api.Parent.__class__.__name__ == "_Slide"
    assert shape.parent.__class__.__name__ == "Slide"
    assert shapes[0].parent.__class__.__name__ == "Slide"


@pytest.fixture(scope="module")
def image():
    array = np.random.randint(0, 255, (200, 100, 3), dtype=np.uint8)  # noqa: NPY002
    return PIL.Image.fromarray(array)


def test_add_image(shapes: Shapes, image: PIL.Image.Image):
    shape = shapes.add_image(image, 20, 30)
    assert shape.left == 20
    assert shape.top == 30
    assert shape.width == image.width * 0.75
    assert shape.height == image.height * 0.75


def test_add_image_scale(shapes: Shapes, image: PIL.Image.Image):
    shape = shapes.add_image(image, scale=2)
    assert shape.width == image.width * 0.75 * 2
    assert shape.height == image.height * 0.75 * 2


def test_add_figure(shapes: Shapes):
    fig, ax = plt.subplots(figsize=(2, 1), dpi=100)
    ax.plot([1, 2, 3, 4, 5])
    s1 = shapes.add_figure(fig)
    s2 = shapes.add_figure(fig, dpi=300)
    assert abs(s1.width - s2.width) < 1
    assert abs(s1.height - s2.height) < 1


def test_paste(shapes: Shapes, image: PIL.Image.Image):
    shape = shapes.add_image(image, 20, 30)
    shape.copy()
    s = shapes.paste(20, 100, 200)
    assert round(s.left) == 20
    assert round(s.top) == 100
    assert round(s.width) == 200
    assert round(s.height) == 400
    s = shapes.paste(20, 100, height=200)
    assert round(s.left) == 20
    assert round(s.top) == 100
    assert round(s.width) == 100
    assert round(s.height) == 200


def test_paste_special(shapes: Shapes, image: PIL.Image.Image):
    shape = shapes.add_image(image, 20, 30)
    shape.copy()
    s = shapes.paste_special("GIF", 20, 100, 200)
    assert round(s.left) == 20
    assert round(s.top) == 100
    assert round(s.width) == 200
    assert round(s.height) == 400
    s = shapes.paste_special("PNG", 20, 100, height=200)
    assert round(s.left) == 20
    assert round(s.top) == 100
    assert round(s.width) == 100
    assert round(s.height) == 200


def test_png(shapes: Shapes, tmp_path: Path):
    shape = shapes.add("Rectangle", 100, 100, 100, 100)
    data = shape.png()
    assert data.startswith(b"\x89PNG")
    path = tmp_path.joinpath("a.png")
    path.write_bytes(data)
    image = PIL.Image.open(path)
    assert image.size == (136, 136)


def test_svg(shapes: Shapes):
    shape = shapes.add("Rectangle", 100, 100, 100, 100)
    text = shape.svg()
    assert text.startswith('<svg width="136" height="136"')


@pytest.fixture
def rng(shapes: Shapes):
    s1 = shapes.add("Rectangle", 100, 100, 100, 100)
    s2 = shapes.add("Oval", 150, 150, 90, 80)
    return shapes.range([s1, s2])


def test_range_repr(rng: ShapeRange):
    assert repr(rng).startswith("<ShapeRange [2]")


def test_range_png(rng: ShapeRange, tmp_path: Path):
    data = rng.png()
    assert data.startswith(b"\x89PNG")
    path = tmp_path.joinpath("a.png")
    path.write_bytes(data)
    image = PIL.Image.open(path)
    assert image.size == (189, 176)


def test_range_svg(rng: ShapeRange):
    text = rng.svg()
    assert "<rect x=" in text
    assert "<path d=" in text


def test_select_unselect(shapes: Shapes):
    s1 = shapes.add("Rectangle", 100, 100, 100, 100)
    s2 = shapes.add("Oval", 150, 150, 90, 80)
    s1.select()
    rng = s2.select(replace=False)
    rng.app.unselect()
    rng.fill.set(color="red", alpha=0.5)
    assert s1.fill.color == 255
    assert s1.fill.alpha == 0.5
    assert s2.fill.color == 255
    assert s2.fill.alpha == 0.5

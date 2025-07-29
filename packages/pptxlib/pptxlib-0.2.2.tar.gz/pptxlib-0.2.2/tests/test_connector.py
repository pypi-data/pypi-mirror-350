import pytest

from pptxlib.app import is_app_available
from pptxlib.shape import Shapes

pytestmark = pytest.mark.skipif(
    not is_app_available(),
    reason="PowerPoint is not available",
)


def test_horizontal(shapes: Shapes):
    s1 = shapes.add("Oval", 100, 100, 40, 50)
    s2 = shapes.add("Oval", 200, 200, 60, 70)
    s3 = s1.connect(s2)
    assert s3.top == 125
    assert s3.left == 140
    assert s3.width == 60
    assert s3.height == 110
    s3 = s2.connect(s1)
    assert s3.top == 125
    assert s3.left == 140
    assert s3.width == 60
    assert s3.height == 110


def test_vertical(shapes: Shapes):
    s1 = shapes.add("Oval", 100, 100, 40, 50)
    s2 = shapes.add("Oval", 200, 200, 60, 70)
    s3 = s1.connect(s2, direction="vertical")
    assert s3.top == 120
    assert s3.left == 150
    assert s3.width == 50
    assert s3.height == 110
    s3 = s2.connect(s1, direction="vertical")
    assert s3.top == 120
    assert s3.left == 150
    assert s3.width == 50
    assert s3.height == 110


def test_straight_horizontal(shapes: Shapes):
    s1 = shapes.add("Oval", 100, 100, 40, 50)
    s2 = shapes.add("Oval", 200, 80, 60, 90)
    s3 = s1.connect(s2)
    assert "Straight Arrow Connector" in repr(s3)
    assert s3.top == 125
    assert s3.left == 140
    assert s3.width == 60
    assert s3.height == 0
    s3 = s2.connect(s1)
    assert "Straight Arrow Connector" in repr(s3)
    assert s3.top == 125
    assert s3.left == 140
    assert s3.width == 60
    assert s3.height == 0


def test_straight_vertical(shapes: Shapes):
    s1 = shapes.add("Oval", 100, 100, 40, 50)
    s2 = shapes.add("Oval", 80, 200, 80, 60)
    s3 = s1.connect(s2)
    assert "Straight Arrow Connector" in repr(s3)
    assert s3.top == 150
    assert s3.left == 120
    assert s3.width == 0
    assert s3.height == 50
    s3 = s2.connect(s1)
    assert "Straight Arrow Connector" in repr(s3)
    assert s3.top == 150
    assert s3.left == 120
    assert s3.width == 0
    assert s3.height == 50

import pytest

from pptxlib.app import is_app_available
from pptxlib.presentation import Presentations
from pptxlib.table import Cell, Column, Row, Table

pytestmark = pytest.mark.skipif(
    not is_app_available(),
    reason="PowerPoint is not available",
)


@pytest.fixture(scope="module")
def table(prs: Presentations):
    pr = prs.add()
    slide = pr.slides.add()
    shapes = slide.shapes
    table = shapes.add_table(2, 3, 100, 250, 100, 100)
    for i, r in enumerate(table):
        for j, c in enumerate(r):
            c.text = f"{i},{j}"
    yield table
    pr.delete()


def test_shape(table: Table):
    assert table.shape == (2, 3)


def test_cell_row_column(table: Table):
    for i in range(2):
        for j in range(3):
            table.cell(i, j).text = f"{i},{j}"


def test_cell_index(table: Table):
    assert table.cell(0).text == "0,0"
    assert table.cell(1).text == "0,1"
    assert table.cell(2).text == "0,2"
    assert table.cell(3).text == "1,0"
    assert table.cell(4).text == "1,1"
    assert table.cell(5).text == "1,2"


def test_getitem_int(table: Table):
    r = table[0]
    assert isinstance(r, Row)
    assert r[0].text == "0,0"
    assert r[1].text == "0,1"
    assert r[2].text == "0,2"


def test_getitem_tuple_int_int(table: Table):
    c = table[1, 2]
    assert isinstance(c, Cell)
    assert c.text == "1,2"


def test_getitem_tuple_int_slice(table: Table):
    r = table[1, :]
    assert isinstance(r, Row)
    assert len(r) == 3
    assert r[0].text == "1,0"
    assert r[1].text == "1,1"
    assert r[2].text == "1,2"


def test_getitem_tuple_slice_int(table: Table):
    c = table[:, 2]
    assert isinstance(c, Column)
    assert len(c) == 2
    assert c[0].text == "0,2"
    assert c[1].text == "1,2"


def test_fill(table: Table):
    table.fill.set(color="red", alpha=0.5)
    assert table[0, 0].shape.fill.color == 255
    assert table[0, 0].shape.fill.alpha == 0.5


def test_minimize_height(table: Table):
    for r in table.rows:
        r.height = 100
        assert r.height == 100
    for c in table.columns:
        c.width = 200
        assert c.width == 200
    table.minimize_height()
    assert table.rows[0].height < 30
    assert table.rows[1].height < 30


def test_axis_repr(table: Table):
    assert repr(table[0]) == "<Row>"
    assert repr(table[1, :]) == "<Row>"
    assert repr(table[:, 2]) == "<Column>"


def test_rows_height(table: Table):
    table.rows[0].height = 100
    table.rows[1].height = 200
    assert table.rows.height == [100, 200]
    table.rows.height = [80, 90]
    assert table.rows.height == [80, 90]


def test_columns_width(table: Table):
    table.columns[0].width = 100
    table.columns[1].width = 200
    table.columns[2].width = 300
    assert table.columns.width == [100, 200, 300]
    table.columns.width = [70, 80, 90]
    assert table.columns.width == [70, 80, 90]


def test_cell_repr(table: Table):
    assert repr(table.cell(0, 0)) == "<Cell>"


def test_cell_shape_name(table: Table):
    assert table.cell(0, 0).shape.name == ""


def test_borders_row(table: Table):
    b = table.rows[0].borders
    b[0].set(color="red", alpha=0.5)
    assert b["top"].color == 255
    assert b["top"].alpha == 0.5


def test_borders_rows(table: Table):
    b = table.rows.borders
    b[1].set(color="blue", alpha=0.2, weight=3)
    for r in table.rows:
        b = r.borders["left"]
        assert b.color == 255 * 256 * 256
        assert 0.199 <= b.alpha <= 0.2
        assert b.weight == 3


def test_borders_columns(table: Table):
    b = table.columns.borders
    b[2].set(color="red", alpha=0.3, weight=2)
    for r in table.columns:
        b = r.borders["bottom"]
        assert b.color == 255
        assert 0.299 <= b.alpha <= 0.301
        assert b.weight == 2


def test_borders_cell(table: Table):
    b = table[1, 1].borders
    b[3].set(color="red", alpha=0.3, weight=4)
    b = b["right"]
    assert b.color == 255
    assert 0.299 <= b.alpha <= 0.301
    assert b.weight == 4


def test_line_format(table: Table):
    from pptxlib.table import LineFormat

    lf = table[1, 1].borders["top"]
    assert isinstance(lf, LineFormat)
    assert repr(lf) == "<LineFormat>"


def test_reset_style(prs: Presentations):
    pr = prs.add()
    slide = pr.slides.add()
    shapes = slide.shapes
    table = shapes.add_table(2, 3, 100, 250, 100, 100)
    table.reset_style()
    assert table.cell(0, 0).shape.fill.visible is False


def test_text(prs: Presentations):
    pr = prs.add()
    slide = pr.slides.add()
    shapes = slide.shapes
    table = shapes.add_table(2, 5, 100, 250, 100, 100)
    texts = ["a", "a", "a", "b", "b"]
    table.rows[0].text(texts, size=12, bold=True, merge=True)
    assert table.cell(0, 0).text == "a"
    assert table.cell(0, 1).text == "a"
    assert table.cell(0, 2).text == "a"
    assert table.cell(0, 3).text == "b"
    assert table.cell(0, 4).text == "b"

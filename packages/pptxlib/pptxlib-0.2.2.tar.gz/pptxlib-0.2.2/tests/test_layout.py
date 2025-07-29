import pytest

from pptxlib.app import is_app_available
from pptxlib.presentation import Presentation, Presentations
from pptxlib.slide import Layout, Layouts

pytestmark = pytest.mark.skipif(
    not is_app_available(),
    reason="PowerPoint is not available",
)


@pytest.fixture(scope="module")
def pr(prs: Presentations):
    pr = prs.add()
    yield pr
    pr.close()


@pytest.fixture(scope="module")
def layouts(pr: Presentation):
    return pr.layouts


@pytest.fixture(scope="module")
def layout(layouts: Layouts):
    return layouts.add("abc")


def test_layouts_add(layouts: Layouts):
    layout = layouts.add("def")
    assert layout.name == "def"


def test_layouts_get(layouts: Layouts, layout: Layout):
    x = layouts.get("abc")
    assert x
    assert x.name == "abc"
    assert x.api.Name == "abc"


def test_get_api_int(layouts: Layouts):
    assert layouts.get_api(100) == 100


def test_get_api_none(layouts: Layouts):
    assert layouts.get_api(None) == 11


def test_get_api_layout_name(layouts: Layouts, layout: Layout):
    assert layouts.get_api("TitleOnly") == 11


def test_get_api_layout(layouts: Layouts, layout: Layout):
    assert layouts.get_api(layout).Name == "abc"  # type: ignore


def test_get_api_name(layouts: Layouts, layout: Layout):
    assert layouts.get_api("abc").Name == "abc"  # type: ignore


def test_copy_from(layouts: Layouts, pr: Presentation):
    slide = pr.slides.add()
    layout = layouts.copy_from(slide, "ghi")
    assert layout.name == "ghi"
    assert layouts[-1].name == "ghi"

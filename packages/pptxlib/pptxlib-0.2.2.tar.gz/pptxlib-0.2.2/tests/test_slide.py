from pathlib import Path

import PIL.Image
import pytest
from win32com.client import constants

from pptxlib.app import is_app_available
from pptxlib.presentation import Presentations
from pptxlib.slide import Slide, Slides

pytestmark = pytest.mark.skipif(
    not is_app_available(),
    reason="PowerPoint is not available",
)


@pytest.fixture
def slide(slides: Slides):
    return slides.add()


def test_active(slides: Slides):
    slide = slides.add()
    slide.select()
    assert slides.active.name == slide.name
    slide.delete()


def test_width(slide: Slide):
    assert slide.width == 960


def test_height(slide: Slide):
    assert slide.height == 540


def test_title(slides: Slides):
    slide = slides.add()
    slide.title = "Title"
    assert slide.title == "Title"


def test_add_with_layout(slides: Slides):
    slide = slides.add(layout="Blank")
    assert slide.api.Layout == constants.ppLayoutBlank
    slide = slides.add()
    assert slide.api.Layout == constants.ppLayoutBlank


def test_png(prs: Presentations, tmp_path: Path):
    slide = prs.add().size(600, 300).slides.add()
    data = slide.png()
    assert data.startswith(b"\x89PNG")
    path = tmp_path.joinpath("a.png")
    path.write_bytes(data)
    image = PIL.Image.open(path)
    assert image.size == (600 * 4 / 3, 300 * 4 / 3)


def test_set(slide: Slide):
    slide.set(title="Title", layout="TwoColumnText")
    assert slide.title == "Title"
    assert slide.api.Layout == constants.ppLayoutTwoColumnText


def test_set_layout(slides: Slides):
    slide = slides.add(layout="Blank")
    layout = slide.layout
    slide = slides.add(layout="TitleOnly")
    slide.set(layout=layout)
    assert slide.api.Layout == constants.ppLayoutBlank

import pytest


def test_rgb_invalid_format():
    from pptxlib.color import rgb

    with pytest.raises(ValueError):
        rgb("invalid")


def test_rgb_invalid_type():
    from pptxlib.color import rgb

    with pytest.raises(ValueError):
        rgb(None)  # type: ignore

import pytest
from win32com.client import constants

from pptxlib.app import is_app_available

pytestmark = pytest.mark.skipif(
    not is_app_available(),
    reason="PowerPoint is not available",
)


@pytest.fixture(scope="module")
def tlbs():
    from pptxlib.client import iter_typelib_specs

    return list(iter_typelib_specs())


@pytest.mark.parametrize(
    "clsid",
    [
        "{00020813-0000-0000-C000-000000000046}",
        "{2DF8D04C-5BFA-101B-BDE5-00AA0044DE52}",
        "{91493440-5A91-11CF-8700-00AA0060263B}",
    ],
)
def test_iter_typelib_specs(tlbs, clsid):
    clsids = [tlb.clsid for tlb in tlbs]
    assert clsid in clsids


def test_ensure_modules():
    from pptxlib.client import ensure_modules

    ensure_modules()
    assert constants.ppLayoutTitleOnly == 11
    assert constants.msoConnectorStraight == 1

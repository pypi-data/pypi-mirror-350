from plone.dexterity.fti import DexterityFTI

import pytest


@pytest.mark.skip(reason="Only available if plone.app.multilingual is installed")
class TestContentTypeFTI:
    portal_type: str = "LRF"

    @pytest.fixture(autouse=True)
    def _setup(self, portal, get_fti):
        self.portal = portal
        self.fti: DexterityFTI = get_fti(self.portal_type)

    @pytest.mark.parametrize(
        "attr,expected",
        [
            ("title", "LRF"),
            ("global_allow", False),
        ],
    )
    def test_fti(self, attr: str, expected):
        """Test FTI values."""
        fti = self.fti

        assert isinstance(fti, DexterityFTI)
        assert getattr(fti, attr) == expected

    @pytest.mark.parametrize(
        "name,expected",
        [
            ("plone.basic", True),
            ("volto.preview_image_link", True),
            ("plone.categorization", True),
            ("plone.publication", True),
            ("plone.ownership", True),
            ("volto.blocks", True),
            ("plone.constraintypes", True),
            ("plone.namefromtitle", True),
            ("plone.navigationroot", True),
            ("plone.locking", True),
            ("plone.versioning", True),
            ("plone.translatable", True),
        ],
    )
    def test_behavior(self, name: str, expected: bool):
        """Test behavior is present or not."""
        fti = self.fti
        behaviors = fti.behaviors
        assert (name in behaviors) is expected

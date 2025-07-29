from plone.dexterity.fti import DexterityFTI

import pytest


class TestContentTypeFTI:
    portal_type: str = "Person"

    @pytest.fixture(autouse=True)
    def _setup(self, portal, get_fti):
        self.portal = portal
        self.fti: DexterityFTI = get_fti(self.portal_type)

    @pytest.mark.parametrize(
        "attr,expected",
        [
            ("title", "Person"),
            ("klass", "collective.person.content.person.Person"),
            ("global_allow", True),
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
            ("volto.preview_image_link", True),
            ("collective.person.person", True),
            ("collective.contact_behaviors.contact_info", True),
            ("kitconcept.core.additional_contact_info", True),
            ("volto.blocks.editable.layout", True),
            ("plone.namefromtitle", True),
            ("plone.shortname", True),
            ("plone.excludefromnavigation", True),
            ("plone.relateditems", True),
            ("plone.versioning", True),
            ("plone.locking", True),
            ("plone.translatable", True),
        ],
    )
    def test_behavior(self, name: str, expected: bool):
        """Test behavior is present or not."""
        fti = self.fti
        behaviors = fti.behaviors
        assert (name in behaviors) is expected

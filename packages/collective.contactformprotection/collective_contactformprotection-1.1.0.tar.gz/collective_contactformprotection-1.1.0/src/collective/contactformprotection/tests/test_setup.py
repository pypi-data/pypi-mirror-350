"""Setup tests for this package."""

from collective.contactformprotection.testing import (  # noqa: E501
    COLLECTIVE_CONTACTFORMPROTECTION_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from plone.base.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that collective.contactformprotection is properly installed."""

    layer = COLLECTIVE_CONTACTFORMPROTECTION_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if collective.contactformprotection is installed."""
        self.assertTrue(
            self.installer.is_product_installed("collective.contactformprotection")
        )

    def test_browserlayer(self):
        """Test that ICollectiveContactformprotectionLayer is registered."""
        from collective.contactformprotection.interfaces import (
            ICollectiveContactformprotectionLayer,
        )
        from plone.browserlayer import utils

        self.assertIn(ICollectiveContactformprotectionLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):
    layer = COLLECTIVE_CONTACTFORMPROTECTION_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("collective.contactformprotection")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.contactformprotection is cleanly uninstalled."""
        self.assertFalse(
            self.installer.is_product_installed("collective.contactformprotection")
        )

    def test_browserlayer_removed(self):
        """Test that ICollectiveContactformprotectionLayer is removed."""
        from collective.contactformprotection.interfaces import (
            ICollectiveContactformprotectionLayer,
        )
        from plone.browserlayer import utils

        self.assertNotIn(
            ICollectiveContactformprotectionLayer, utils.registered_layers()
        )

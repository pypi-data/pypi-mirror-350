# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from redturtle.scale.testing import REDTURTLE_SCALE_INTEGRATION_TESTING  # noqa: E501

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that redturtle.scale is properly installed."""

    layer = REDTURTLE_SCALE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if redturtle.scale is installed."""
        self.assertTrue(self.installer.is_product_installed("redturtle.scale"))

    def test_browserlayer(self):
        """Test that IRedturtleScaleLayer is registered."""
        from plone.browserlayer import utils
        from redturtle.scale.interfaces import IRedturtleScaleLayer

        self.assertIn(IRedturtleScaleLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = REDTURTLE_SCALE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("redturtle.scale")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if redturtle.scale is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("redturtle.scale"))

    def test_browserlayer_removed(self):
        """Test that IRedturtleScaleLayer is removed."""
        from plone.browserlayer import utils
        from redturtle.scale.interfaces import IRedturtleScaleLayer

        self.assertNotIn(IRedturtleScaleLayer, utils.registered_layers())

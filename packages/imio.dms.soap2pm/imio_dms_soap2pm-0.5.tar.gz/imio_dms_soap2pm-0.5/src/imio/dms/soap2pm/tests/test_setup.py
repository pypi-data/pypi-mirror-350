# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from imio.dms.soap2pm.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of imio.dms.soap2pm into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if imio.dms.soap2pm is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('imio.dms.soap2pm'))

    def test_uninstall(self):
        """Test if imio.dms.soap2pm is cleanly uninstalled."""
        self.installer.uninstallProducts(['imio.dms.soap2pm'])
        self.assertFalse(self.installer.isProductInstalled('imio.dms.soap2pm'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IImioDmsSoap2pmLayer is registered."""
        from imio.dms.soap2pm.interfaces import IImioDmsSoap2pmLayer
        from plone.browserlayer import utils
        self.assertIn(IImioDmsSoap2pmLayer, utils.registered_layers())

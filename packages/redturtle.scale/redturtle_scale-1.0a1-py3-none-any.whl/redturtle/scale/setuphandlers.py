# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from redturtle.scale import logger
from redturtle.scale.scale import unapply_patches
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "redturtle.scale:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return ["redturtle.scale.upgrades"]


def get_valid_objects(brains):
    """Generate a list of objects associated with valid brains."""
    for b in brains:
        try:
            obj = b.getObject()
        except KeyError:
            obj = None

        if obj is None:  # warn on broken entries in the catalog
            logger.warning("Invalid reference: {0}".format(b.getPath()))
            continue
        yield obj


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    # reindex image_scales metadata
    logger.info("Reindexing image_scales metadata")
    catalog = api.portal.get_tool("portal_catalog")
    for p in catalog._catalog.paths.values():
        # reindex only metadata
        catalog.reindexObject(api.content.get(p), idxs=["image_scales"])


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
    unapply_patches()
    catalog = api.portal.get_tool("portal_catalog")
    for p in catalog._catalog.paths.values():
        # reindex only metadata
        catalog.reindexObject(api.content.get(p), idxs=["image_scales"])

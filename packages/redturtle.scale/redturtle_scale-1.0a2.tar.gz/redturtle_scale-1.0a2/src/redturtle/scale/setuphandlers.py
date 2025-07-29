# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from redturtle.scale import logger
from redturtle.scale.scale import unapply_patches
import transaction
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

def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    # reindex image_scales metadata
    logger.info("Reindexing image_scales metadata")
    catalog = api.portal.get_tool("portal_catalog")
    n = 0
    tot = len(catalog._catalog.paths.values())
    for p in catalog._catalog.paths.values():
        # reindex only metadata
        catalog.reindexObject(api.content.get(p), idxs=["id"])
        n += 1
        if n % 100 == 0:
            logger.info("commit %s/%s", n, tot)
            transaction.commit()


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
    unapply_patches()
    catalog = api.portal.get_tool("portal_catalog")
    n = 0
    tot = len(catalog._catalog.paths.values())
    for p in catalog._catalog.paths.values():
        # reindex only metadata
        catalog.reindexObject(api.content.get(p), idxs=["id"])
        n += 1
        if n % 100 == 0:
            logger.info("commit %s/%s", n, tot)
            transaction.commit()

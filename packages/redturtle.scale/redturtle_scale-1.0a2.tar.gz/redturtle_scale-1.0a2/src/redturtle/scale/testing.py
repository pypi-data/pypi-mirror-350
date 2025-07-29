# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

import redturtle.scale


class RedturtleScaleLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=redturtle.scale)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "redturtle.scale:default")


REDTURTLE_SCALE_FIXTURE = RedturtleScaleLayer()


REDTURTLE_SCALE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(REDTURTLE_SCALE_FIXTURE,),
    name="RedturtleScaleLayer:IntegrationTesting",
)


REDTURTLE_SCALE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(REDTURTLE_SCALE_FIXTURE,),
    name="RedturtleScaleLayer:FunctionalTesting",
)

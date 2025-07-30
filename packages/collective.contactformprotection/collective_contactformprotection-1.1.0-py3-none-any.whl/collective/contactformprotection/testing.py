from plone import api
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.contactformprotection  # noqa


class CollectiveContactformprotectionLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)

        import plone.formwidget.recaptcha

        self.loadZCML(package=plone.formwidget.recaptcha)

        import plone.formwidget.hcaptcha

        self.loadZCML(package=plone.formwidget.hcaptcha)

        import collective.z3cform.norobots

        self.loadZCML(package=collective.z3cform.norobots)

        self.loadZCML(package=collective.contactformprotection)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "plone.formwidget.hcaptcha:default")
        applyProfile(portal, "plone.formwidget.recaptcha:default")
        applyProfile(portal, "collective.z3cform.norobots:default")
        applyProfile(portal, "collective.contactformprotection:default")
        # basic mailsetup
        api.portal.set_registry_record(
            "plone.email_from_address", "test@localhost.local"
        )
        api.portal.set_registry_record("plone.email_from_name", "testuser")


COLLECTIVE_CONTACTFORMPROTECTION_FIXTURE = CollectiveContactformprotectionLayer()


COLLECTIVE_CONTACTFORMPROTECTION_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_CONTACTFORMPROTECTION_FIXTURE,),
    name="CollectiveContactformprotectionLayer:IntegrationTesting",
)


COLLECTIVE_CONTACTFORMPROTECTION_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_CONTACTFORMPROTECTION_FIXTURE,),
    name="CollectiveContactformprotectionLayer:FunctionalTesting",
)


COLLECTIVE_CONTACTFORMPROTECTION_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_CONTACTFORMPROTECTION_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="CollectiveContactformprotectionLayer:AcceptanceTesting",
)

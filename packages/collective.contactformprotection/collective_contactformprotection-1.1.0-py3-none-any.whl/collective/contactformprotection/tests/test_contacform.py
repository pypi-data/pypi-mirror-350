"""Setup tests for this package."""

from collective.contactformprotection.testing import (
    COLLECTIVE_CONTACTFORMPROTECTION_INTEGRATION_TESTING,
)
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.zope import Browser

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.contactformprotection is properly installed."""

    layer = COLLECTIVE_CONTACTFORMPROTECTION_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.browser = Browser(self.layer["app"])
        self.browser.addHeader(
            "Authorization",
            "Basic {}:{}".format(
                SITE_OWNER_NAME,
                SITE_OWNER_PASSWORD,
            ),
        )

    def test_contactform_disabled(self):
        self.browser.open("http://nohost/plone/contact-info")
        self.assertIn("form.widgets.sender_fullname", self.browser.contents)

        # disable via controlpanel
        self.browser.open("http://nohost/plone/@@contactformprotection-controlpanel")
        self.browser.getControl("Disable contactform globally").click()
        self.browser.getControl("Save").click()

        # there should be nomore contactform
        self.browser.open("http://nohost/plone/contact-info")
        self.assertNotIn("form.widgets.sender_fullname", self.browser.contents)
        self.assertIn("Contact form is disabled.", self.browser.contents)

    def test_contactform_captchawidget(self):
        self.browser.open("http://nohost/plone/contact-info")

        # disabled per default
        self.assertNotIn(
            "formfield-form-widgets-IContactFormCaptchaField-captcha",
            self.browser.contents,
        )

        # enable captcha in controlpanel
        self.browser.open("http://nohost/plone/@@contactformprotection-controlpanel")
        self.browser.getControl(name="form.widgets.use_captcha:list").value = "hcaptcha"
        self.browser.getControl("Save").click()

        self.browser.open("http://nohost/plone/contact-info")
        # field should be visible now
        self.assertIn(
            "formfield-form-widgets-IContactFormCaptchaField-captcha",
            self.browser.contents,
        )

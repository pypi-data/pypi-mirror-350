from Acquisition import aq_inner
from collective.contactformprotection import _
from collective.contactformprotection.vocabulary import lookup_captchavocab_item
from plone import api
from plone.autoform.interfaces import WIDGETS_KEY
from plone.autoform.widgets import ParameterizedWidget
from Products.CMFPlone.browser.contact_info import ContactForm as ContactInfoForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import validator
from zope import schema
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.interface.interfaces import ComponentLookupError
from zope.schema import ValidationError


class CaptchaNotFound(Exception):
    __doc__ = _("Could not find a valid captcha addon. Did you uninstall it?")


class InvalidCaptchaCode(ValidationError):
    __doc__ = _("Please validate the captcha field before sending the form.")


class IContactFormCaptchaField(Interface):
    captcha = schema.TextLine(
        title=_("Captcha code"),
        required=False,
    )


class ContactForm(ContactInfoForm):
    template = ViewPageTemplateFile("contact-form.pt")

    @property
    def additionalSchemata(self):
        captcha = lookup_captchavocab_item()

        if captcha and captcha.widget:
            IContactFormCaptchaField.setTaggedValue(
                WIDGETS_KEY, {"captcha": ParameterizedWidget(captcha.widget)}
            )
            return (IContactFormCaptchaField,)

        return ()

    @property
    def enabled(self):
        return not api.portal.get_registry_record(
            "collective.contactformprotection.disable_form",
            default=False,
        )


class CaptchaValidator(validator.SimpleFieldValidator):
    # Object, Request, Form, Field, Widget,
    # We adapt the CaptchaValidator class to all form fields (IField)

    def validate(self, value):
        super().validate(value)
        captcha = lookup_captchavocab_item()

        if not captcha.validator_view:
            raise CaptchaNotFound

        try:
            captcha = getMultiAdapter(
                (aq_inner(self.context), self.request),
                name=captcha.validator_view,
            )
            if not captcha.verify(value):
                raise InvalidCaptchaCode
        except ComponentLookupError:
            raise InvalidCaptchaCode

        return True


# Register Captcha validator for the Captcha field in the
# IContactFormExtenderFields Form
validator.WidgetValidatorDiscriminators(
    CaptchaValidator, field=IContactFormCaptchaField["captcha"]
)

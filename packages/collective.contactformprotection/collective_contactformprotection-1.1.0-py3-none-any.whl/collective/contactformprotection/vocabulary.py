from collective.contactformprotection import _
from plone import api
from plone.base.utils import get_installer
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class CaptchaVocabItem:
    def __init__(self, token, value, widget=None, validator_view=""):
        self.token = token
        self.value = value
        self.widget = widget
        self.validator_view = validator_view


@implementer(IVocabularyFactory)
class CaptchaVocabulary:
    """ """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = []
        installer = get_installer(api.portal.get(), getRequest())

        try:
            from plone.formwidget.hcaptcha import HCaptchaFieldWidget

            if installer.is_product_installed("plone.formwidget.hcaptcha"):
                items.append(
                    CaptchaVocabItem(
                        "hcaptcha", _("HCaptcha"), HCaptchaFieldWidget, "hcaptcha"
                    )
                )
        except ImportError:
            pass

        try:
            from plone.formwidget.recaptcha import ReCaptchaFieldWidget

            if installer.is_product_installed("plone.formwidget.recaptcha"):
                items.append(
                    CaptchaVocabItem(
                        "recaptcha", _("ReCaptcha"), ReCaptchaFieldWidget, "recaptcha"
                    )
                )
        except ImportError:
            pass

        try:
            from collective.z3cform.norobots import NorobotsFieldWidget

            if installer.is_product_installed("collective.z3cform.norobots"):
                items.append(
                    CaptchaVocabItem(
                        "norobots", _("Norobots"), NorobotsFieldWidget, "norobots"
                    )
                )
        except ImportError:
            pass

        # create a list of SimpleTerm items:
        terms = []
        for item in items:
            term = SimpleTerm(
                value=item.token,
                token=str(item.token),
                title=item.value,
            )
            term.widget = item.widget
            term.validator_view = item.validator_view

            terms.append(term)

        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


CaptchaVocabularyFactory = CaptchaVocabulary()


def lookup_captchavocab_item(context=None):
    # determine the available captcha
    use_captcha = api.portal.get_registry_record(
        "collective.contactformprotection.use_captcha",
    )
    if use_captcha is None:
        return
    try:
        return CaptchaVocabularyFactory(context).getTermByToken(use_captcha)
    except LookupError:
        # likely a selected but uninstalled/removed captcha addon
        return

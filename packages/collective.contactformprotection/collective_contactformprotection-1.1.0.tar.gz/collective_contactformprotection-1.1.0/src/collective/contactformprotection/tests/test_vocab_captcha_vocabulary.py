from collective.contactformprotection import _
from collective.contactformprotection.testing import (  # noqa
    COLLECTIVE_CONTACTFORMPROTECTION_INTEGRATION_TESTING,
)
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.interfaces import IVocabularyTokenized

import unittest


class CaptchaVocabularyIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_CONTACTFORMPROTECTION_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_vocab_captcha_vocabulary(self):
        vocab_name = "contactformprotection.captchavocabulary"
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))
        self.assertEqual(len(vocabulary), 3)
        self.assertEqual(
            vocabulary.getTerm("hcaptcha").title,
            _("HCaptcha"),
        )

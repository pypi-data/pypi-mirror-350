.. This README is meant for consumption by humans and PyPI. PyPI can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on PyPI or github. It is a comment.

.. image:: https://github.com/collective/collective.contactformprotection/actions/workflows/meta.yml/badge.svg
    :target: https://github.com/collective/collective.contactformprotection/actions/workflows/meta.yml


================================
collective.contactformprotection
================================

This package protects the default contact form of Plone which is generally accessible via ``/contact-info``.
If you have installed this product, you can go to the ``Contacformprotection Control Panel`` and adjust its settings.


Settings
--------

- Provide a checkbox in the controlpanel to disable the form globally
- Add a H/Recaptcha/Norobots field depending on the installed 3rd party addon ``plone.formwidget.[h|re]captcha`` or ``collective.z3cform.norobots``.


Captcha support
---------------

If you have installed ``plone.formwidget.recaptcha``, ``plone.formwidget.hcaptcha`` or ``collective.z3cform.norobots`` it is automatically
added to the form. In case both are installed, you can make a choice in the controlpanel.

You can install the packages by adding the ``extra_required`` to this package::

    [buildout]
    ...
    eggs =
        collective.contactformprotection[hcaptcha,recaptcha,norobots]


The settings mentioned above are all set in the configuration registry. See ``plone.app.registry`` how to set these
values TTW or in a package profile.


Installation
------------

Install collective.contactformprotection by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.contactformprotection


and then running ``bin/buildout``


Customizing Captcha vocabulary
------------------------------

The captcha settings is provided by a zope vocabulary with enhanced term objects::

    class CaptchaVocabItem(object):
        def __init__(self, token, value, widget=None, validator_view=""):
            self.token = token
            self.value = value
            self.widget = widget
            self.validator_view = validator_view

If you have additional captcha addons or want to override the provided widget and validator view, you can
override the vocabulary utility ``contactformprotection.captchavocabulary`` with your terms.



Authors
-------

Peter Mathis, petschki



Contribute
----------

- Issue Tracker: https://github.com/collective/collective.contactformprotection/issues
- Source Code/Documentation: https://github.com/collective/collective.contactformprotection


License
-------

The project is licensed under the GPLv3.

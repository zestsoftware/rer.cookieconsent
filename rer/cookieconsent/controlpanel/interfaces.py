# -*- coding: utf-8 -*-
from plone import api
from plone.registry.field import PersistentField
from rer.cookieconsent import messageFactory as _
from z3c.form.object import registerFactoryAdapter
from zope import schema

# from zope.component.hooks import getSite
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.vocabulary import SimpleVocabulary


trueFalseVocabulary = SimpleVocabulary.fromItems(
    ((u'true', 'true'), (u'false', 'false'))
)


def default_language():
    site = api.portal.get()
    try:
        return site.portal_languages.getDefaultLanguage()
    except AttributeError:
        # PLONE 5
        language_tool = api.portal.get_tool('portal_languages')
        return language_tool.getDefaultLanguage()


class ICookieBannerEntry(Interface):
    """Single entry for the Cookie Consent banner configuration
    """

    lang = schema.Choice(
        title=_(u'Language'),
        defaultFactory=default_language,
        missing_value=u'',
        required=True,
        vocabulary=u'rer.cookieconsent.vocabularies.AvailableLanguages',
    )

    text = schema.Text(
        title=_(u'Cookie consent banner content'),
        description=_(
            'text_help',
            default=u'Provide the text to be put inside the cookie consent banner.\n'  # noqa
            u'You can use HTML here but you can avoid it.\n'  # noqa
            u'Use the "$privacy_link" marker to insert an HTML link to the Privacy Policy (see below).\n'  # noqa
            u'If you want full controls over the HTML generated you can use the "$privacy_link_url" marker '  # noqa
            u'(URL of the link) and "$privacy_link_text" (text of the link).\n'  # noqa
            u'In the same way you can use "$dashboard_link", "$dashboard_link_url" and "$dashboard_text" '  # noqa
            u'to provide links to the opt-out dashboard.',
        ),  # noqa
        default=u'',
        missing_value=u'',
        required=True,
    )

    privacy_link_url = schema.TextLine(
        title=_(u'URL of the Privacy Policy'),
        description=_(
            'privacy_link_url_help',
            default=u'An URL, or a absolute path, to a page where user can read the full '  # noqa
            u'Privacy Policy of your site.\n'  # noqa
            u'Examples: "http://externalsite.com/privacy.html", "/internal/document".',
        ),  # noqa
        required=False,
    )

    privacy_link_text = schema.TextLine(
        title=_(u'Text of the Privacy Policy link'),
        description=_(
            'privacy_link_text_help',
            default=u'The text to be used when generating the URL specified in the '  # noqa
            u'URL of the Privacy Policy".\n'
            u'If not provided, the full URL is used.',
        ),
        required=False,
    )

    dashboard_link_text = schema.TextLine(
        title=_(u'Text of the link to opt-out dashboard'),
        description=_(
            'dashboard_link_text',
            default=u'The text to be used when generating the URL to the opt-out dashboard',
        ),  # noqa
        required=False,
    )


class IOptOutEntrySubitemPersistentObject(Interface):
    pass


@implementer(IOptOutEntrySubitemPersistentObject)
class OptOutEntrySubitemPersistentObject(PersistentField, schema.Object):
    pass


class IOptOutEntrySubitem(Interface):
    """A single translation entry for a OutOut configuration
    See IOptOutEntry
    """

    lang = schema.Choice(
        title=_(u'Language'),
        defaultFactory=default_language,
        missing_value=u'',
        required=True,
        vocabulary=u'rer.cookieconsent.vocabularies.AvailableLanguages',
    )

    app_title = schema.TextLine(
        title=_(u'Application name'),
        description=_(
            'app_title_help',
            default=u'This will be the title used in the opt-out configuration dashboard.',
        ),  # noqa
        default=u'',
        missing_value=u'',
        required=False,
    )

    app_description = schema.Text(
        title=_(u'Application description'),
        description=_(
            'app_description_help',
            default=u'A long description that must explain what this opt-out will do if activated.\n'  # noqa
            u'You can also use HTML here.',
        ),
        default=u'',
        missing_value=u'',
        required=False,
    )


class IOptOutEntry(Interface):
    """Single entry for an Opt-Out application configuration
    """

    app_id = schema.ASCIILine(
        title=_(u'Application ID'),
        description=_(
            'app_id_help',
            default=u'A unique identifier for the application influenced bt this opt-out',
        ),  # noqa
        default='',
        missing_value='',
        required=True,
    )

    cookies = schema.Tuple(
        title=_(u'Cookies'),
        description=_(
            'cookies_help',
            default=u'A list of cookies names prefixes.\n'
            u'This opt-out will generate a cookie in the form PREFIX-optout for every defined prefix.',
        ),  # noqa
        required=True,
        value_type=schema.ASCIILine(),
    )

    default_value = schema.Choice(
        title=_(u'Cookie(s) initial value'),
        description=_(
            'default_value_help',
            default=u'When a user access for the first time the site, all of the opt-out cookies are set.\n'  # noqa
            u'You must select the default value for those cookies.',
        ),  # noqa
        required=True,
        default='true',
        vocabulary=trueFalseVocabulary,
    )

    texts = schema.Tuple(
        title=_(u'Opt-out entry titles and descriptions'),
        description=_(
            'help_optout_texts',
            default=u'For every involved language provide title and description that will be used '  # noqa
            u'for generate an translated opt-out dashboard.\n'
            u'In the case a specific translation is missing, the first in the list will be '  # noqa
            u'used as default.\n'
            u'If this field is not filler, a translation for "APPID_optout_title" '  # noqa
            u'and "APPID_optout_description" will be used.',
        ),
        value_type=OptOutEntrySubitemPersistentObject(
            IOptOutEntrySubitem, title=_(u'Opt-out title and description')
        ),
        required=False,
        default=(),
        missing_value=(),
    )


@implementer(ICookieBannerEntry)
class CookieBannerEntry(object):
    def __init__(
        self, lang=u'', text=u'', privacy_link_url=u'', privacy_link_text=u''
    ):
        self.lang = lang
        self.text = text
        self.privacy_link_url = privacy_link_url
        self.privacy_link_text = privacy_link_text


@implementer(IOptOutEntry)
class OptOutEntry(object):
    def __init__(
        self, app_id=u'', cookies=(), default_value=u'true', texts=()
    ):
        self.app_id = app_id
        self.cookies = cookies
        self.default_value = default_value
        self.texts = texts


@implementer(IOptOutEntrySubitem)
class OptOutEntrySubitem(object):
    def __init__(self, lang=u'', app_title=u'', app_description=u''):
        self.lang = lang
        self.app_title = app_title
        self.app_description = app_description


class ICookieBannerEntryPersistentObject(Interface):
    pass


@implementer(ICookieBannerEntryPersistentObject)
class CookieBannerEntryPersistentObject(PersistentField, schema.Object):
    validate_invariants = True


class IOptOutEntryPersistentObject(Interface):
    pass


@implementer(IOptOutEntryPersistentObject)
class OptOutEntryPersistentObject(PersistentField, schema.Object):
    pass


class ICookieBannerSettings(Interface):
    """Settings for the Cookie Consent banner
    """

    # enabled = schema.Bool(
    #    title=_(u'Consent banner enabled'),
    #    description=_(
    #        'help_cookie_consent_enabled',
    #        default=_(u'If checked, the cookie consent banner will be displayed.')),

    #    required=False,
    #    default=False,
    #)

    accept_on_click = schema.Bool(
        title=_(u'Accept policy on every click'),
        description=_(
            'help_accept_on_click',
            default=u'If checked, any click on links on any page will be interpreted as the '  # noqa
            u'user accepted the cookie policy.',
        ),
        required=False,
        default=False,
    )

    cookie_consent_configuration = schema.Tuple(
        title=_(u'Cookie consent configuration'),
        description=_(
            'help_cookie_consent_configuration',
            default=u'For every involved language, provide a configuration of the cookie consent banner.\n'  # noqa
            u'The first defined policy configuration will be the default ones '  # noqa
            u'(the ones used when not language specific configuration is found).',
        ),  # noqa
        value_type=CookieBannerEntryPersistentObject(
            ICookieBannerEntry, title=_(u'Cookie consent banner configuration')
        ),  # noqa
        required=False,
        default=(),
        missing_value=(),
    )


class IOptOutSettings(Interface):
    """Settings for the Optout"""

    optout_configuration = schema.Tuple(
        title=_(u'Opt-out configurations'),
        description=_(
            'help_optout_configuration',
            default=u'When the user accepted the general cookie policy he can still accept/decline '  # noqa
            u'a single kind of cookie(s) from a 3rd part application.\n'  # noqa
            u'From this panel you can configure opt-out cookies for those applications.\n'  # noqa
            u'PLEASE NOTE: this product will only handle and generate cookies, is duty of '  # noqa
            u'others products to use those cookies in the correct manner.',
        ),  # noqa
        value_type=OptOutEntryPersistentObject(
            IOptOutEntry, title=_(u'Opt-out configuration')
        ),
        required=False,
        default=(),
        missing_value=(),
    )


class ICookieConsentSettings(ICookieBannerSettings, IOptOutSettings):
    """Settings used in the control panel for cookiecosent: unified panel
    """


registerFactoryAdapter(ICookieBannerEntry, CookieBannerEntry)
registerFactoryAdapter(IOptOutEntry, OptOutEntry)
registerFactoryAdapter(IOptOutEntrySubitem, OptOutEntrySubitem)

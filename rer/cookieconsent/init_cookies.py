# -*- coding: utf-8 -*-
# from ZPublisher.interfaces import IPubBeforeCommit, IPubSuccess
from DateTime import DateTime
from plone import api
from plone.browserlayer.utils import registered_layers
from plone.registry.interfaces import IRegistry
from rer.cookieconsent import config
from rer.cookieconsent.controlpanel.interfaces import ICookieConsentSettings
from rer.cookieconsent.interfaces import ICookieConsentLayer
from rer.cookieconsent.utils import setCookie
from zope.component import queryUtility

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


# @adapter(IPubSuccess)
def send_initial_cookies_values(event):
    """
    If the COOKIECONSENT_NAME if not present at all, user not choosen yet if
    accept cookies or not.
    In that case we automatically send all of the opt-put cookies not present.
    """

    request = event.request

    # Checks to limit subscribers calls
    if (
        config.COOKIECONSENT_NAME in request.response.cookies
        or ICookieConsentLayer not in registered_layers()
    ):
        return
    site = api.portal.get()
    if site is None:
        return

    # TODO: evaluate if move this list in a Plone registry field (performance?)
    for subdomain in config.DOMAIN_WHITELIST:
        if urlparse(request.URL).netloc.find(subdomain) > -1:
            return
    optout_all(request, writeRequest=True)


def optout_all(request, value=None, update=False, writeRequest=False):
    """
    For all of the opt-out cookies, set the value
    This will not change values for cookies already set until update=True is
    provided
    """
    registry = queryUtility(IRegistry)
    settings = registry.forInterface(ICookieConsentSettings, check=False)
    if settings and settings.optout_configuration:
        for oo_conf in settings.optout_configuration:
            for cookie in oo_conf.cookies:
                cookiename = "{0}-optout".format(cookie)
                if cookiename in request.cookies and not update:
                    continue
                nextYear = DateTime() + 365
                cookievalue = value if value else oo_conf.default_value
                setCookie(
                    request.response,
                    cookiename,
                    cookievalue,
                    expires=nextYear.rfc822(),
                )
                if writeRequest:
                    request.cookies[cookiename] = cookievalue

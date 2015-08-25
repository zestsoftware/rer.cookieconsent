# -*- coding: utf-8 -*-

from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser import BrowserView
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from rer.cookieconsent.controlpanel.interfaces import ICookieConsentSettings
from rer.cookieconsent import config
from rer.cookieconsent.init_cookies import optout_all
from rer.cookieconsent import messageFactory as _
from zope.i18n import translate
from DateTime import DateTime
from zope.component import getMultiAdapter
from plone.memoize.view import memoize


class OptOutDashboardView(BrowserView):
    """Personal dashboard for opt-out preferences"""
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.general_cookie_consent = None
        self.nextYear = DateTime() + 365
        request.set('disable_border', True)

    def __call__(self, *args, **kwargs):
        if 'form.submitted' in self.request.form:
            self._save_changes()
            IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"), "info")
            self.request.response.redirect("%s/@@%s" % (self.context.absolute_url(),
                                                        self.__name__),)
        return self.index()

    def _save_changes(self):
        request = self.request
        cookies = request.cookies
        form = request.form
        if not form.get('accept_cookies'):
            # Cookie policy rejected: set all of the opt-out cookies
            optout_all(request, 'true', update=True)
            self.setOneYearCookie(config.COOKIECONSENT_NAME, 'false')
            return
        # Cookie consent given: let's save also optout cookies
        self.setOneYearCookie(config.COOKIECONSENT_NAME, 'true')
        for optout in self.settings().optout_configuration:
            value = 'true' if form.get('app_%s' % optout.app_id)=='true' else 'false'
            for cookie in optout.cookies:
                self.setOneYearCookie("%s-optout" % cookie, value)

    def setOneYearCookie(self, name, value):
        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        site = portal_state.portal()
        self.request.response.setCookie(name, value,
                                        path='/'.join(site.getPhysicalPath()),
                                        expires=self.nextYear.rfc822())


    def _i18n_alternatives(self, oo_conf, id, default):
        oo_i18n_id = u"%s_optout_%s" % (oo_conf.app_id, id)
        oo_item = translate(_(oo_i18n_id), context=self.request)
        if unicode(oo_item)==oo_i18n_id:
            oo_item = default
        return oo_item

    @memoize
    def settings(self):
        registry = queryUtility(IRegistry)
        return registry.forInterface(ICookieConsentSettings, check=False)

    def optouts(self):
        settings = self.settings()
        request = self.request
        cookies = request.cookies
        self.general_cookie_consent = cookies.get(config.COOKIECONSENT_NAME, False)=='true'

        results = []
        for oo_conf in settings.optout_configuration:
            optout = {}
            optout['id'] = oo_conf.app_id
            optout['title'] = self._i18n_alternatives(oo_conf, u'title', oo_conf.app_title)
            raw_i18n_desc = self._i18n_alternatives(oo_conf, u'description', oo_conf.app_description)
            optout['description'] = '<br />'.join(raw_i18n_desc.strip().splitlines())
            
            # check cookies: to enable the radio as "deny" we care about at least of one cookie
            negative_cookies = [c for c in oo_conf.cookies \
                    if not cookies.get("%s-optout" % c, None) or cookies["%s-optout" % c]=='false']
            optout['cookie'] = False if negative_cookies else True
            results.append(optout)
        return results

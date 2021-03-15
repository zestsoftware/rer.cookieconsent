# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from rer.cookieconsent.init_cookies import optout_all
from zope.publisher.interfaces.browser import IBrowserView
from urllib.parse import unquote_plus


class ResetOptoutView(BrowserView):
    """Set all of the opt-out cookies to false
    Redirect to "current" page after that.
    """

    def __call__(self, *args, **kwargs):
        optout_all(self.request, "false", update=True)
        context = self.context
        if IBrowserView.providedBy(context):
            # This context is also a view, we called something like
            # /foo/bar/@@view/@@reset-optout
            here_url = "{0}/@@{1}".format(
                context.context.absolute_url(), context.__name__
            )
        else:
            qs = self.request.QUERY_STRING
            here_url = context.absolute_url()
            # Let's support utm_ and other attributes in redirect.
            if qs != "":
                here_url = unquote_plus("=".join(qs.split("=")[1:]))
        print(here_url)
        self.request.response.redirect(here_url)

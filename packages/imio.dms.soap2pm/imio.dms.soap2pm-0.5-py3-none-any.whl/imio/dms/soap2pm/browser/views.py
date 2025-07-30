# -*- coding: utf-8 -*-

from imio.helpers.xhtml import object_link
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView

import base64


class IncomingMailSoapClientView(BrowserView):
    """ Adapts an incomingmail to prepare data to exchange within imio.pm.wsclient """

    def get_main_files(self):
        pc = getToolByName(self.context, 'portal_catalog')
        res = []
        for brain in pc(portal_type=('dmsmainfile', 'dmsommainfile', 'dmsappendixfile'),
                        path='/'.join(self.context.getPhysicalPath())):
            obj = brain.getObject()
            res.append({'title': safe_unicode(obj.title),
                        'filename': safe_unicode(obj.file.filename),
                        'file': base64.b64encode(obj.file.data)})
        return res

    def detailed_description(self):
        """ Return a link to current object """
        return u"<p>Fiche courrier liée: %s</p>" % object_link(self.context, target="_blank")

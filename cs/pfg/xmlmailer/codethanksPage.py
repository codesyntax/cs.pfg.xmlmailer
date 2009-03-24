import os

from AccessControl import ClassSecurityInfo
from Acquisition import aq_parent

from Products.Archetypes.atapi import *
from Products.PloneFormGen.content.thanksPage import FormThanksPage, ThanksPageSchema

from StringIO import StringIO
from zope.interface import implements
from email import Encoders
from email.Header import Header
from email.MIMEAudio import MIMEAudio
from email.MIMEBase import MIMEBase
from email.MIMEImage import MIMEImage
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from cs.pfg.xmlmailer.config import *
from cs.pfg.xmlmailer import XMLMailerFactory as _

from DateTime import DateTime

from zope.interface import implements

import transaction
import zExceptions
from AccessControl import ClassSecurityInfo

from Products.CMFCore.permissions import View, ModifyPortalContent

from Products.Archetypes.public import *
from Products.Archetypes.utils import shasattr
from Products.Archetypes.interfaces.field import IField

from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.configuration import zconf

from Products.PloneFormGen.config import PROJECTNAME
from Products.PloneFormGen.interfaces import IPloneFormGenThanksPage

from Products.PloneFormGen import PloneFormGenMessageFactory as _
from Products.PloneFormGen import HAS_PLONE30, dollarReplace

import zope.i18n

CodeThanksPageSchema = ThanksPageSchema.copy()



class CodeFormThanksPage(FormThanksPage):
    """A thank-you page that can display form input"""

    schema         =  CodeThanksPageSchema

    content_icon   = 'ThanksPage.gif'
    meta_type      = 'CodeFormThanksPage'
    portal_type    = 'CodeFormThanksPage'
    archetype_name = 'Code Form Thanks Page'

    immediate_view = 'fg_thankspage_view'
    default_view   = 'fg_thankspage_view'
    suppl_views = ()

    typeDescription= 'A thank-you page that can display form input.'

    global_allow = 0    

    security       = ClassSecurityInfo()
    
    security.declarePublic('getThanksEpilogue')
    def getThanksEpilogue(self):
        """ get expanded epilogue """
        import pdb;pdb.set_trace()
        
        return self._dreplace( self.getRawThanksEpilogue() )

registerType(CodeFormThanksPage, PROJECTNAME)

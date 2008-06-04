from AccessControl import ClassSecurityInfo
from Acquisition import aq_parent

from Products.Archetypes.atapi import registerType
from Products.PloneFormGen.content.formMailerAdapter import FormMailerAdapter, formMailerAdapterSchema

from StringIO import StringIO

from email import Encoders
from email.Header import Header
from email.MIMEAudio import MIMEAudio
from email.MIMEBase import MIMEBase
from email.MIMEImage import MIMEImage
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from cs.pfg.xmlmailer.config import *

xmladapterSchema = formMailerAdapterSchema.copy()

class FormXMLMailerAdapter(FormMailerAdapter):
    """ A form action adapter that will e-mail plaint text form input
        together with an XML representation of the form
    """

    schema = xmladapterSchema
    portal_type = meta_type = 'XMLMailerAdapter'
    archetype_name = 'XML Mailer Adapter'

    security = ClassSecurityInfo()

    security.declarePrivate('get_mail_text_in_xml')
    def get_mail_text_in_xml(self, fields, request, **kwargs):
        text = StringIO()

        text.write('<?xml version="1.0" encoding="utf-8">?')
        text.write('<element>')
        text.write('<header>')
        text.write('<TITLE>')
        text.write(aq_parent(self).Title())
        text.write('</TITLE>')
        text.write('</header>')
        
        if self.body_pre:
            text.write('<foreword>')
            text.write(self.body_pre)
            text.write('</foreword>')
        
        text.write('<element_list>')
        for field in fields:
            text.write('<item>')
            text.write('<title>')
            text.write(field.fgField['widget'].label)
            text.write('</title>')
            text.write('<text>')
            text.write(field.htmlValue(request))
            text.write('</text>')
            text.write('</item>')                       

        text.write('</element_list>')

        if self.body_post:
            text.write('<epilogue>')
            text.write(self.body_pre)
            text.write('</epilogue>')

        if self.body_footer:
            text.write('<footer>')
            text.write(self.body_pre)
            text.write('</footer>')
            

        text.write('</element>')
        return text.getvalue()
        

    security.declarePrivate('get_mail_text')
    def get_mail_text(self, fields, request, **kwargs):
        """ Get header and body of e-amil as text (string)
            This will create both parts of the e-mail: text and the XML file
        """

        headerinfo, additional_headers, body = self.get_header_body_tuple(fields, request, **kwargs)
        body_xml = self.get_mail_text_in_xml(fields, request, **kwargs)

        mime_text = MIMEText(body, _subtype=self.body_type or 'html', _charset=self._site_encoding())
        attachments = self.get_attachments(fields, request)

        outer = MIMEMultipart()
        outer.attach(mime_text)

        # write header
        for key, value in headerinfo.items():
            outer[key] = value

        # write additional header
        for a in additional_headers:
            key, value = a.split(':', 1)
            outer.add_header(key, value.strip())

        for attachment in attachments:
            filename = attachment[0]
            ctype = attachment[1]
            encoding = attachment[2]
            content = attachment[3]

            if ctype is None:
                ctype = 'application/octet-stream'

            maintype, subtype = ctype.split('/', 1)

            if maintype == 'text':
                msg = MIMEText(content, _subtype=subtype)
            elif maintype == 'image':
                msg = MIMEImage(content, _subtype=subtype)
            elif maintype == 'audio':
                msg = MIMEAudio(content, _subtype=subtype)
            else:
                msg = MIMEBase(maintype, subtype)
                msg.set_payload(content)
                # Encode the payload using Base64
                Encoders.encode_base64(msg)

            # Set the filename parameter
            msg.add_header('Content-Disposition', 'attachment', filename=filename)
            outer.attach(msg)

        ctype = 'application/octet-stream'
        maintyep, subtype = ctype.split('/', 1)
        p = MIMEBase(maintype, subtype)
        p.set_payload(body_xml)
        p.add_header('content-disposition', 'attachment', filename='form.xml')
        Encoders.encode_base64(p)
        outr.attach(p)
        return outer.as_string()


registerType(FormXMLMailerAdapter, PROJECTNAME)

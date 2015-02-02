"""
From: https://codecomments.wordpress.com/2008/01/04/python-gmail-smtp-example/

Derived from:
http://kutuma.blogspot.com/2007/08/sending-emails-via-gmail-with-python.html
and http://mail.python.org/pipermail/python-list/2003-September/225540.html



"""


import os, sys
import smtplib
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEAudio import MIMEAudio
from email.MIMEImage import MIMEImage
from email.Encoders import encode_base64

def sendMail(subject, text, *attachmentFilePaths):
  gmailUser = 'from_server@danenet.org'
  recipient = 'eric.howland@gmail.com'
  msg = MIMEMultipart()
  msg['From'] = gmailUser
  msg['To'] = recipient
  msg['Subject'] = subject
  msg.attach(MIMEText(text))
  for attachmentFilePath in attachmentFilePaths:
    msg.attach(getAttachment(attachmentFilePath))

  mailServer = smtplib.SMTP_SSL('ASPMX.L.GOOGLE.COM', 465)
  #try:
  #    mailServer = smtplib.SMTP('ASPMX.L.GOOGLE.COM', 587)  <=== right port??
  #except:
  #    
  #    err = sys.exc_info()[0]
  #    print """Unable to connect to the mail server.  This is realy a IP6 error
  #      but can be caused by a block on outgoing connections to SMPT servers
  #      when the fallback is to try to make a IP6 connection which then
  #      fails with this error
  #    """, err
  #    sys.exit("""Unable to connect to the mail server.  This is likely a IP6 error
  #      but can be caused by a block on outgoing connections to SMPT servers
  #      when the fallback is to try to make a IP6 connection
  #    """)

  mailServer.ehlo()
  mailServer.starttls()
  mailServer.ehlo()
  mailServer.login(gmailUser, gmailPassword)
  mailServer.sendmail(gmailUser, recipient, msg.as_string())
  mailServer.close()
  print('Sent email to %s' % recipient)

  
def getAttachment(attachmentFilePath):
  contentType, encoding = mimetypes.guess_type(attachmentFilePath)
  if contentType is None or encoding is not None:
    contentType = 'application/octet-stream'
  mainType, subType = contentType.split('/', 1)
  file = open(attachmentFilePath, 'rb')
  if mainType == 'text':
    attachment = MIMEText(file.read())
  elif mainType == 'message':
    attachment = email.message_from_file(file)
  elif mainType == 'image':
    attachment = MIMEImage(file.read(),_subType=subType)
  elif mainType == 'audio':
    attachment = MIMEAudio(file.read(),_subType=subType)
  else:
    attachment = MIMEBase(mainType, subType)
  attachment.set_payload(file.read())
  encode_base64(attachment)
  file.close()
  attachment.add_header('Content-Disposition', 'attachment',   filename=os.path.basename(attachmentFilePath))
  return attachment


def emailmain():
    global attachmentFilePaths
    attachmentFilePaths = ["/var/www/"]
    
    sendMail("Test message from server",
             "the readings go here", *attachmentFilePaths)

if __name__ == "__main__":
    emailmain()


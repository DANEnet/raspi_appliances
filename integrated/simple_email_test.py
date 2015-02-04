import smtplib, os, datetime
import gmail_password



def mail0(receiver,Message):

  s=smtplib.SMTP_SSL()
  s.connect("smpt.gmail.com", 465)

  s.login('from_server@danenet.org', gmail_password.gmail_password())
  s.sendmail("eric.howland@gmail.com", T, M)


def mail_2(receiver,Message):
  ### try to open and then switch to ttls
    print  "step 1", receiver, Message
    

    s=smtplib.SMTP("ASPMX.L.GOOGLE.COM", 587)
    s.set_debuglevel(9)
    print "step 1b after smtplib"
    #s.connect("ASPMX.L.GOOGLE.COM", 587)
    #print "step 1c after connect"
    s.ehlo()
    print "step 1d after ehlo"
    s.starttls()
    print "step 1e after starttls"
    s.ehlo()
    print "step 2 after ehlo"
    #s.login("email@gmail.com", gmail_passoword())
    s.login('from_server@danenet.org', gmail_password.gmail_password())
    print "step 3 right before sendmail"
    s.sendmail("from_server@danenet.org", receiver, Message)



# from http://www.pceworld.com/view/9216127
def mail_3(receiver,Message):
    print  "step 1", receiver, Message
    
    try:
        s=smtplib.SMTP_SSL()
        s.set_debuglevel(9)
        print "step 1b after smtplib"
        s.connect("smtp.gmail.com", 465)
        print "step 1c after connect"
        s.ehlo()
        print "step 1d after ehlo"
        #s.starttls()
        print "step 1e after starttls"
        s.ehlo()
        print "step 2 after ehlo"
        #s.login("email@gmail.com", gmail_password())
        s.login('from_server@danenet.org', gmail_password.gmail_password())
        print "step 3 right before sendmail"
        s.sendmail("from_server@danenet.org", receiver, Message)
    except Exception,R:
            return R
    print "success??"
    
def main():
  now = datetime.datetime.today()
  msg = "This is a test %s"%now.strftime("%Y-%m-%dT%H:%M:%S")
  print msg
  mail_3("ehowland@danenet.org", msg)

if __name__ == "__main__":
    main()
    
################################################# works
#    print  "step 1", receiver, Message
#    import smtplib
#    try:
#        s=smtplib.SMTP_SSL()
#        s.connect("smtp.gmail.com",465)
#        s.ehlo()
#        s.starttls()
#        s.ehlo()
#        s.login('from_server@danenet.org', 'messag_2.Garcia')
#        s.sendmail("from_server@danenet.org", receiver, Message)
#    except Exception,R:
#            return R
#####################################################

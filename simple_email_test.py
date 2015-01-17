def mail0():
  import smtplib
  s=smtplib.SMTP_SSL()
  s.connect("smpt.gmail.com", 465)

  s.login('from_server@danenet.org', 'messag_2.Garcia')
  s.sendmail("eric.howland@gmail.com", T, M)


# from http://www.pceworld.com/view/9216127
def mail(receiver,Message):
    print  "step 1", receiver, Message
    import smtplib
    try:
        s=smtplib.SMTP_SSL()
	print "step 1b after smtplib"
        s.connect("smtp.gmail.com",465)
	print "step 1c after connect"
        s.ehlo()
	print "step 1d after ehlo"
        s.starttls()
	print "step 1e after starttls"
        s.ehlo()
	print "step 2 after ehlo"
        #s.login("email@gmail.com", "password")
	s.login('from_server@danenet.org', 'messag_2.Garcia')
        print "step 3 right before sendmail"
	s.sendmail("from_server@danenet.org", receiver, Message)
    except Exception,R:
            return R

mail("jordan@danenet.org", "This is a test2")

def mail0():
  import smtplib
  s=smtplib.SMTP_SSL()
  s.connect("smpt.gmail.com", 465)

  s.login('from_server@danenet.org', 'messag_2.Garcia')
  s.sendmail("eric.howland@gmail.com", T, M)


# from http://www.pceworld.com/view/9216127
def mail(receiver,Message):
    import smtplib
    try:
        s=smtplib.SMTP()
        s.connect("smtp.gmail.com",465)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login("email@gmail.com", "password")
        s.sendmail("email@gmail.com", receiver, Message)
    except Exception,R:
            return R

import smtplib

s=smtplib.SMTP_SSL()
s.connect("smpt.gmail.com", 465)

s.login('from_server@danenet.org', 'messag_2.Garcia')
s.sendmail("eric.howland@gmail.com", T, M)

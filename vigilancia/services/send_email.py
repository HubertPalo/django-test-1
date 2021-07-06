import smtplib
import os
os.environ['JAVAPORCO_GMAIL_USER'] = 'darlinnep.extra@gmail.com'
os.environ['JAVAPORCO_GMAIL_PASSWORD'] = 'LegereGoogle6'

gmail_user = os.getenv('JAVAPORCO_GMAIL_USER')
gmail_password = os.getenv('JAVAPORCO_GMAIL_PASSWORD')

sent_from = gmail_user
to = ['darlinnep@gmail.com', 'henriquepchagas@gmail.com', 'maonamata.wm@gmail.com', 'paulakkawi@gmail.com', 'fepedrosa.eco@gmail.com', 'ri_miranda@uol.com.br']
subject = 'Super Important Message'
body = 'Hey, what\'s up?\n\n- Movement detected in trap'
email_text ="""\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)
def send_gmail_test(id_armadilha):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text + id_armadilha)
        server.close()
    except:
        print('Something went wrong...')

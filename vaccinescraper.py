# import requests
import requests
# import BeautifulSoup library to parse page
from bs4 import BeautifulSoup
# import time to wait between scrapes
import time
# import smtplib library to send email
import smtplib
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# Twilio config
toNumber = '2106431140'  # receive number
fromNumber = '6147339949'  # twilio account number
accountSid = 'AC6adc67b53b0db7357c2791b3067b5c0c'
authToken = '5c759cc18e5db6df2db08c9bf1cca117'
client = Client(accountSid, authToken)

while True:
    url = "https://covid19.sanantonio.gov/Services/Vaccination-for-COVID-19"
    # your headers like this is a browser, get from https://www.whatismybrowser.com/
    headers = {"content-type":"text"}
    # download homepage
    response = requests.get(url, headers=headers)
    # parse
    soup = BeautifulSoup(response.text, "lxml")  # install the lmxl library

    # search for text saying the vaccine reg is unavailable
    if str(soup).find("vaccine registration is temporarily unavailable") != -1:
        print("Registration unavailable")
        # wait 5 seconds to check again
        time.sleep(5)
        continue
    else:
        print("here")
        msg = 'Subject: Vaccine Registration is back!'
        fromaddr = 'PUT AN EMAIL HERE'
        toaddrs = ['jim.love@ymail.com']

        # create twilio message
        try:
            client.messages.create(to=toNumber, from_=fromNumber, body='Vaccine Registration is back!')
        except (NameError, TwilioRestException):
            pass

        # create mailing server
        server = smtplib.SMTP('smtp.gmail.com', 587) # if the sender email is not a gmail lmk
        server.starttls()
        server.login("YOUR EMAIL HERE SAME AS BEFORE", "YOUR PASSWORD TO EMAIL")
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()
        break

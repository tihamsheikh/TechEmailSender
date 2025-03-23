# An application that sends daily techmails
# from replit community

import requests, schedule, smtplib, os, time
from bs4 import BeautifulSoup
from replit import db
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def scrapingWeb():
  url = "https://replit.com/community-hub"
  
  response = requests.get(url)
  html = response.text
  
  soup = BeautifulSoup(html, "html.parser")
  myLinks = soup.find_all("a", {"class": "css-epm014"})
  
  for item in myLinks:
    db[f"{item.text}"] = f"{item['href']}"

def filterEvent():
  dict = {}
  keys = db.keys()
  for key in keys:
    dict[key] = db[key]
  return dict

def getContent():
  dict = filterEvent()
  count = 0
  email = ""
  for key in dict.keys():
    if count == 4: break
    email += f"{key}"
    email += f"{dict[key]}"
    count += 1
  return email
  
def mailing():
  username = os.environ['mailUsername']
  password = os.environ['mailPassword']
  email = getContent()
  server = "smtp.gmail.com"
  port = 587
  s = smtplib.SMTP(host=server, port=port)

  s.starttls()
  s.login(username, password)

  msg = MIMEMultipart()
  msg['To'] = username
  msg['From'] = username
  msg['Subject'] = "Daily Tech News!!"
  msg.attach(MIMEText(email, 'html'))
  s.send_message(msg)
  del msg

def sendMail():
  mailing()
  print("""
  Prepairing for today's message.....
  ....
  ...
  Done!
  Sending..
  
  Mail Sent
  """)

schedule.every(3).seconds.do(sendMail)

while True:
  schedule.run_pending()
  time.sleep(1)

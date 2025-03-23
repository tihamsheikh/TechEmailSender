# An application to send weather summary through email
# pkg smtplib, gemini, tkinter, schedule, email
# api open weather

import os, smtplib, requests, datetime, KEYS
from typing import Optional

from google import genai
from email.mime.multipart import MIMEMultipart as mime_multipart
from email.mime.text import MIMEText as mime_text
import tkinter as tk

# weather information section (1st operation)
def weather_info(city):

    api_key = KEYS.open_weather_key
    # city = "Sydney" # use as parameter | needs user input

    weather_call_url = f"https://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={city}"

    response = requests.get(weather_call_url).json()
    # print(response)
    print("Acquired weather information")
    return response

# ai summarization (2nd operation)
def summarize_weather_info(city):
    api_key = KEYS.genai_key

    client = genai.Client(api_key=api_key)

    weather_information = weather_info(city)
    # print(weather_information)

    response = client.models.generate_content(
    model="gemini-2.0-flash",
            contents=f"""
            {weather_information}
            Please summarize this json weather information and temperatures should be in celsius. 
            Also along with summarization recommend me what should I do in this weather.
            Note: Only start with weather summarization and do not add anything extra like you are responding. But do add titles like "Summarization of weather"
            and "Recommended activity", please.
            """
    )

    # print(response.text)
    content = response.text
    print("Information summarized")
    return response.text

# email sending section (3rd operation)
def email_section(username: str, password: str, client: str, city: str):

    # username = "e.zero.bd.i@gmail.com"   # user username (use as parameter) | needs user input
    # app_password = "mklt msxp krdh vsvg"   # app password (use as parameter) | needs user input
    port = 587
    host = "smtp.gmail.com"

    server = smtplib.SMTP(host=host, port=port)

    server.starttls()
    server.login(user=username, password=password)

    # client = "vincephgameing@gmail.com" # client email (use as parameter) | needs user input
    content = summarize_weather_info(city).split("\n")  # get from gemini (use as parameter)

    # email formating start
    main_content = ""
    count = 0
    template_list = [
        "<html><head></head><body><h2><strong>",
        "</strong></h2><p>",
        "</p><h3><strong>",
        "</strong></h3><p>",
        "</p></body></html>"
    ]

    for info in content:
        if info == "":
            continue
        # print(template_list[count])
        # print(info)
        main_content += template_list[count]
        main_content += info
        count += 1
    main_content += template_list[-1]

    # email formating end

    message = mime_multipart()
    message["To"] = client
    message["From"] = username
    message["Subject"] = "Weather News!!!!"
    message.attach(mime_text(main_content, "html"))

    server.send_message(message)
    server.quit()
    print("Success\nEmail sent")

#

username = "e.zero.bd.i@gmail.com"   # user username (use as parameter) | needs user input
app_password = "mklt msxp krdh vsvg"
client = "vincephgameing@gmail.com"
city = "Dhaka"

email_section(username, app_password, client, city)
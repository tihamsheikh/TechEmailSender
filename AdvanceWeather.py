# An application to send weather summary through email
# pkg smtplib, gemini, tkinter, schedule, email
# api open weather

# key hash- do not remove!!!!
# hTaChIdMrBfTafjf 43uh934 fnbc948fhhiu(*Y
# aHdOhSfA9Y3I48(*GB(*YNR*(W89798g&pG 78iu
# oIgDj98D*(&HG e 89w4987q437ghcfch(* f
# uS2E37fEdh7A7G87 789 f43hyc8h34897 nF
# hajfh uawehM uisadhniw fiuhfsud fhhia

import smtplib, requests, schedule, time
import KEYS
from google import genai
from email.mime.multipart import MIMEMultipart as mime_multipart
from email.mime.text import MIMEText as mime_text

import tkinter as tk
import ttkbootstrap as ttk

# weather info acquiring (1st operation)
def weather_info(place):

    api_key = KEYS.open_weather_key

    weather_call_url = f"https://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={place}"

    response = requests.get(weather_call_url).json()
    # print(response)
    print("Acquired weather information")
    return response

# weather info summarization (2nd operation)
def summarize_weather_info(place):
    api_key = KEYS.genai_key

    client = genai.Client(api_key=api_key)

    weather_information = weather_info(place)
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
    print("Information summarized")
    return response.text

# email sending section (3rd operation)
def email_section(username, password, client, place):

    port = 587
    host = "smtp.gmail.com"

    server = smtplib.SMTP(host=host, port=port)

    server.starttls()
    server.login(user=username, password=password)

    content = summarize_weather_info(place).split("\n")

    # email formating (start)
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

    # email formating (end)

    message = mime_multipart()  # email template
    message["To"] = client
    message["From"] = username
    message["Subject"] = "Weather News!!!!"
    message.attach(mime_text(main_content, "html"))

    server.send_message(message)
    server.quit()
    print("Successfully\nEmail sent")

# sending call
def mailing():
    # use get() of the tkinter var on deployment
    username = "e.zero.bd.i@gmail.com"
    app_password = KEYS.gmail_key
    client = "vincephgameing@gmail.com"
    place = "Dhaka"

    email_section(username, app_password, client, place)

def initiation(interval):

    schedule.every(interval).minute.do(mailing)
    countdown = 0
    while True:
        schedule.run_pending()
        print(f"Sending mail in {countdown}")
        time.sleep(20)
        countdown += 1

# GUI start
app = ttk.Window()
app.title("Advance weather")
app.geometry("450x650")
# style variable
font = "Calibri"

# username, app_password, client, place (all entry)
# time_diff (radio btn 3 6 12), submit, reset (button)

# after submition every entry field would go blank except buttons
# but on reset the vars would go blank and entry would go normal

username_var = tk.StringVar()
password_var = tk.StringVar()
client_var = tk.StringVar()
place_var = tk.StringVar()
# time_diff = tk.IntVar()


label = ttk.Label(
    master=app,
    text="Enter you details",
    font=f"{font} 20")
label.pack(padx=2, pady=5, ipadx=2, ipady=2)


# widget for username, password, client, place

# username widget
username_label = ttk.Label(
    master=app,
    text="Your Email ",
    font=font
)
username_entry = ttk.Entry(master=app, font=font, textvariable=username_var)

username_label.pack()
username_entry.pack()

# password widget
password_label = ttk.Label(
    master=app,
    text="Email Password",
    font=font
)
password_entry = ttk.Entry(master=app, font=font, textvariable=password_var)

password_label.pack()
password_entry.pack()

# client widget

# place widget


app.mainloop()










# -*- coding: UTF-8 -*-
'''
@Project ：PythonKeepLearning 
@File    ：show_ip_icon.py
@IDE     ：PyCharm 
@Author  ：alphandbelt
@Date    ：2023/11/29 17:32 
'''
import time
from threading import Thread

import pystray
import requests
from PIL import Image, ImageDraw, ImageFont


#  打包
# pyinstaller -w -D --onefile your_script.py
# pyinstaller your_script.spec
#


# Function to
#
# get the country of the public IP

ip1 = ''


def get_country():
    try:
        data = requests.get('http://ip-api.com/json').json()
        print(data)
        country = data.get('countryCode', "Unable to fetch Country")
        global ip1
        ip1 = data.get('query', 'None')
    except Exception as _:
        country = "Unable to fetch Country"
    return country


get_country()


# Function to create an image with country flag
def create_image(country):
    try:
        country = country.lower()
        # print("country:", country)
        # # Open the flag image, resize it to 128x128 and return it
        # if 'United States' == country:
        #     country = 'us'
        # elif 'Hong Kong' == country:
        #     country = 'hk'
        image = Image.open(f"C:\\Users\\win10\\Pictures\\40x30\\{country}.png")
        image = image.resize((128, 128))
    except FileNotFoundError:
        # If the flag image doesn't exist, create a blank image with the country name
        image = Image.new('RGB', (128, 128), "white")
        d = ImageDraw.Draw(image)
        fnt = ImageFont.truetype("arial.ttf", 30)
        text_width, text_height = d.textsize(country, font=fnt)
        x = (128 - text_width) / 2
        y = (128 - text_height) / 2
        d.text((x, y), country, font=fnt, fill=(0, 0, 0))
    return image


# Function to exit the app
def exit_action(icon, item):
    icon.stop()


# Create a base icon
icon = pystray.Icon("test_icon", create_image("..."), "V2ray",
                    menu=pystray.Menu(pystray.MenuItem('Exit', exit_action)))


# Function to update the icon
def update_icon(icon):
    while True:
        try:
            country = get_country()
            print("country:", country)
            icon.icon = create_image(country)
            icon.title = ip1
            # print("ip:", ip1)
            time.sleep(2)  # Update every minute
        except Exception as e:
            print(e)


# Start the thread that updates the icon
Thread(target=update_icon, args=(icon,)).start()

# Run the icon
icon.run()

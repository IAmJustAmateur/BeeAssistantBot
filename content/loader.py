import os
import logging

from content.bot_content import Bot_Content

from content.csv_content_loader import content_loader

from bd_api_services.users_base import Users_Base

content_folder = os.path.join("dialogs")
content_dict = {

    "Bot Intro": "Bot Intro.csv",
    "User Intro": "User Intro.csv",

}

try:
    bot_content = Bot_Content(content_loader=content_loader, content_sources=content_dict, content_folder= content_folder)
    logging.info("content loaded")
except:
    bot_content = None

users_base = Users_Base()

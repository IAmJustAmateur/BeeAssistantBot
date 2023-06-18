from collections import namedtuple
from typing import List, Dict, Callable
import logging

from content.topics_questions import Question


from content.bot_commands import Bot_Command
from content.content_parts import Content_Part


from misc.utils import get_cell_value, get_json_value, pad_or_truncate

from states.dialog_states import DialogStateNames

class Bot_Content():
    def __init__(
            self,
            content_loader: Callable[[Dict, str], Dict[str, Content_Part]],
            content_sources: Dict,
            content_folder: str
        ):
        self.content_sources = content_loader(content_sources, content_folder)
        logging.info("content sources set")

        self.load_bot_intro()
        self.load_user_intro()
        self.load_commands()
        #self.load_topic_selection()
        #self.load_topics()

        logging.info("content loaded")

    def load_commands(self):
        self.bot_commands = (
            Bot_Command("start", "start bot"), # start
        )

    def load_bot_intro(self):
        content_part: Content_Part = self.content_sources["Bot Intro"]
        bot_intro_cells = content_part.Body

        self.bot_intro: List[Question] = []
        messages: List[str] = []
        for row in bot_intro_cells:
            row = pad_or_truncate(row, 5)
            bot_message_text =  row[0]

            answer_options = get_json_value(row[1])

            messages.append(bot_message_text)
            if answer_options is not None:
                question = Question(messages, answer_options)
                self.bot_intro.append(question)
                messages = []

    def load_user_intro(self):
        content_part: Content_Part = self.content_sources["User Intro"]
        user_intro_cells  = content_part.Body
        self.user_intro: List[Question] = []
        for row in user_intro_cells:
            row = pad_or_truncate(row, 3)
            bot_message =  row[0]
            answer_options = get_json_value(row[1])
            user_var = get_cell_value(row[2])

            question = Question([bot_message], answer_options=answer_options,
                                user_var = user_var)
            self.user_intro.append(question)

    def load_topic_selection(self):
        content_part: Content_Part = self.content_sources["Topic Selection"]
        cells = content_part.Body
        self_topic_selection = List[Question]

    def load_topics(self):
        content_part: Content_Part = self.content_sources["Topics"]
from copy import copy
from asyncio import sleep

import logging

from aiogram import Bot, types
from typing import Any, List, Callable, Optional, Dict, Tuple

from handlers.bot_keyboards import create_keyboard, ReplyKeyboardRemove

Context = Dict


class Question():
    def __init__(self, messages: List[str],
                answer_options: List[str] | Dict |None,
                user_var: Optional[str|List[str]] = None,
                ):

        self._messages = messages
        self._answer_options = answer_options
        self. _user_var = user_var
        self._answer = None

    @property
    def answer(self):
        if self._answer:
            return self._answer
        return None

    @property
    def var(self):
        if self._user_var:
            return self._user_var
        return None

    @answer.setter
    def answer(self, value: str):
        self._answer = value.lower().capitalize()

    @property
    def user_var(self):
        if self._user_var:
            return self._user_var
        return None

    def set_var(self):
        if self._user_var:
            if type(self.answer_options) == dict:
                options = [option.lower() for option in list(self.answer_options.keys())]
                if self._answer.lower() in options:
                    self._answer = self.answer_options[self._answer.capitalize()]
    @property
    def answer_options(self):
        if type(self._answer_options):
            return self._answer_options
        return None

    async def send_messages(self, bot: Bot, user_id, context: dict):

        for bot_message in self._messages[:-1]:
            await bot.send_message(user_id, bot_message, reply_markup=ReplyKeyboardRemove())
            await sleep(0.5)

        if isinstance(self, TopicSelectionQuestion):
            answer_options = self.select_answer_options(context["user_level"])
        else:
            answer_options = self.answer_options

        kb = create_keyboard(answer_options, row_width=1)
        await bot.send_message(user_id, self._messages[-1], reply_markup=kb)


class TopicSelectionQuestion(Question):

    def __init__(
                    self,
                    messages: List[str],
                    answer_options: List[str] | Dict |None,
                    user_var: Optional[str|List[str]] = None,
                ):

        self._messages = messages

        tmp_answer_options = dict()
        for key in answer_options.keys():
            v = answer_options[key]
            answer_option = dict()
            for i in range(len(v)):
                answer_option[v[i]] = v[i]
            tmp_answer_options[key] = answer_option

        self._answer_options = dict(tmp_answer_options)

        self. _user_var = user_var
        self._answer = None

    def select_answer_options(self, var_value) -> Dict:
        answer_options = self.answer_options[var_value]
        return answer_options


class Topic():
    def __init__(self, name: str,  title: str, url: str):
        self.name = name
        self.title = title
        self.url = url

from typing import Dict, Any
import logging
from aiogram.dispatcher import FSMContext

from content.topics_questions import Question, Topic

from states.states import get_state_name

class Context():
    def __init__(self):
        self._context = dict()

    def set_state(self, state_name: str):
        self._context["state"] = state_name

    def set_question_index(self, question_index: int):
        self._context["question_index"] = question_index

    def get_question_index(self):
        return self._context["question_index"]

    def set_state(self, state: FSMContext, user_id):
        state_name = get_state_name(state=state, user_id=user_id)
        self._context["state"] = state_name

    def set_user_var(self, question: Question):
        self._context[question.user_var] = question.answer

    def get_user_var(self, question: Question) -> Any:
        return self._context[question.user_var]

    def get_context(self) -> Dict:
        return self._context

    def add_topic(self, topic: Topic):
        self._context["topic name"] =topic.name
        self._context["topic url"] = topic.url

    def add_user_id(self, user_id):
        self._context["user_id"] = user_id

    def reset(self):
        self._context = {}

async def get_context(state: FSMContext) -> Context:
    data = await state.get_data()
    try:
        context = Context()
        context._context = data['context']

    except KeyError:
        context = Context()
    return context


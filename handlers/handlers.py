from typing import Union
import logging

import asyncio

from aiogram import types, Bot
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from content.bot_content import Bot_Content
from content.loader import bot_content, users_base

from content.topics_questions import Question, Topic

from states.states import Bot_States
from states.dialog_states import DialogStateNames

from users.users import User

from handlers.context import Context, get_context


async def update_user_dialog_context(
    state: FSMContext,
    bot_state: State,
    context: Context, user: User
):
    """Update user dialog context"""

    await state.set_state(bot_state)
    context.set_state(state, user.id)
    await state.update_data({"context": context.get_context()})


async def send_farewell(
    state: FSMContext,
    bot: Bot,
    context: Context,
    user: User):
    """ farewell """
    question: Question = bot_content.get_dialog(DialogStateNames.Farewell)
    await question.send_messages(bot, user.id, context.get_context())
    await state.reset_state()


async def send_topic(topic: Topic, state: FSMContext,
                     context: Context, user: User,
                     message: Union[types.Message, types.CallbackQuery]):
    if topic is None:
        await send_farewell(state, message.bot, context, user)
        return


    topic_dialog:Question = bot_content.get_dialog(DialogStateNames.TopicSelection)
    await topic_dialog.send_messages(message.bot, message.from_user.id, context=context.get_context())

    await update_user_dialog_context(state, Bot_States.TopicReading,
                                             context, user)


async def start(message: types.Message, state: FSMContext='*'):

    bot_intro = bot_content.bot_intro
    question: Question = bot_intro[0]
    await question.send_messages(message.bot, message.from_user.id, context ={})

    user = User(message.from_user.id)
    #user.create_by_id()

    context = Context()
    context.set_question_index(0)

    await update_user_dialog_context(
        state,
        Bot_States.BotIntro,
        context,
        user
    )

async def bot_intro(callback_query: types.CallbackQuery, state: FSMContext):
    logging.info(f"BotIntro, {callback_query.data}, user: {callback_query.from_user.id}")
    bot_intro_dialog = bot_content.bot_intro
    user = User(callback_query.from_user.id)

    context = await get_context(state)
    question_index = context.get_question_index()
    question: Question = bot_intro_dialog[question_index]
    question.answer = callback_query.data

    if question_index < len(bot_intro_dialog) - 1:

        question_index +=1
        question = bot_intro_dialog[question_index]
        await question.send_messages(callback_query.bot, callback_query.from_user.id, context=None)
        context.set_question_index(question_index)
        await update_user_dialog_context(
            state,
            Bot_States.BotIntro,
            context,
            user
        )

    else: # last question

        user_intro = bot_content.user_intro
        question: Question = user_intro[0]
        question_index = 0
        await question.send_messages(callback_query.bot, callback_query.from_user.id, context.get_context())
        context.set_question_index(question_index)
        await update_user_dialog_context(state, Bot_States.UserIntro,
                                            context,  user)


async def user_intro_message(message: types.Message, state: FSMContext) :
    logging.info(f"UserIntro, message: {message.text}, user: {message.from_user.id}")

    await user_intro_answer(message, user_id = message.from_user.id, user_answer=message.text, state=state)

async def user_intro_callback(callback_query: types.CallbackQuery, state: FSMContext):
    logging.info(f"UserIntro, callback: {callback_query.data}")

    await user_intro_answer(callback_query, user_id=callback_query.from_user.id, user_answer=callback_query.data, state=state)

async def user_intro_answer(message: Union[types.Message, types.CallbackQuery], user_id: int, user_answer: str, state: FSMContext):

    context = await get_context(state)
    question_index = context.get_question_index()
    question: Question = bot_content.user_intro[question_index]
    user = User(message.from_user.id)

    question.answer = user_answer

    context.set_user_var(question)

    await next_question(message.bot,
                        user_id = user_id,
                        user_answer=user_answer,
                        question=question,
                        question_index=question_index,
                        context=context,
                        state=state
                        )


async def next_question(bot: Bot, user_id: int, user_answer: str, question: Question, question_index: int, context: Context, state=FSMContext):

    user_intro = bot_content.user_intro
    user = User(user_id)

    #user.set_user_var(question)

    question_index +=1
    context.set_question_index(question_index)
    context.set_user_var(question)
    question: Question = user_intro[question_index]

    if question_index == len(user_intro) - 1:  # last question
        await update_user_dialog_context(state, Bot_States.TopicSelection, context, user)

    else:
        await update_user_dialog_context(state, Bot_States.UserIntro, context, user)

    await question.send_messages(bot, user_id, context = context.get_context())

async def topic_selection(callback_query: types.CallbackQuery, state: FSMContext):
    logging.info(f"TopicSelection, {callback_query.data}, user: {callback_query.from_user.id}")
    #topic_selection = bot_content.topic_selection
    user = User(callback_query.from_user.id)

    context = await get_context(state)


from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


class Bot_States(StatesGroup):
    BotIntro = State()
    UserIntro = State()
    TopicSelection = State()
    ContinueOrNot = State()
    Sleep = State()


def get_state_name(state: FSMContext, user_id: int):
    try:
        state_name = state.storage.data[str(user_id)][str(user_id)] \
            ['state'].split(':')[1]
    except KeyError:
        state_name = None
    return state_name


def get_bot_state_name(state: State):
    state_name = state.state.split(':')[1]
    return state_name

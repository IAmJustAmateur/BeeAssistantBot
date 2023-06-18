import pytest
from unittest.mock import AsyncMock
from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bd_api_services.users_base import Users_Base



from config import BOT_TOKEN
from content.bot_content import Bot_Content

from content.csv_content_loader import content_loader

content_folder = "Dialogs"
content_dict = {

    "Bot Intro": "Bot Intro.csv",
    "Commands": "Dialogs-Commands.csv",
    "Contents": "Dialogs-Contents.csv",
    "Entertainments": "Dialogs-Entertainments.csv",
    "Phrases": "Dialogs-Phrases.csv",
    "Quizs": "Dialogs-Quizs.csv",
    "Tasks": "Dialogs-Tasks.csv",
    "User Intro": "Dialogs-User Intro.csv",
    "Weather": "Dialogs-Weather.csv",
}

@pytest.fixture(scope='session')
def bot_content() -> Bot_Content:
    bc =  Bot_Content( content_sources=content_dict, content_loader=content_loader, content_folder=content_folder)
    return bc

@pytest.fixture(scope='function')
def dp() -> Dispatcher:
    bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
    storage = MemoryStorage()
    return Dispatcher(bot, storage=storage)

@pytest.fixture(scope='session')
def base() -> Users_Base:
    users_base = Users_Base()
    return users_base

@pytest.fixture(scope="function")
def test_user1(base: Users_Base):
    test_user_id = 666666
    try:
        base.delete_bot_user(test_user_id)
    except:
        pass
    user_info = {
        "user_name": "simple user",
        "location": {
            "country": "Польша",
            "code": "PL",
            "city": "Bialystok",
            "coordinates": {
                "lat": 50.4928426,
                "lon": 23.9402125
            }
        },
        "user_data": {"sex": "male"}
    }
    base.create_bot_user(test_user_id, user_info)
    return test_user_id

@pytest.fixture(scope="function")
def test_user2(base: Users_Base):
    test_user_id = 77777
    try:
        base.delete_bot_user(test_user_id)
    except:
        pass
    user_info = {
        "user_name": "simple user",
        "location": {
            "country": "Польша",
            "code": "PL",
            "city": "Bialystok",
            "coordinates": {
                "lat": 50.4928426,
                "lon": 23.9402125
            }
        }
    }
    base.create_bot_user(test_user_id, user_info)
    return test_user_id

@pytest.fixture(scope='function')
def handlers_test_user(base: Users_Base) -> int:
    test_user_id = 8888888
    try:
        base.delete_bot_user(test_user_id)
    except:
        pass
    user_info = {
        "user_name": "simple user",
        "location": {
            "country": "Польша",
            "code": "PL",
            "city": "Bialystok",
            "coordinates": {
                "lat": 50.4928426,
                "lon": 23.9402125
            }
        }
    }

    base.create_bot_user(test_user_id, user_info)
    return test_user_id

@pytest.fixture(scope='function')
def state(dp: Dispatcher, handlers_test_user: int) -> FSMContext:
    state = FSMContext(
        storage = dp.storage,
        user = handlers_test_user,
        chat = handlers_test_user,
    )
    return state

@pytest.fixture(scope='function')
def callback_query(handlers_test_user: int) -> AsyncMock:
    cq = AsyncMock()
    cq.from_user.id = handlers_test_user
    cq.bot = AsyncMock()
    return cq

@pytest.fixture(scope='function')
def message(handlers_test_user: int) -> AsyncMock:
    m = AsyncMock()
    m.from_user.id = handlers_test_user
    m.bot = AsyncMock()
    return m
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import BotCommand

from aiogram.contrib.fsm_storage.memory import MemoryStorage


from config import BOT_TOKEN, admin_id

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(level=logging.INFO, format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s')

from handlers.handlers import (start, bot_intro, user_intro_message, user_intro_callback, topic_selection, bot_content)
from states.states import Bot_States


bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def on_startup(dp: Dispatcher):

    await bot.send_message(admin_id, "Bot launched. Start working")
    commands_for_bot = [BotCommand(command = cmd.command, description = cmd.brief) for cmd in bot_content.bot_commands]
    await dp.bot.set_my_commands(commands_for_bot)


    dp.register_message_handler(start, state='*', commands=["start"])
    dp.register_callback_query_handler(bot_intro, state=Bot_States.BotIntro)
    dp.register_message_handler(user_intro_message, state=Bot_States.UserIntro)
    dp.register_callback_query_handler(user_intro_callback, state=Bot_States.UserIntro)
    dp.register_callback_query_handler(topic_selection, state=Bot_States.TopicSelection)


if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True, on_startup = on_startup)

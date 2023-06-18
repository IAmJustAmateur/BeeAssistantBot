
from typing import Dict, List
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardRemove,
                           InlineKeyboardMarkup, InlineKeyboardButton)

def create_keyboard_markup(answer_options: List) -> ReplyKeyboardMarkup:
    '''
    create keyboard
    '''

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    buttons: List[KeyboardButton] = []
    for key in answer_options:
        btn: KeyboardButton = KeyboardButton(key)
        buttons.append(btn)
    row_buttons = [buttons[x:x+2] for x in range(0, len(buttons), 2)]
    for row in row_buttons:
        if len(row) == 2:
            keyboard.row(row[0], row[1])
        else:
            keyboard.row(row[0])

    return keyboard


def create_inline_keyboard(answer_options: Dict,  row_width = 2) -> InlineKeyboardMarkup:
    '''
    create inline keyboard
    '''
    inline_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width = row_width)
    buttons: List[InlineKeyboardButton] = []
    for key in answer_options:
        inline_btn: InlineKeyboardButton = InlineKeyboardButton(key, callback_data=answer_options[key])
        buttons.append(inline_btn)
    row_buttons = [buttons[x:x+row_width] for x in range(0, len(buttons), row_width)]
    for row in row_buttons:
        if len(row) > 1:
            buttons = []
            for i in range(row_width):
                try:
                    buttons.append(row[i])
                except:
                    pass
            inline_kb.row(*buttons)
        else:
            inline_kb.row(row[0])

    return inline_kb


def create_keyboard(answer_options, row_width = 2):
    if answer_options is None:
        return ReplyKeyboardRemove()
    if type(answer_options) == list:
        return create_keyboard_markup(answer_options=answer_options)
    elif type(answer_options) == dict:
        return create_inline_keyboard(answer_options=answer_options, row_width = row_width)
    elif type(answer_options) == str:
        return create_keyboard_markup(answer_options=[answer_options])
    return

def create_yes_no_keyboard():
    answer_options = {'Yes': 'Yes', 'No': 'No'}
    return create_inline_keyboard(answer_options=answer_options, row_width=2)

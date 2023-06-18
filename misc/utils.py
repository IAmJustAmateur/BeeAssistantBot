from typing import Dict, List, Any
import json
import re
from datetime import datetime
from timezonefinder import TimezoneFinder


import pytz


def get_cell_value(cell: Any) -> Any | None:
    '''
    return google spreadsheet cell value or None
    '''
    if cell:
        return cell
    return None


def get_user_variables(cell: Any) -> str | List[str] | None:
    '''
    return user variable or user variable list
    '''
    if cell:
        variables = list(map(lambda s: s.strip(), cell.split(",")))
        if len(variables) == 1:
            return variables[0]
        else:
            return variables
    else:
        return None


def get_json_value(cell: str | None) -> List | Dict | str | None:
    if not cell:
        return None
    try:
        result = json.loads(cell)
    except:
        result = cell
    return result


def get_options_list(cell_value: str | None) -> List[str] | Dict | None:
    '''
    return Dict if cell_value is Dict
    if not split str by \n

    '''
    if not cell_value:
        return None

    try:
        d = get_json_value(cell_value)
        if type(d) == dict:
            return d
    except:
        pass

    options = list(map(lambda s: s.strip(), cell_value.split("\n")))
    return options


def quiz_answer_options(cell_value: str | None) -> Dict | None:
    '''
    split str by \n

    '''
    if not cell_value:
        return None
    options = {}
    option_list = list(map(lambda s: s.strip(), cell_value.split("\n")))
    for option in option_list:
        options[option] = option
    return options


def list_from_long_str(s: str, delimeter: str) -> List[str] | str | None:
    '''
    split str by delimeter
    '''
    if not str:
        return None
    if str == "":
        return None
    ls = s.split(delimeter)
    if ls[0].startswith(delimeter):
        ls[0] = ls[0][1:]
    if len(ls) == 1:
        return ls[0]
    return ls


def flat_list(options: List[Any] | Dict) -> List[str]:
    '''
    create flat_list from list which contains:
    - lists of str
    - str
    - int
    '''
    result: List[str] = []
    if type(options) == list:
        for list_item in options:
            if type(list_item) == list:
                for item in list_item:
                    result.append(str(item).lower())
            elif type(list_item) == str:
                result.append(list_item.lower())
            elif type(list_item) == int:
                result.append(str(list_item))

    elif type(options) == dict:
        for option in list(options.values()):
            result.append(str(option).lower())

    return result


def merge_dict(d1: Dict, d2: Dict) -> Dict:
    '''
    merge 2 dictionary
    '''
    if d1 is None:
        return d2
    if d2 is None:
        return d1

    return dict(d1, **d2)


def get_utc_time_str(coords: Dict, time_str: str):
    '''
    transform time_str into UTC time_str using coordinates

    '''
    timezone_str = get_timezome(coords)
    timezone = pytz.timezone(timezone_str)

    if ":" in time_str:
        delimeter = ":"
    elif "." in time_str:
        delimeter = '.'
    elif "-" in time_str:
        delimeter = '-'

    h, m = [int(x) for x in time_str.split(delimeter)[0:2]]

    dt = datetime.now()
    dt = dt.replace(hour=h, minute=m, second=0)
    dt = timezone.localize(dt)
    # to_zone = tz.gettz('UTC')
    to_zone = pytz.timezone('UTC')
    utc = dt.astimezone(to_zone)
    utc_time_str = f'{str(utc.hour).zfill(2)}:{str(utc.minute).zfill(2)}'

    return  utc_time_str


def process_wakeup_time(time_str: str) -> str:
    '''
    process time_str, round up to 15 minutes

    '''
    hours_minutes: List = re.split('[-:.\s]\s*', time_str)
    if (len(hours_minutes) < 2):
        return None

    if len(hours_minutes[1]) < 2:
        return None

    try:
        hours = int(hours_minutes[0])
        minutes = int(hours_minutes[1])
    except:
        return None
    if hours < 0 or hours > 24:
        return None
    if minutes < 0 or minutes >= 60:
        return None
    if minutes < 8:
        minutes = 0
    elif minutes < 23:
        minutes = 15
    elif minutes < 38:
        minutes = 30
    elif minutes < 53:
        minutes = 45
    else:
        minutes = 0
        hours += 1
        if hours >= 24:
            hours -= 24
    wakeup_time: str = f'{str(hours).zfill(2)}:{str(minutes).zfill(2)}'

    return wakeup_time


def int_from_answer(answer) -> int | None:
    try:
        value = int(answer)
        return value
    except:
        return None


def return_self(answer: Any) -> Any:
    return answer


def pad_or_truncate(some_list: list[str], target_len):
    '''
    truncate some list to target_len
    or
    add empty strings

    '''
    return some_list[:target_len] + ['']*(target_len - len(some_list))


def get_timezome(coords: Dict) -> str:
    '''
    return time zone from coordinates
    '''

    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=coords['lon'], lat=coords['lat'])

    return timezone_str

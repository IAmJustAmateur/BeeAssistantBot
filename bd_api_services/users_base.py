from typing import Dict, List
import logging
from datetime import datetime, timezone
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_TABLE


class Base_Exception(Exception):
    def __init__(self, message='database access error') -> None:
        self.message = message
        super().__init__(self.message)


class User_Data_Exception(Exception):
    def __init__(self, message = 'database structure error') -> None:
        self.message = message
        super().__init__(self.message)


class Users_Base:
    def __init__(self):
        url = SUPABASE_URL
        key = SUPABASE_KEY
        self.supabase: Client = create_client(url, key)
        self.table = self.supabase.table(SUPABASE_TABLE)

    def bot_user_exists(self, user_id):

        data = self.table.select("*").eq("id", user_id).execute()
        if len(data.data) > 0:
            return True
        return False

    def create_bot_user(self, user_id, user_info: Dict = {}):
        # time_update = str(datetime.now(timezone.utc))
        # request = dict({"id": user_id}, **dict(user_info, **{"time_update": time_update}))
        request = dict({"id": user_id})
        try:
            # replace with upsert
            data, count = self.table.insert(request).execute()
            return data
        except Exception as e:
            logging.info(e)
            raise Base_Exception

    def delete_bot_user(self, user_id):
        try:
            self.table.delete().match({"id": user_id}).execute()
        except Exception:
            raise Base_Exception

    def update_user_info(self, user_id, user_info: Dict):

        try:
            data = self.table.update(user_info).eq("id", user_id).execute()
            return data
        except Exception as e:
            logging.debug(e)
            raise Base_Exception

    def get_user_info(self, user_id) -> Dict:
        try:
            data = self.table.select("*").eq("id", user_id).execute()
        except Exception as e:
            logging.debug(e)
            raise Base_Exception
        try:
            user_info = data.data[0]
            return user_info
        except Exception as e:
            logging.debug(e)
            raise User_Data_Exception

    def set_user_var(self, user_id, var, value):
        try:
            user_info = self.get_user_info(user_id)
            user_data = user_info["user_data"]
            if user_data is None:
                user_data = {}
            user_data[var] = value
            user_info["user_data"] = user_data
            self.update_user_info(user_id, user_info)
        except Exception as e:
            logging.debug(e)
            raise e

    def reset_user(self, user_id):
        self.update_user_info(user_id, user_info=None)


from content.topics_questions import Question

from content.loader import users_base


class User():
    def __init__(self, user_id):
        self.id = user_id

    def get_user_info(self):
        self.user_info = users_base.get_user_info(self.id)

    def create_by_id(self):
        if not users_base.bot_user_exists(self.id):
            users_base.create_bot_user(self.id)

    def set_user_var(self, question: Question):

        users_base.set_user_var(self.id, question.var, question.answer)

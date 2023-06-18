from bd_api_services.users_base import Users_Base

users_base = Users_Base()

def test_create_client():
    user_id = 11111
    users_base.create_bot_user(user_id)


import vk_api,os
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv('.env'))


def send_message_user(user_id, message, keyboard=None):
  session = vk_api.VkApi(token=os.getenv('__TOKEN__'))
  session.method('messages.send',{'user_id': user_id, 'message': message, 'random_id': 0, 'keyboard' : keyboard})
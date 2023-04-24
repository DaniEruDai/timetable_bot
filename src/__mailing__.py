import vk_api
from vk_api.keyboard import VkKeyboard,VkKeyboardColor
from vk.database import DB
import os
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv('__additional_files__\\.env'))

def start_keyboard():
  keboard = VkKeyboard(one_time=True)
  keboard.add_button('Начать',VkKeyboardColor.POSITIVE)
  return keboard


def send_message_user(user_id, message,keyboard=False):
  session = vk_api.VkApi(token=os.getenv('__TOKEN__'))
  session.method('messages.send',{'user_id': user_id, 'message': message, 'random_id': 0, 'keyboard': keyboard})
  

def main():
  start_key = start_keyboard()
  database = DB('..\data.db')
  while True:
    text = input("Введите текст сообщения для рассылки\n@ ")
    for user_id in database.get_all_ids('user'):
      send_message_user(user_id,text, keyboard = start_key)
  
if __name__ == '__main__':
  main()
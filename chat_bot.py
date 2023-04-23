from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv('__additional_files__\\.env'))

import os
from vk.database import DB

from schedule.kgtt.timetable import TimeTable
import json

from vkbottle.bot import Bot,Message



bot = Bot(token=os.getenv('__TOKEN__'))
database = DB('data.db')

def _get_keys():
  with open('timetable.json','r',encoding='utf-8') as js:
    dictionary = json.loads(js.read())
  return tuple(dictionary.keys())

@bot.on.chat_message(text = ["!изменить <item>","!изменить"])
async def edit_object_handler(message: Message, item = None):
  database.init_new_chat(message.chat_id)
  if item is not None and item in _get_keys():
    database.update_field(id = message.chat_id,
                                  table_name='chat',
                                  category='object',
                                  new = item)
    await message.answer('Объект изменен')
  else:
    await message.answer('Такого объекта нет')

@bot.on.chat_message(text = ["!конфиг <item>","!конфиг"])
async def edit_config_handler(message: Message, item = None):
  database.init_new_chat(message.chat_id)
  
  default = database.get_information_from('chat',message.chat_id)['object']
  config = database.get_information_from('chat',message.chat_id)['config']
  if default:
    if item is not None:
      database.update_field(id = message.chat_id,
                                    table_name='chat',
                                    category='config',
                                    new = item)
      await message.answer('Конфигурация изменена')
    else:
      await message.answer(f'Конфигурация для {default}\n{config}')
  else:
    await message.answer('Для начала настройте объект\nЭто можно сделать при омощи команды : !изменить')

@bot.on.chat_message(text = "!р")
async def timetable_handler(message: Message):
  database.init_new_chat(message.chat_id)
  default = database.get_information_from('chat',message.chat_id)['object']
  config = database.get_information_from('chat',message.chat_id)['config']
  if default:
    text = TimeTable('timetable.json',default=default,config_string=config).get_text()
    await message.answer(text)
  else : 
    await message.answer('Для начала настройте объект\nЭто можно сделать при помощи команды : !изменить')

@bot.on.chat_message(text = ["!помощь","!help","/help"])
async def help_handler(message: Message):
  await message.answer('Краткое описание команд : \n1.!изменить - изменяет объект рассылки для чата\n2.!конфиг - изменяет конфигурацию для объекта рассылки\n3.!р - присылает расписание для объекта с учётом конфигурации\n\nБолее подробно : \nvk.com/@schedule_kgtt-raspisanie-dlya-chatov')

@bot.on.chat_message(text = ["!сброс"])
async def help_handler(message: Message):
  database.delete_chat(message.chat_id)
  await message.answer('Настройки сброшены!')

bot.run_forever()
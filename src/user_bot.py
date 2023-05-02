from ruobr_api.ruobr_api import Ruobr, RuobrException, get_tomorrow
from schedule.timetable import Timetable,get_dict
from schedule.tjson import *

import os

from vk.UserBot import UserBot

from vk.ctx import CtxStorage
from vk._keyboards import UserKeyboards
from vk._states import States

import json
import emoji
from io import BytesIO
from datetime import datetime


from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv('.env'))

_json = os.getenv('js_path')
_db = os.getenv('db_path')

bot = UserBot(_db,'user',os.getenv('TOKEN'))
Ctx = CtxStorage()


def _get_keys() -> tuple:
  with open(_json, 'r', encoding='utf-8') as js:
    dictionary = json.loads(js.read())
  return tuple(dictionary.keys())

class Utilities:

  @bot.on.message('!json')
  def service_reload(self):
    if self.user_id == 435170678:
      bot.utils.send_message('Ожидайте...')
      write_json(_json,get_dict())
      bot.utils.send_message('JSON перезаписан!')

  @bot.on.message('!р', '!расписание', '/р', '/расписание')
  def send_shedule(self):
    if self.object:
      text = Timetable(_json, self.object, self.config).get_text()
      bot.utils.send_message(text)
    else:
      bot.db.set_state(States.REGISTER[0])
      bot.utils.send_message('Объект для рассылки не найден\nПриступаем к регистарции!', keyboard = UserKeyboards.OK)

  @bot.on.message('Начать', 'Начало', 'Старт', '/start', '/Начать')
  def start(self):
    bot.utils.send_message('За работу!', keyboard =UserKeyboards.MAIN_MENU)

  @bot.on.message('!сброс', '/сброс')
  def reset(self):
    bot.db.set_state(States.MAIN_MENU)
    bot.db.delete_user()
    bot.utils.send_message('Все данные успешно удалены!', keyboard =UserKeyboards.MAIN_MENU)

  @bot.on.message(emoji.emojize(':hollow_red_circle:'))
  def back(self):
    bot.db.set_state(States.MAIN_MENU)
    bot.utils.send_message('Главное меню', keyboard =UserKeyboards.MAIN_MENU)

class Main:

  @bot.on.multiply(['Расписание'], [States.MAIN_MENU])
  def schedule(self):
    bot.db.set_state(States.SCHEDULE_MENU)
    bot.utils.send_message('Раздел с расписанием', keyboard =UserKeyboards.SCHEDULE)

  @bot.on.multiply(['Оценки'], [States.MAIN_MENU])
  def marks(self):
    if self.ruobr_login and self.ruobr_password:
      bot.db.set_state(States.MARKS_MENU)
      bot.utils.send_message('Напишите дату или выберите один из нескольких вариантов', keyboard =UserKeyboards.EVALUATION)
    else:
      bot.db.set_state(States.RUOBR_REGISTER[0])
      bot.utils.send_message('Для работы раздела необходимо зайти в Cabinet Ruobr!', keyboard =UserKeyboards.OK)

  @bot.on.multiply([emoji.emojize(':gear:')], [States.MAIN_MENU])
  def parameters(self):

    fullname = bot.utils.get_fullname()
    text = f"{fullname}\n\nОбъект таблицы : {self.object}\nКонфигурация расписания : \n{self.config}\nЛогин : {self.ruobr_login}\nПароль : {self.ruobr_password}"

    bot.db.set_state(States.PARAMETERS_MENU)
    bot.utils.send_message(text, keyboard =UserKeyboards.PARAMETERS)

class Parameters:
  @bot.on.multiply(['Изменить логин и пароль Ruobr'], [States.PARAMETERS_MENU])
  def edit_pl(self):
    bot.db.set_state(States.RUOBR_REGISTER[0])
    bot.utils.send_message('Начнем!', keyboard =UserKeyboards.OK)

  @bot.on.multiply(['Изменить конфиг'], [States.PARAMETERS_MENU])
  def edit_configuration(self):
    bot.db.set_state(States.EDIT_CONF[0])
    bot.utils.send_message('Начнем!', keyboard =UserKeyboards.OK)

  @bot.on.multiply(['Изменить объект'], [States.PARAMETERS_MENU])
  def edit_object(self):
    bot.db.set_state(States.REGISTER[0])
    bot.utils.send_message('Начнем!', keyboard =UserKeyboards.OK)

  @bot.on.multiply(['Помощь'], [States.PARAMETERS_MENU])
  def helps(self):
    text = "Дополнительные команды\n\n!сброс - Полностью сбрасывает все параметры пользователя\n\nВопросы можете задать тут :"
    bot.utils.send_message(text, url='https://vk.com/topic-214878797_49282332')

class Schedule:
  @bot.on.multiply(['Рассылка'], [States.SCHEDULE_MENU])
  def mailing(self):
    if self.object:
      bot.db.set_state(States.MAILING_MENU)
      bot.utils.send_message('Всё окей!', keyboard =UserKeyboards.MAILING)

    else:
      bot.db.set_state(States.REGISTER[0])
      bot.utils.send_message('Объект для рассылки не найден\nПриступаем к регистарции!', keyboard =UserKeyboards.OK)

  @bot.on.multiply(['Предсказания'], [States.SCHEDULE_MENU])
  def prediction(self):
    if self.ruobr_login and self.ruobr_password:
      bot.db.set_state(States.PREDICTION_MENU)
      bot.utils.send_message(                   'Раздел "Предсказания" позволяет получить расписание из "Ruobr" по дате, однако стоит учитывать, что оно может быть неточным.',
                   keyboard =UserKeyboards.PREDICTION)
    else:
      bot.db.set_state(States.RUOBR_REGISTER[0])
      bot.utils.send_message('Для работы раздела необходимо зайти в Cabinet Ruobr!', keyboard =UserKeyboards.OK)

  @bot.on.multiply(['Из таблицы'], [States.SCHEDULE_MENU])
  def from_table(self):
    if self.object:
      text = Timetable(_json, self.object, self.config).get_text()
      bot.utils.send_message(text) 
    else:
      bot.db.set_state(States.REGISTER[0])
      bot.utils.send_message('Объект расписания не найден\nПриступаем к регистарции!', keyboard = UserKeyboards.OK)

class Prediction:

  @bot.on.state(States.PREDICTION_MENU)
  def input_date(self):
    if self.text != emoji.emojize(':hollow_red_circle:') and self.text[0].isdigit():
      try:
        text = Ruobr(self.ruobr_login, self.ruobr_password).get_schedule(self.text).get_text()
        bot.utils.send_message(f"Расписание на {self.text}\n\n{text}")
      except RuobrException.DateException:
        bot.utils.send_message('Неверный формат даты!\nДень.Месяц.Год')
      except RuobrException.EmptyScheduleException:
        bot.utils.send_message(f'Расписания на {self.text} нет!')

  @bot.on.multiply(['На завтра'], [States.PREDICTION_MENU])
  def tomorrow(self):
    try:
      str_tomorrow = get_tomorrow()
      text = Ruobr(self.ruobr_login, self.ruobr_password).get_schedule(str_tomorrow).get_text()
      bot.utils.send_message(f"Расписание на {str_tomorrow}\n\n{text}")
    except RuobrException.EmptyScheduleException:
      bot.utils.send_message(f'Расписания на {str_tomorrow} нет!')

class Mailing:
  
  @bot.on.multiply(['Отписаться'], [States.MAILING_MENU])
  def unsubscribe(self):
    bot.db.update_field(category='mailing', new ='False')
    bot.utils.send_message('Рассылка отключена!')

  @bot.on.multiply(['Подписаться'], [States.MAILING_MENU])
  def subscribe(self):
    bot.db.update_field(category='mailing', new ='True')
    bot.utils.send_message('Рассылка включена!')

class Marks:
  @bot.on.state(States.MARKS_MENU)
  def input_text(self):
    if self.text != emoji.emojize(':hollow_red_circle:') and self.text[0].isdigit():
      try:
        bot.utils.send_message('Ожидайте...')
        text = Ruobr(self.ruobr_login, self.ruobr_password).get_marks(self.text).get_text()
        bot.utils.send_message(text)
      except RuobrException.DateException:
        bot.utils.send_message('Неверный формат даты!')

  @bot.on.multiply(['На сегодня'], [States.MARKS_MENU])
  def get_marks_of_day(self):
    bot.utils.send_message('Ожидайте...')
    text = Ruobr(self.ruobr_login, self.ruobr_password).get_marks('day').get_text()
    bot.utils.send_message(text)

  @bot.on.multiply(['За месяц'], [States.MARKS_MENU])
  def get_marks_of_day(self):
    bot.utils.send_message('Ожидайте...')
    text = Ruobr(self.ruobr_login, self.ruobr_password).get_marks('month').get_text()
    bot.utils.send_message(text)

  @bot.on.multiply(['За год'], [States.MARKS_MENU])
  def get_marks_of_day(self):
    bot.utils.send_message('Ожидайте...')
    text = Ruobr(self.ruobr_login, self.ruobr_password).get_marks('year').get_text()
    bot.utils.send_message(text)

  @bot.on.multiply(['Таблица оценок'], [States.MARKS_MENU])
  def get_table_marks(self):
    bot.db.set_state(States.EXCEL_MENU)
    bot.utils.send_message("Напишите год", keyboard=UserKeyboards.EXCEL)

class Excel:
  @bot.on.multiply(['За этот учебный год'], [States.EXCEL_MENU])
  def get_excel_marks_now(self):
    bot.utils.send_message('Ожидайте...')
    buffer = BytesIO()
    Ruobr(self.ruobr_login, self.ruobr_password).get_excel('now').save(buffer)
    fullname = bot.utils.get_fullname().split(' ')
    filename = f'{fullname[0]}_{fullname[1]}_{datetime.now().strftime("%Y_%m_%d")}'
    attachments = [filename,buffer]
    bot.utils.send_message('Ваш файл готов!', file = attachments)
    buffer.close()
  
  @bot.on.state(States.EXCEL_MENU)
  def get_excel_marks_now(self):
    if self.text != emoji.emojize(':hollow_red_circle:') and self.text[0].isdigit():
      try:
        bot.utils.send_message('Ожидайте...')
        buffer = BytesIO()
        Ruobr(self.ruobr_login, self.ruobr_password).get_excel(self.text).save(buffer)
        fullname = bot.utils.get_fullname().split(' ')
        filename = f'{fullname[0]}_{fullname[1]}_{datetime.now().strftime("%Y_%m_%d")}'
        attachments = [filename,buffer]
        bot.utils.send_message('Ваш файл готов!', file = attachments)
        buffer.close()
      except RuobrException.DateException:
        bot.utils.send_message('Неверный формат даты!')

class ConfReg:
  @bot.on.multiply([emoji.emojize(':OK_button:')], [States.EDIT_CONF[0]])
  def ok_answer(self):
    bot.db.set_state(States.EDIT_CONF[1])
    bot.utils.send_message('Введите конфигурацию для расписания',keyboard = UserKeyboards.CANCEL, url='vk.com/@schedule_kgtt-konfiguraciya')

  @bot.on.state(States.EDIT_CONF[1])
  def sub_register_1(self):
    if self.text != emoji.emojize(':hollow_red_circle:'):
      ctx_name = f'attr{self.user_id}'
      Ctx.set(ctx_name, self.text)
      
      try_start = Timetable('src/test.json', 'Тест', self.text).get_text()
      bot.db.set_state(States.EDIT_CONF[2])
      bot.utils.send_message(f'Пример :\n\n{try_start}', keyboard = UserKeyboards.SELECTION)
      bot.utils.send_message('Вы согласны ?')


  @bot.on.multiply([emoji.emojize(':thumbs_up:')], [States.EDIT_CONF[2]])
  def sub_register_table_positive_answer(self):
    bot.db.update_field(category='config', new= Ctx.get(f'attr{self.user_id}'))
    Ctx.delete(f'attr{self.user_id}')
    bot.db.set_state(States.MAIN_MENU)
    bot.utils.send_message('Успешно!',keyboard = UserKeyboards.MAIN_MENU)

  @bot.on.multiply([emoji.emojize(':thumbs_down:')], [States.EDIT_CONF[2]])
  def sub_register_table_negative_answer(self):
    bot.db.set_state(States.EDIT_CONF[1])
    bot.utils.send_message('Введите конфигурацию для расписания', keyboard = UserKeyboards.CANCEL)

class TableReg:
  @bot.on.multiply([emoji.emojize(':OK_button:')], [States.REGISTER[0]])
  def ok_answer(self):
    bot.db.set_state(States.REGISTER[1])
    bot.utils.send_message('Введите группу или преподавателя, как указано в таблице',keyboard =UserKeyboards.CANCEL, url = 'https://clck.ru/psvfm')

  @bot.on.state(States.REGISTER[1])
  def register_1(self):
    if self.text in _get_keys():
      
      Ctx.set(f'attr{self.user_id}', self.text)
      bot.db.set_state(States.REGISTER[2])
      bot.utils.send_message('Вы согласны ?', keyboard=UserKeyboards.SELECTION)

  @bot.on.multiply([emoji.emojize(':thumbs_up:')], [States.REGISTER[2]])
  def register_table_positive_answer(self):
    bot.db.update_field(category='object', new = Ctx.get(f'attr{self.user_id}'))
    Ctx.delete(f'attr{self.user_id}')
    bot.db.set_state(States.MAIN_MENU)
    bot.utils.send_message('Вы успешно зарегистрированы\n!р - Получить расписание',keyboard =UserKeyboards.MAIN_MENU)

  @bot.on.multiply([emoji.emojize(':thumbs_down:')], [States.REGISTER[2]])
  def register_table_negative_answer(self):
    bot.db.set_state(States.REGISTER[1])
    bot.utils.send_message('Введите группу или преподавателя, как указано в таблице', keyboard = UserKeyboards.CANCEL, url = 'https://clck.ru/psvfm')

class RuobrReg:
  @bot.on.multiply([emoji.emojize(':OK_button:')], [States.RUOBR_REGISTER[0]])
  def ok_answer(self):
    bot.db.set_state(States.RUOBR_REGISTER[1])
    bot.utils.send_message('Введите логин от Cabinet Ruobr',keyboard =UserKeyboards.CANCEL, url = 'https://cabinet.ruobr.ru/login/')

  @bot.on.state(States.RUOBR_REGISTER[1])
  def register_login(self):
    if self.text != emoji.emojize(':hollow_red_circle:'):
      
      ctx_login = f'attr{self.user_id}_login'
      Ctx.set(ctx_login, self.text)
      
      bot.db.set_state(States.RUOBR_REGISTER[2])
      bot.utils.send_message(f'Логин : {Ctx.get(ctx_login)}\nВведите пароль от Cabinet Ruobr', keyboard =UserKeyboards.CANCEL)

  @bot.on.state(States.RUOBR_REGISTER[2])
  def register_selection(self):
    if self.text != emoji.emojize(':hollow_red_circle:'):
      
      ctx_login = f'attr{self.user_id}_login'
      ctx_password = f'attr{self.user_id}_password'

      Ctx.set(ctx_password,self.text)
      
      bot.db.set_state(States.RUOBR_REGISTER[3])
      bot.utils.send_message(f"Логин : {Ctx.get(ctx_login)}\nПароль : {Ctx.get(ctx_password)}")
      bot.utils.send_message('Вы согласны ?', keyboard = UserKeyboards.SELECTION)

  @bot.on.multiply([emoji.emojize(':thumbs_up:')], [States.RUOBR_REGISTER[3]])
  def register_table_positive_answer(self):
    bot.db.set_state(States.MAIN_MENU)
    try:
      ctx_login = f'attr{self.user_id}_login'
      ctx_password = f'attr{self.user_id}_password'
      
      Ruobr(Ctx.get(ctx_login), Ctx.get(ctx_password))

      bot.db.update_field(category='ruobr_login', new = Ctx.get(ctx_login))
      bot.db.update_field(category='ruobr_password', new = Ctx.get(ctx_password))

      bot.db.set_state(States.MAIN_MENU)
      bot.utils.send_message('Вы успешно зарегистрированы!', keyboard =UserKeyboards.MAIN_MENU)
      
      Ctx.delete(ctx_password)
      Ctx.delete(ctx_login)
      
    except RuobrException.AuthException:
      bot.db.set_state(States.RUOBR_REGISTER[1])
      bot.utils.send_message('Логин или пароль указаны неверно!\nВведите логин от Cabinet Ruobr',
                   keyboard =UserKeyboards.CANCEL)

  @bot.on.multiply([emoji.emojize(':thumbs_down:')], [States.RUOBR_REGISTER[3]])
  def register_table_negative_answer(self):
    bot.db.set_state(States.RUOBR_REGISTER[1])
    bot.utils.send_message('Введите логин от Cabinet Ruobr', keyboard =UserKeyboards.CANCEL)

bot.Start()

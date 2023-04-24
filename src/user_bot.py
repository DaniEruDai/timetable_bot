from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv('__additional_files__\\.env'))



from ruobr_api.ruobr_api import Ruobr, RuobrException, get_tomorrow
from schedule.kgtt.timetable import TimeTable, read_json


from vk.UserBot._bot import send_message, message_handler, state_handler, multiply_handler, StartBot, get_fullname
from vk.UserBot._bot import CtxStorage
from vk.UserBot._keyboards import UserKeyboards
from vk.UserBot._states import States

from vk.database import DB


import json
import emoji


database = DB('data.db')
Ctx = CtxStorage()


def _get_keys() -> tuple:
  with open('timetable.json', 'r', encoding='utf-8') as js:
    dictionary = json.loads(js.read())
  return tuple(dictionary.keys())


"""Общие меню"""


class Utilities:

  @message_handler('!р', '!расписание', '/р', '/расписание')
  def send_shedule(self):
    if self.object:
      # Получение расписания
      try:
        text = TimeTable(read_json('timetable.json'), self.object, self.config).get_text()
        send_message(self.user_id, text)
      except Exception:
        send_message(self.user_id, 'Возникла ошибка при получении расписания.\nПопробуйте изменить объект расписания.')


    else:
      database.swap_user_state(self.user_id, States.REGISTER[0])
      send_message(self.user_id, 'Объект для рассылки не найден\nПриступаем к регистарции!', UserKeyboards.OK)

  @message_handler('Начать', 'Начало', 'Старт', '/start', '/Начать')
  def start(self):
    send_message(self.user_id, 'За работу!', UserKeyboards.MAIN_MENU)

  @message_handler('!сброс', '/сброс')
  def reset(self):

    database.swap_user_state(self.user_id, States.MAIN_MENU)
    database.delete_user(self.user_id)
    send_message(self.user_id, 'Все данные успешно удалены!', UserKeyboards.MAIN_MENU)

  @message_handler(emoji.emojize(':hollow_red_circle:'))
  def back(self):
    database.swap_user_state(self.user_id, States.MAIN_MENU)
    send_message(self.user_id, 'Главное меню', UserKeyboards.MAIN_MENU)


class Main:

  @multiply_handler(['Расписание'], [States.MAIN_MENU])
  def schedule(self):
    database.swap_user_state(self.user_id, States.SCHEDULE_MENU)
    send_message(self.user_id, 'Раздел с расписанием', UserKeyboards.SCHEDULE)

  @multiply_handler(['Оценки'], [States.MAIN_MENU])
  def marks(self):
    if self.ruobr_login and self.ruobr_password:
      database.swap_user_state(self.user_id, States.MARKS_MENU)
      send_message(self.user_id, 'Напишите дату или выберите один из нескольких вариантов', UserKeyboards.EVALUATION)
    else:
      database.swap_user_state(self.user_id, States.RUOBR_REGISTER[0])
      send_message(self.user_id, 'Для работы раздела необходимо зайти в Cabinet Ruobr!', UserKeyboards.OK)

  @multiply_handler([emoji.emojize(':gear:')], [States.MAIN_MENU])
  def parameters(self):

    fullname = get_fullname(self.user_id)
    text = f"{fullname}\n\nОбъект таблицы : {self.object}\nКонфигурация расписания : \n{self.config}\nЛогин : {self.ruobr_login}\nПароль : {self.ruobr_password}"

    database.swap_user_state(self.user_id, States.PARAMETERS_MENU)
    send_message(self.user_id, text, UserKeyboards.PARAMETERS)


class Parameters:
  @multiply_handler(['Изменить логин и пароль Ruobr'], [States.PARAMETERS_MENU])
  def edit_pl(self):
    database.swap_user_state(self.user_id, States.RUOBR_REGISTER[0])
    send_message(self.user_id, 'Начнем!', UserKeyboards.OK)

  @multiply_handler(['Изменить конфиг'], [States.PARAMETERS_MENU])
  def edit_configuration(self):
    database.swap_user_state(self.user_id, States.EDIT_CONF[0])
    send_message(self.user_id, 'Начнем!', UserKeyboards.OK)

  @multiply_handler(['Изменить объект'], [States.PARAMETERS_MENU])
  def edit_object(self):
    database.swap_user_state(self.user_id, States.REGISTER[0])
    send_message(self.user_id, 'Начнем!', UserKeyboards.OK)

  @multiply_handler(['Помощь'], [States.PARAMETERS_MENU])
  def helps(self):
    text = "Дополнительные команды\n\n!сброс - Полностью сбрасывает все параметры пользователя\n\nВопросы можете задать тут :"
    send_message(self.user_id, text, url='https://vk.com/topic-214878797_49282332')


"""Расписание = [Предсказания,Рассылка]"""


class Schedule:
  @multiply_handler(['Рассылка'], [States.SCHEDULE_MENU])
  def mailing(self):
    if self.object:
      database.swap_user_state(self.user_id, States.MAILING_MENU)
      send_message(self.user_id, 'Всё окей!', keyboard=UserKeyboards.MAILING)

    else:
      database.swap_user_state(self.user_id, States.REGISTER[0])
      send_message(self.user_id, 'Объект для рассылки не найден\nПриступаем к регистарции!', UserKeyboards.OK)

  @multiply_handler(['Предсказания'], [States.SCHEDULE_MENU])
  def prediction(self):
    if self.ruobr_login and self.ruobr_password:
      database.swap_user_state(self.user_id, States.PREDICTION_MENU)
      send_message(self.user_id,
                   'Раздел "Предсказания" позволяет получить расписание из "Ruobr" по дате, однако стоит учитывать, что оно может быть неточным.',
                   UserKeyboards.PREDICTION)
    else:
      database.swap_user_state(self.user_id, States.RUOBR_REGISTER[0])
      send_message(self.user_id, 'Для работы раздела необходимо зайти в Cabinet Ruobr!', UserKeyboards.OK)

  @multiply_handler(['Из таблицы'], [States.SCHEDULE_MENU])
  def from_table(self):
    if self.object:
      try:
        text = TimeTable(read_json('timetable.json'), self.object, self.config).get_text()
        send_message(self.user_id, text)
      except Exception:
        send_message(self.user_id, 'Возникла ошибка при получении расписания.\nПопробуйте изменить объект расписания.')
    else:
      database.swap_user_state(self.user_id, States.REGISTER[0])
      send_message(self.user_id, 'Объект расписания не найден\nПриступаем к регистарции!', UserKeyboards.OK)


class Prediction:

  @state_handler(States.PREDICTION_MENU)
  def input_date(self):
    if self.text != emoji.emojize(':hollow_red_circle:') and self.text[0].isdigit():
      try:
        text = Ruobr(self.ruobr_login, self.ruobr_password).get_schedule(self.text).get_text()
        send_message(self.user_id, f"Расписание на {self.text}\n\n{text}")
      except RuobrException.DateException:
        send_message(self.user_id, 'Неверный формат даты!\nДень.Месяц.Год')
      except RuobrException.EmptyScheduleException:
        send_message(self.user_id, f'Расписания на {self.text} нет!')

  @multiply_handler(['На завтра'], [States.PREDICTION_MENU])
  def tomorrow(self):
    try:
      str_tomorrow = get_tomorrow()
      text = Ruobr(self.ruobr_login, self.ruobr_password).get_schedule(str_tomorrow).get_text()
      send_message(self.user_id, f"Расписание на {str_tomorrow}\n\n{text}")
    except RuobrException.EmptyScheduleException:
      send_message(self.user_id, f'Расписания на {str_tomorrow} нет!')


class Mailing:
  @multiply_handler(['Отписаться'], [States.MAILING_MENU])
  def unsubscribe(self):
    database.update_field(self.user_id, 'user', 'mailing', 'False')
    send_message(self.user_id, 'Рассылка отключена!')

  @multiply_handler(['Подписаться'], [States.MAILING_MENU])
  def subscribe(self):
    database.update_field(self.user_id, 'user', 'mailing', 'True')
    send_message(self.user_id, 'Рассылка включена!')


"""Оценки"""


class Marks:
  @state_handler(States.MARKS_MENU)
  def input_text(self):
    if self.text != emoji.emojize(':hollow_red_circle:') and self.text[0].isdigit():
      try:
        send_message(self.user_id, 'Ожидайте...')
        text = Ruobr(self.ruobr_login, self.ruobr_password).get_marks(self.text).get_text()
        send_message(self.user_id, text)
      except RuobrException.DateException:
        send_message(self.user_id, 'Неверный формат даты!')

  @multiply_handler(['На сегодня'], [States.MARKS_MENU])
  def get_marks_of_day(self):
    send_message(self.user_id, 'Ожидайте...')
    text = Ruobr(self.ruobr_login, self.ruobr_password).get_marks('day').get_text()
    send_message(self.user_id, text)

  @multiply_handler(['За месяц'], [States.MARKS_MENU])
  def get_marks_of_day(self):
    send_message(self.user_id, 'Ожидайте...')
    text = Ruobr(self.ruobr_login, self.ruobr_password).get_marks('month').get_text()
    send_message(self.user_id, text)

  @multiply_handler(['За год'], [States.MARKS_MENU])
  def get_marks_of_day(self):
    send_message(self.user_id, 'Ожидайте...')
    text = Ruobr(self.ruobr_login, self.ruobr_password).get_marks('year').get_text()
    send_message(self.user_id, text)

  @multiply_handler(['Таблица оценок'], [States.MARKS_MENU])
  def get_table_marks(self):
    send_message(self.user_id, "Раздел в разработке")


"""Регистрация"""


class ConfReg:
  @multiply_handler([emoji.emojize(':OK_button:')], [States.EDIT_CONF[0]])
  def ok_answer(self):
    database.swap_user_state(self.user_id, States.EDIT_CONF[1])
    send_message(self.user_id,
                 'Введите конфигурацию для расписания',
                 UserKeyboards.CANCEL, url='vk.com/@schedule_kgtt-konfiguraciya')

  @state_handler(States.EDIT_CONF[1])
  def sub_register_1(self):
    if self.text != emoji.emojize(':hollow_red_circle:'):
      Ctx.set(self.ctx_name, self.text)

      database.swap_user_state(self.user_id, States.EDIT_CONF[2])
      try_start = TimeTable(read_json('src\\test.json'), 'Тест', self.text).get_text()
      send_message(self.user_id, f'Как это будет выглядеть\n\n{try_start}\n\nВы согласны ?',
                   keyboard=UserKeyboards.SELECTION)

  @multiply_handler([emoji.emojize(':thumbs_up:')], [States.EDIT_CONF[2]])
  def sub_register_table_positive_answer(self):
    database.update_field(self.user_id, 'user', 'config', Ctx.get(self.ctx_name))
    Ctx.delete(self.ctx_name)
    database.swap_user_state(self.user_id, States.MAIN_MENU)
    send_message(self.user_id,
                 'Успешно',
                 UserKeyboards.MAIN_MENU)

  @multiply_handler([emoji.emojize(':thumbs_down:')], [States.EDIT_CONF[2]])
  def sub_register_table_negative_answer(self):
    database.swap_user_state(self.user_id, States.EDIT_CONF[1])

    send_message(self.user_id, 'Введите конфигурацию для расписания', UserKeyboards.CANCEL)


class TableReg:
  @multiply_handler([emoji.emojize(':OK_button:')], [States.REGISTER[0]])
  def ok_answer(self):
    database.swap_user_state(self.user_id, States.REGISTER[1])
    send_message(self.user_id,
                 'Введите группу или преподавателя, как указано в таблице',
                 UserKeyboards.CANCEL, 'https://clck.ru/psvfm')

  @state_handler(States.REGISTER[1])
  def register_1(self):
    if self.text in _get_keys():
      Ctx.set(self.ctx_name, self.text)

      database.swap_user_state(self.user_id, States.REGISTER[2])
      send_message(self.user_id, 'Вы согласны ?', keyboard=UserKeyboards.SELECTION)

  @multiply_handler([emoji.emojize(':thumbs_up:')], [States.REGISTER[2]])
  def register_table_positive_answer(self):
    database.update_field(self.user_id, 'user', 'object', Ctx.get(self.ctx_name))
    Ctx.delete(self.ctx_name)
    database.swap_user_state(self.user_id, States.MAIN_MENU)
    send_message(self.user_id,
                 'Вы успешно зарегистрированы\n!р - Получить расписание',
                 UserKeyboards.MAIN_MENU)

  @multiply_handler([emoji.emojize(':thumbs_down:')], [States.REGISTER[2]])
  def register_table_negative_answer(self):
    database.swap_user_state(self.user_id, States.REGISTER[1])
    send_message(self.user_id,
                 'Введите группу или преподавателя, как указано в таблице',
                 UserKeyboards.CANCEL, 'https://clck.ru/psvfm')


class RuobrReg:

  @multiply_handler([emoji.emojize(':OK_button:')], [States.RUOBR_REGISTER[0]])
  def ok_answer(self):
    database.swap_user_state(self.user_id, States.RUOBR_REGISTER[1])
    send_message(self.user_id,
                 'Введите логин от Cabinet Ruobr',
                 UserKeyboards.CANCEL)

  @state_handler(States.RUOBR_REGISTER[1])
  def register_password(self):
    if self.text != emoji.emojize(':hollow_red_circle:'):
      # Запись временного логина
      ctx_ruobr_login = self.ctx_name + '_login'
      Ctx.set(ctx_ruobr_login, self.text)

      database.swap_user_state(self.user_id, States.RUOBR_REGISTER[2])
      send_message(self.user_id, 'Введите пароль от Cabinet Ruobr', UserKeyboards.CANCEL)

  @state_handler(States.RUOBR_REGISTER[2])
  def register_selection(self):
    if self.text != emoji.emojize(':hollow_red_circle:'):
      # Запись временного пароля
      ctx_ruobr_password = self.ctx_name + '_password'
      ctx_ruobr_login = self.ctx_name + '_login'
      Ctx.set(ctx_ruobr_password, self.text)
      database.swap_user_state(self.user_id, States.RUOBR_REGISTER[3])
      send_message(self.user_id, f"Логин: {Ctx.get(ctx_ruobr_login)}\nПароль: {Ctx.get(ctx_ruobr_password)}")
      send_message(self.user_id, 'Вы согласны ?', keyboard=UserKeyboards.SELECTION)

  @multiply_handler([emoji.emojize(':thumbs_up:')], [States.RUOBR_REGISTER[3]])
  def register_table_positive_answer(self):
    database.swap_user_state(self.user_id, States.MAIN_MENU)
    try:
      ctx_ruobr_password = self.ctx_name + '_password'
      ctx_ruobr_login = self.ctx_name + '_login'
      Ruobr(Ctx.get(ctx_ruobr_login), Ctx.get(ctx_ruobr_password))

      database.update_field(self.user_id, 'user', 'ruobr_login', Ctx.get(ctx_ruobr_login))
      database.update_field(self.user_id, 'user', 'ruobr_password', Ctx.get(ctx_ruobr_password))

      database.swap_user_state(self.user_id, States.MAIN_MENU)
      send_message(self.user_id, 'Вы успешно зарегистрированы!', UserKeyboards.MAIN_MENU)

      Ctx.delete(ctx_ruobr_login)
      Ctx.delete(ctx_ruobr_password)


    except RuobrException.AuthException:
      database.swap_user_state(self.user_id, States.RUOBR_REGISTER[1])
      send_message(self.user_id, 'Логин или пароль указаны неверно!\nВведите логин от Cabinet Ruobr',
                   UserKeyboards.CANCEL)

  @multiply_handler([emoji.emojize(':thumbs_down:')], [States.RUOBR_REGISTER[3]])
  def register_table_negative_answer(self):
    database.swap_user_state(self.user_id, States.RUOBR_REGISTER[1])
    send_message(self.user_id,
                 'Введите логин от Cabinet Ruobr',
                 UserKeyboards.CANCEL)


StartBot()

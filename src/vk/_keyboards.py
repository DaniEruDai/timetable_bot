from vk_api.keyboard import VkKeyboard,VkKeyboardColor
import emoji

def _SELECTION_KEYBOARD():
    keyboard = VkKeyboard()
    keyboard.add_button(emoji.emojize(':thumbs_up:'), color=VkKeyboardColor.POSITIVE)
    keyboard.add_button(emoji.emojize(':thumbs_down:'), color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button(emoji.emojize(':hollow_red_circle:'),color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()
  
def _MAIN_KEYBOARD():
    keyboard = VkKeyboard()
    keyboard.add_button("Расписание", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("Оценки", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button(emoji.emojize(':gear:'), color=VkKeyboardColor.SECONDARY)
    
    
    return keyboard.get_keyboard()
  
def _SCHEDULE_KEYBOARD():
  keyboard = VkKeyboard()
  keyboard.add_button("Предсказания", color=VkKeyboardColor.SECONDARY)
  keyboard.add_button("Из таблицы", color=VkKeyboardColor.POSITIVE)
  keyboard.add_button("Рассылка", color=VkKeyboardColor.SECONDARY)
  keyboard.add_line()
  keyboard.add_button(emoji.emojize(':hollow_red_circle:'),color=VkKeyboardColor.NEGATIVE)
  return keyboard.get_keyboard()

def _MAILING_KEYBOARD():
  keyboard = VkKeyboard()
  keyboard.add_button("Отписаться", color=VkKeyboardColor.SECONDARY)
  keyboard.add_button("Подписаться", color=VkKeyboardColor.SECONDARY)
  keyboard.add_line()
  keyboard.add_button(emoji.emojize(':hollow_red_circle:'),color=VkKeyboardColor.NEGATIVE)
  
  
  return keyboard.get_keyboard()

def _PARAMETERS_KEYBOARD():
  keyboard = VkKeyboard()
  keyboard.add_button("Изменить логин и пароль Ruobr", color=VkKeyboardColor.SECONDARY)
  keyboard.add_line()
  keyboard.add_button("Изменить конфиг", color=VkKeyboardColor.SECONDARY)
  keyboard.add_button("Изменить объект", color=VkKeyboardColor.SECONDARY)
  keyboard.add_line()
  keyboard.add_button("Помощь", color=VkKeyboardColor.POSITIVE)
  keyboard.add_line()
  keyboard.add_button(emoji.emojize(':hollow_red_circle:'),color=VkKeyboardColor.NEGATIVE)
  return keyboard.get_keyboard()
  
def _PREDICTION_KEYBOARD():
  keyboard = VkKeyboard()
  keyboard.add_button("На завтра", color=VkKeyboardColor.SECONDARY)
  keyboard.add_line()
  keyboard.add_button(emoji.emojize(':hollow_red_circle:'),color=VkKeyboardColor.NEGATIVE)
  
  return keyboard.get_keyboard()

def _EVALUATION_KEYBOARD():
  keyboard = VkKeyboard()
  keyboard.add_button("На сегодня", color=VkKeyboardColor.SECONDARY)
  keyboard.add_button("За месяц", color=VkKeyboardColor.SECONDARY)
  keyboard.add_button("За год", color=VkKeyboardColor.SECONDARY)
  keyboard.add_line()
  keyboard.add_button('Таблица оценок',color=VkKeyboardColor.POSITIVE)
  keyboard.add_line()
  keyboard.add_button(emoji.emojize(':hollow_red_circle:'),color=VkKeyboardColor.NEGATIVE)
  return keyboard.get_keyboard()

def _OK_KEYBOARD():
  keyboard = VkKeyboard()
  keyboard.add_button(emoji.emojize(':OK_button:'), color=VkKeyboardColor.POSITIVE)
  return keyboard.get_keyboard()

def _CANCEL_KEYBOARD():
  keyboard = VkKeyboard()
  keyboard.add_button(emoji.emojize(':hollow_red_circle:'), color=VkKeyboardColor.NEGATIVE)
  return keyboard.get_keyboard()

def _EXCEL_KEYBOARD():
  keyboard = VkKeyboard()
  keyboard.add_button('За этот учебный год',color=VkKeyboardColor.SECONDARY)
  keyboard.add_line()
  keyboard.add_button(emoji.emojize(':hollow_red_circle:'), color=VkKeyboardColor.NEGATIVE)
  return keyboard.get_keyboard()

class UserKeyboards:
  EMPTY = VkKeyboard().get_empty_keyboard()
  SELECTION = _SELECTION_KEYBOARD()
  MAIN_MENU = _MAIN_KEYBOARD()
  SCHEDULE = _SCHEDULE_KEYBOARD()
  PREDICTION = _PREDICTION_KEYBOARD()
  EVALUATION = _EVALUATION_KEYBOARD()
  OK = _OK_KEYBOARD()
  CANCEL = _CANCEL_KEYBOARD()
  MAILING = _MAILING_KEYBOARD()
  PARAMETERS = _PARAMETERS_KEYBOARD()
  EXCEL = _EXCEL_KEYBOARD()



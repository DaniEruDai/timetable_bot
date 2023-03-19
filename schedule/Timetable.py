from GoogleTable import get_table, Table
import re
from itertools import chain,zip_longest
from datetime import datetime
import json
import os
import time


class _CropTableTeachers():
  """
Класс CropTable предназначен для работы с таблицами и обработки данных в них. 
\nОн может быть использован, например, для выделения определенных данных из таблицы, фильтрации их и преобразования в нужный формат.
  """

  def __init__(self,table : Table,teacher:str,column_index:int,keys:tuple) -> None:
    self.__TABLE__ = table
    self.key_1,self.key_2 = keys
    self.teacher  = teacher
    self.__column_index = column_index

  def get_lessons(self) -> list:
    lesson = self.__TABLE__[self.__column_index][self.key_1:self.key_2][1::2]
    return lesson

  def get_groups(self) -> list:
    teachers = self.__TABLE__[self.__column_index][self.key_1:self.key_2][::2]
    return teachers

  def get_cabinets(self) -> list:
    cabinets = self.__TABLE__[self.__column_index+1][self.key_1:self.key_2][::2]
    return cabinets

  def get_time(self) -> list:
  
    date_str = re.search(r'\d{2}\.\d{2}\.\d{4}', ' '.join(self.__TABLE__[0])).group() # дата в формате "День.Месяц.Год"
    date_obj = datetime.strptime(date_str, '%d.%m.%Y')
    weekday_num = date_obj.isoweekday()
    
    time = ['08:30 - 10:00',
                '10:10 - 11:40',
                '11:50 - 13:20',
                '13:30 - 15:00',
                '15:10 - 16:40',
                '16:45 - 18:15']
    
    if weekday_num == 3:
        time = ['08:30 - 10:00',
                '10:10 - 11:40',
                '11:50 - 12:20',
                '12:30 - 14:00',
                '14:10 - 15:40',
                '16:50 - 17:20']
        
    return time

  def get_numbers(self) -> list:
  
    result = self.__TABLE__[0][self.key_1:self.key_2]
    result = [i for i in result if i != '']
    return result

  def get_dictionary(self):
    lessons = self.get_lessons()
    lessons_bool = list(map(lambda i : True if i == '' else False,lessons))
    if all(lessons_bool):
      return None
      
    return  {'default' : self.get_teachers(),
            'lesson':lessons,
            'cabinet' : self.get_cabinets(),
            'time':self.get_time(),
            'number': self.get_numbers()}

class TeachersTable:

  def __init__(self) -> None:
    self.__TABLE__ = self.__update_table(get_table('1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU','1202329550')[:9])
    self.__TABLE__ = Table(map(lambda x : [''] + x if len(x) % 2 != 0 else x, self.__TABLE__))

  def __update_table(self,table) -> Table :
    
    changed_table = []
    for column in table:
      changed_column = []
      for ellement in column:
        group_in_string = re.search(r'[А-Я][а-я]+\s{1}\w[А-Я.]+\s{1}\w[А-Я.]', ellement)
        new_ellement = group_in_string.group() if group_in_string else ellement       
        changed_column.append(new_ellement)
      changed_table.append(changed_column)
    return Table(changed_table)

  def __get_exception_teachers(self) -> list :  
    exception_groups = []
    for column in self.__TABLE__:
      string_from_column = ' '.join(column)
      result = re.findall(r'[А-Я][а-я]+\s{1}\w[А-Я.]+\s{1}\w[А-Я.]', string_from_column)
      if not result:
        continue
      exception_groups.append(result[-1])
    return tuple(exception_groups)

  def get_teacher_names(self) -> tuple:
    string_from_table = ' '.join(tuple(chain(*self.__TABLE__)))
    result = re.findall(r'[А-ЯЁ][а-яё]+\s+[А-ЯЁ]\.\s+[А-ЯЁ]\.', string_from_table)
    return result

  def get_all_teachers_dictionary(self) -> dict | None:
   
    dictionary = {}
    __GROUPS__ = self.get_teacher_names()
    __Exception_groups = self.__get_exception_teachers()
    for t_1,t_2 in zip_longest(__GROUPS__,__GROUPS__[1:],fillvalue=''):
      keys = (self.__TABLE__.get_index(t_1).row+1,self.__TABLE__.get_index(t_2).row)
      if t_1 in __Exception_groups:
        keys = (self.__TABLE__.get_index(t_1).row+1,self.__TABLE__.get_index(t_1).row+12)
      column_index = self.__TABLE__.get_index(t_1).column
     
      data = _CropTableTeachers(
        keys=keys,
        teacher=t_1,
        column_index=column_index,
        table=self.__TABLE__)

      dictionary[t_1] = data.get_dictionary()
    
    return dictionary

class _CropTableStudents():
  """
Класс CropTable предназначен для работы с таблицами и обработки данных в них. 
\nОн может быть использован, например, для выделения определенных данных из таблицы, фильтрации их и преобразования в нужный формат.
  """

  def __init__(self,table : Table,group:str,column_index:int,keys:tuple) -> None:
    self.__TABLE__ = table
    self.key_1,self.key_2 = keys
    self.group  = group
    self.__column_index = column_index
    self.__extra_index = self.__get__extra_index()
    
  def __get__extra_index(self) -> tuple :
    """Данный метод является функцией, которая возвращает кортеж индексов из обрезаной под определненный диапазон таблицы , где стоят дополнительные предметы"""
    lesson = self.__TABLE__[self.__column_index][self.key_1:self.key_2][::2]
    lesson_2 = self.__TABLE__[self.__column_index + 2][self.key_1:self.key_2][::2]
    return tuple([i for i,(l1,l2) in enumerate(zip(lesson,lesson_2)) if l1 and l2 ])

  def get_lessons(self) -> list:
   
    lesson = self.__TABLE__[self.__column_index][self.key_1:self.key_2][::2]
    lesson_2 = self.__TABLE__[self.__column_index + 2][self.key_1:self.key_2][::2]
    result = []
    
    for i,(l1,l2) in enumerate(zip(lesson,lesson_2)):
      
      if not l1 and not l2:
        result.append(l1)
        
      elif l1 and l2:
        result.append(l1)
        result.append(l2)
      
      elif l1 and not l2:
        result.append(l1)
      
      elif l2 and not l1:
        result.append(l2)
        
    return result

  def get_teachers(self) -> list:
    teachers = self.__TABLE__[self.__column_index][self.key_1:self.key_2][1::2]
    teachers_2 = self.__TABLE__[self.__column_index+2][self.key_1:self.key_2][1::2]
    
  
    result = []
    
    for t1,t2 in zip(teachers,teachers_2):
      
      
      if not t1 and not t2:
        result.append(t1)
        
      elif t1 and t2:
        result.append(t1)
        result.append(t2)
      
      elif t1 and not t2:
        result.append(t1)
      
      elif t2 and not t1:
        result.append(t2)
        
    return result

  def get_cabinets(self) -> list:
    cabinets = self.__TABLE__[self.__column_index+4][self.key_1:self.key_2][::2]
    cabinets_2 = self.__TABLE__[self.__column_index+1][self.key_1:self.key_2][::2]
    cabinets_3 = self.__TABLE__[self.__column_index+3][self.key_1:self.key_2][::2]
    
    
    result = []
    
    for c1,c2,c3 in zip(cabinets,cabinets_2,cabinets_3):
      
      if c1 == c2 == c3:
        result.append(c1)
        
      elif c2 and c3:
        result.append(c2)
        result.append(c3)
      
      elif c1:
        result.append(c1)
        
      elif c2 and not c3 :
        result.append(c2)
      
      elif c3 and not c2:
        result.append(c3)
        
    return result

  def get_numbers(self) -> list:
    
    result = self.__TABLE__[0][self.key_1:self.key_2]
    result = [i for i in result if i != '']
    
    if (self.__extra_index):
      for index in self.__extra_index:
        result.insert(index+1,f'{result[index]}.2')
        result[index] = f'{result[index]}.1'
        
    return result

  def get_time(self) -> list:
  
    date_str = re.search(r'\d{2}\.\d{2}\.\d{4}', ' '.join(self.__TABLE__[0])).group() # дата в формате "День.Месяц.Год"
    date_obj = datetime.strptime(date_str, '%d.%m.%Y')
    weekday_num = date_obj.isoweekday()
    

    time = ['08:30 - 10:00',
                '10:10 - 11:40',
                '11:50 - 13:20',
                '13:30 - 15:00',
                '15:10 - 16:40',
                '16:45 - 18:15']
    
    if weekday_num == 3:
        time = ['08:30 - 10:00',
                '10:10 - 11:40',
                '11:50 - 12:20',
                '12:30 - 14:00',
                '14:10 - 15:40',
                '16:50 - 17:20']
    
    if (self.__extra_index):
      for index in self.__extra_index:
        time.insert(index + 1, time[index])

    return time

  def get_dictionary(self):
    lessons = self.get_lessons()
    lessons_bool = list(map(lambda i : True if i == '' else False,lessons))
    if all(lessons_bool):
      return None
    return  {'default' : self.get_teachers(),
            'lesson':lessons,
            'cabinet' : self.get_cabinets(),
            'time':self.get_time(),
            'number': self.get_numbers()}

class StudentsTable:
  """
Этот класс, обрабатывает таблицу расписания с информацией о занятиях для разных групп учащихся. Класс StudentsTable предназначен для обновления таблицы и упрощения извлечения из нее информации. Класс имеет несколько методов, которые помогают извлекать данные из таблицы, таких как get_group_names, который возвращает список всех имен групп, и get_all_groups_dictionary, который возвращает словарь, содержащий информацию о классах для всех групп учащихся.
  """

  def __init__(self) -> None:
    self.__TABLE__ = self.__update_table(get_table('1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU')[:24])
    """
Данная строка позволяет обработать таблицу расписания и гарантирует, что каждый столбец таблицы имеет четное число элементов. 
Это упрощает дальнейшую обработку таблицы в методах класса, которые используют эту таблицу для получения информации о занятиях для каждой группы.
    """
    self.__TABLE__ = Table(map(lambda x : [''] + x if len(x) % 2 != 0 else x, self.__TABLE__)) 

  def __update_table(self,table) -> Table :
    """
Данная функция редназначена для обновления таблицы расписания, содержащей информацию о занятиях для всех групп студентов.\n
Функция принимает в качестве аргумента объект класса Table, содержащий информацию о расписании. Затем функция итерируется по всем столбцам и строкам таблицы, используя регулярное выражение для поиска в каждой ячейке строки, содержащей название группы.\n
Если такая строка найдена, то она заменяется на название группы. Если же название группы не найдено в ячейке, то ячейка остается без изменений.\n
    """
    changed_table = []
    for column in table:
      changed_column = []
      for ellement in column:
        group_in_string = re.search(r'\S\w*-[\.А-Я-0-9]+', ellement)
        changed_column.append(group_in_string.group() if group_in_string else ellement)
      changed_table.append(changed_column)
    return Table(changed_table)

  def __get_exception_groups(self) -> list :
    """Данный метод представляет собой функцию, 
    которая получает все группы из таблицы и возвращает список строк,
    содержащих названия групп-исключений(Находятся в самом низу таблицы)."""
    exception_groups = []
    for column in self.__TABLE__:
      string_from_column = ' '.join(column)
      result = re.findall(r'\S\w*-[\.А-Я-0-9]+', string_from_column)
      if not result:
        continue
      exception_groups.append(result[-1])
    return tuple(exception_groups)

  def get_group_names(self) -> tuple:
    """Данный метод представляет собой функцию, 
    которая получает все группы из таблицы и возвращает список строк,
    содержащих названия групп."""
    string_from_table = ' '.join(tuple(chain(*self.__TABLE__)))
    result = re.findall(r'\S\w*-[\.А-Я-0-9]+', string_from_table)
    return tuple(result)

  def get_all_groups_dictionary(self) -> dict | None:
    """
Данная функция предназначена для получения словаря, содержащего данные о занятиях для всех групп КГТТ. 
Она возвращает словарь, где каждый ключ соответствует названию группы, а каждое значение - это словарь, содержащий данные о занятиях для этой группы.\n\n
Функция использует методы из класса CropTable для получения информации о расписании для каждой группы. Для этого она вызывает метод get_group_names() для получения списка названий всех групп студентов. Затем она итерируется по списку групп и создает объект CropTable для каждой группы, используя метод self.__TABLE__.get_index(gr_1) для определения индекса столбца, соответствующего этой группе.\n
Затем функция использует методы объекта CropTable, чтобы получить информацию о занятиях для каждой группы и сохраняет эту информацию в словаре dictionary. Ключом для каждой записи словаря является название группы, а значением - словарь, содержащий информацию о занятиях для этой группы.\n
В конце функция возвращает словарь dictionary, содержащий информацию о занятиях для всех групп студентов.
    """
    dictionary = {}
    __GROUPS__ = self.get_group_names()
    __Exception_groups = self.__get_exception_groups()
    
    
    for gr_1,gr_2 in zip_longest(__GROUPS__,__GROUPS__[1:],fillvalue=''):
      keys = (self.__TABLE__.get_index(gr_1).row+1,self.__TABLE__.get_index(gr_2).row)
      if gr_1 in __Exception_groups:
        keys = (self.__TABLE__.get_index(gr_1).row+1,self.__TABLE__.get_index(gr_1).row+12)
      
      column_index = self.__TABLE__.get_index(gr_1).column

      data = _CropTableStudents(
        keys=keys,
        group=gr_1,
        column_index=column_index,
        table=self.__TABLE__)

      dictionary[gr_1]  = data.get_dictionary()
      
    return dictionary

def get_all_dictionaries() -> dict:
  """
Фунция создает общий словарь для преподователей и студентов
  """
  ST = StudentsTable().get_all_groups_dictionary()
  TT = TeachersTable().get_all_teachers_dictionary()
  return ST | TT

def update_json_file(new_data:dict = {}) -> None:
    """
Данная функция предназначена для обновления файла в формате JSON с помощью данных, представленных в виде словаря Python.
Она обновляет данные в файле "timetable.json", добавляя в него новые данные из переданного словаря.
\nЕсли файл "timetable.json" не найден, функция создаст его и запишет туда все данные из метода self.get_all_groups_dictionary(), который вернет словарь со всеми группами студентов в формате, подходящем для записи в JSON.
    """
    try:
      with open("timetable.json",'r',encoding='UTF-8') as js:
        json_data = json.loads(js.read())
        if json_data:
          json_data = json_data | new_data
        
      with open("timetable.json",'w',encoding='UTF-8') as js:
        json.dump(obj=json_data,
                  fp = js,
                  ensure_ascii=False,
                  indent=4)  

    except FileNotFoundError :
      with open("timetable.json",'w',encoding='UTF-8') as js:
        json.dump(obj=get_all_dictionaries(),
                  fp = js,
                  ensure_ascii=False,
                  indent=4)

def get_creation_date():

# путь к файлу, дату создания которого мы хотим получить
  path = 'timetable.json'
  # получение времени создания файла
  created_time = os.path.getctime(path)

  # преобразование времени в строку с форматированием
  created_time_str = time.strftime('%Y-%m-%d в %H:%M:%S', time.localtime(created_time))

  # вывод даты создания файла
  return f'Последнее обновление расписания : {created_time_str}'

class Configurator():
  
  def __init__(self,group:str,config_string : str = '(number)[time]|cabinet| lesson - default\n') -> None:
    self.config_string = config_string
    self.json_data : dict = self.__get_json_data()[group]


  def __get_clean_row(self)->str:
    string = self.config_string
    for value in ('default','lesson','cabinet' ,'time','number'):
      if value in self.config_string:
        string = string.replace(value,"{"+str(value)+"}")
    return string
    
  def __get_reverse_values(self)->list:
    values = []
    for value in ('default','lesson','cabinet' ,'time','number'):
      if value not in self.config_string:
        values.append(value)
        
    return values

  def __get_json_data(self)->None:
      with open("timetable.json",'r',encoding='UTF-8') as js:
        json_data = json.loads(js.read())
        return json_data
    
  def configuration(self) -> list:
    
    for key in self.__get_reverse_values():
      del self.json_data[key]

    rows = ''
    keys = list(self.json_data.keys())
    for value in zip(*self.json_data.values()):
      format_dict = {k:v for k, v in zip(keys, value)}
      row = self.__get_clean_row().format(**format_dict)
      rows = rows + row
    return rows
    
      
     

print(Configurator('ЭП-22-9').configuration())


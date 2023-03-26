from schedule.GoogleTable import get_table, Table
import re
from itertools import chain,zip_longest
from datetime import datetime


class _CropTableStudents():
  """
Этот класс предоставляет методы для получения информации о уроках, учителях, кабинетах, времени и порядке уроков для конкретной группы. Он предназначен для использования вместе с классом StudentsTable.
  """
  def __init__(self,table : Table,group:str,column_index:int,keys:tuple,date) -> None:
    self.key_1,self.key_2 = keys
    self.__column_index = column_index
    self.__TABLE__ = table
    self.group  = group
    self.__extra_index = self.__get__extra_index()
    self.date = date
  
  def __get__extra_index(self) -> tuple :
    """Данный метод является функцией, которая возвращает кортеж индексов из обрезаной под определненный диапазон таблицы , где стоят дополнительные предметы"""
    lesson = self.__TABLE__[self.__column_index][self.key_1:self.key_2][::2]
    
    lesson_2 = self.__TABLE__[self.__column_index + 2][self.key_1:self.key_2][::2]
   
    
    return tuple([i for i,(l1,l2) in enumerate(zip(lesson,lesson_2)) if l1 and l2 ])
  
  @staticmethod
  def __even_it_out(lst:list)->list:
    count_start =0
    count_end = 0
    
    for i in lst:
      if i == '':
        count_start+=1
      else : break
      
    for i in lst[::-1]:
      if i == '':
        count_end+=1
      else : break

    if count_start % 2 != 0:
      lst.insert(0,'')
    if count_end % 2 != 0:
      lst.append('')
      
    return lst
  
  @staticmethod
  def __find_range(lst : list)->tuple:
    first, last = None, None
    for i, s in enumerate(lst):
        if s != '':
            if first is None:
                first = i
            last = i
    return (first, last+1) if first is not None else (None, None)
  
  @staticmethod
  def __get_english_strings(arrays) -> list:
    result_arrays = []
    for i in arrays:
      array = []
      for word in i:
        
        english_chars = ""
        
        for char in word:
          
          if char.isalpha() and char.isascii():
            english_chars += char
            
        array.append(english_chars)
      result_arrays.append(array)
    
    return result_arrays
  
  def get_lessons(self) -> list:
    lesson = self.__even_it_out(self.__TABLE__[self.__column_index][self.key_1:self.key_2])[::2]
    lesson_2 = self.__even_it_out(self.__TABLE__[self.__column_index + 2][self.key_1:self.key_2])[::2]
    
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

  def get_default(self) -> list:
    teachers = self.__even_it_out(self.__TABLE__[self.__column_index][self.key_1:self.key_2])[1::2]
    teachers_2 = self.__even_it_out(self.__TABLE__[self.__column_index+2][self.key_1:self.key_2])[1::2]

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
    cabinets = self.__even_it_out(self.__TABLE__[self.__column_index+4][self.key_1:self.key_2])[::2]
    cabinets_2 = self.__even_it_out(self.__TABLE__[self.__column_index+1][self.key_1:self.key_2])[::2]
    cabinets_3 = self.__even_it_out(self.__TABLE__[self.__column_index+3][self.key_1:self.key_2])[::2]
    
    
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
  
    date_str = re.search(r'\d{2}\.\d{2}\.\d{4}', ' '.join(self.__TABLE__[0])).group()
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

  def get_distance(self) -> list:
    distance = []

    for c1,c2,c3 in zip(*self.__get_english_strings([self.get_lessons(),self.get_default(),self.get_cabinets()])):
      if c1 == c2 == c3:
        distance.append(c1)
      elif c2 and c3:
        distance.append(c2)
        distance.append(c3)
      elif c1:
        distance.append(c1)
      elif c2 and not c3 :
        distance.append(c2)
      elif c3 and not c2:
        distance.append(c3)
    return distance
        
  def __get_clean_data(self):
    lessons = self.get_lessons()
    default = self.get_default()
    cabinets = self.get_cabinets()
    distance = self.get_distance()
    
    for i,(l,d) in enumerate(zip(lessons,distance)):
      repl = l.replace(d,'')
      lessons[i] = repl.strip()
      
    for i,(de,d) in enumerate(zip(default,distance)):
      repl = de.replace(d,'')
      default[i] = repl.strip()

    for i,(c,d) in enumerate(zip(cabinets,distance)):
      repl = c.replace(d,'')
      cabinets[i] = repl.strip()
    
    return lessons,default,cabinets

  def get_dictionary (self) -> dict:
    lessons = self.get_lessons()
    r1,r2 = self.__find_range(lessons)
    lessons_bool = list(map(lambda i : True if i == '' else False,lessons))
    clean_data = self.__get_clean_data()
    
    if all(lessons_bool):
      return None
    return  {'default' :clean_data[1][r1:r2],
            'lesson':clean_data[0][r1:r2],
            'cabinet' : clean_data[2][r1:r2],
            'time':self.get_time()[r1:r2],
            'number': self.get_numbers()[r1:r2],
            'distance': self.get_distance()[r1:r2],
            'date' : self.date}

 
    

class StudentsTable:

  def __init__(self) -> None:
    self.__TABLE__ = self.__update_table(get_table('студентам')[:24])

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

  def __get_date_for_students(self):
    string = re.search(r'\d{2}\.\d{2}\.\d{4}', ' '.join(self.__TABLE__[0])).group()
    return string

  def get_group_names(self) -> tuple:
    """Данный метод представляет собой функцию, 
    которая получает все группы из таблицы и возвращает список строк,
    содержащих названия групп."""
    string_from_table = ' '.join(tuple(chain(*self.__TABLE__)))
    result = re.findall(r'\S\w*-[\.А-Я-0-9]+', string_from_table)
    return tuple(result)

  def get_all_dictionary(self) -> dict | None:
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
        table=self.__TABLE__,
        date = self.__get_date_for_students())

      dictionary[gr_1]  = data.get_dictionary()
      
    return dictionary

  def test(self,group):

    __GROUPS__ = self.get_group_names()
    __Exception_groups = self.__get_exception_groups()
    
    
    for gr_1,gr_2 in zip_longest(__GROUPS__,__GROUPS__[1:],fillvalue=''):
      keys = (self.__TABLE__.get_index(gr_1).row+1,self.__TABLE__.get_index(gr_2).row)
      if gr_1 in __Exception_groups:
        keys = (self.__TABLE__.get_index(gr_1).row+1,self.__TABLE__.get_index(gr_1).row+12)
      
      column_index = self.__TABLE__.get_index(gr_1).column
        
      if gr_1 == group:
        return _CropTableStudents(
          keys=keys,
          group=gr_1,
          column_index=column_index,
          table=self.__TABLE__,
          date = self.__get_date_for_students())

def get_dictionary_for_students():
  return StudentsTable().get_all_dictionary()


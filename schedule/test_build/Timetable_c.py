from GoogleTable import GoogleTable, table
import re
from itertools import chain,zip_longest
from datetime import datetime
import json
from dataclasses import dataclass



  
  

class Preparation:
  
  def __init__(self) -> None:
    self.__TABLE__ = table(GoogleTable('1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU').columns()[:24])
    
  def get_all_groups(self) -> tuple:
    """Данный метод представляет собой функцию, 
    которая получает все группы из таблицы и возвращает список строк,
    содержащих названия групп."""
    string_from_table = ' '.join(tuple(chain(*self.__TABLE__)))
    result = re.findall(r'\S\w*-[\.А-Я-0-9]+', string_from_table)
    return tuple(result)

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

  def _get_changed_table_for_indexes(self) -> table :
    """Данный метод является функцией, которая преобразует исходную таблицу, 
    состоящую из списков, в таблицу, 
    где каждый элемент представляет собой строку с названием группы.\n
    P.S Если строка найдена, то ее значение добавляется в список changed_column, 
    иначе в список добавляется пустая строка.
    """
    changed_table = []
    for column in self.__TABLE__:
      changed_column = []
      for ellement in column:
        group_in_string = re.search(r'\S\w*-[\.А-Я-0-9]+', ellement)
        changed_column.append(group_in_string.group() if group_in_string else '')
      changed_table.append(changed_column)
    return table(changed_table)

  def _get_dictionary_span(self) -> dict:
      """Метод создает словарь, где ключами являются названия групп, 
      а значениями - диапазоны строк таблицы, 
      соответствующие каждой группе."""
      dictionary = {}
      groups = self.get_all_groups()
      table_for_find_index= self._get_changed_table_for_indexes()
      
      for gr_1,gr_2 in zip_longest(groups,groups[1:],fillvalue=''):
        value = table_for_find_index.bindex(gr_1).row+1,table_for_find_index.bindex(gr_2).row
        if gr_1 in self.__get_exception_groups():
          value = table_for_find_index.bindex(gr_1).row+1,table_for_find_index.bindex(gr_1).row+12
        dictionary[gr_1] = value
      return dictionary

  
   
@dataclass
class CropTable():
  group : str 
  crop_table_obj : table
  column_index : int
  extra_index : tuple
  counting_column_for_number : list
  date_str : str
  
  
  def get_lessons(self) -> list:
    
    lesson = self.crop_table_obj[0][::2]
    lesson_2 = self.crop_table_obj[2][::2]
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
    teachers = self.crop_table_obj[0][1::2]
    teachers_2 = self.crop_table_obj[2][1::2]
  
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
        result.append(t1)
        
    return tuple(result)

  def get_cabinets(self) -> list:
    cabinets = self.crop_table_obj[4][::2]
    cabinets_2 = self.crop_table_obj[1][::2]
    cabinets_3 = self.crop_table_obj[3][::2]
    
    
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
        
    return tuple(result)
      
  def get_numbers(self) -> list:
    
    result = self.counting_column_for_number
    result = [i for i in result if i != '']
    
    if (self.extra_index):
      for index in self.extra_index:
        result.insert(index+1,f'{result[index]}.2')
        result[index] = f'{result[index]}.1'
        
    return tuple(result)
   
  def get_time(self) -> list:
  
    def day_of_week() -> int:
      """Метод возвращает номер дня недели 
      для заданной даты в формате "День.Месяц.Год"."""
      date_str = re.search(r'\d{2}\.\d{2}\.\d{4}', self.date_str).group() # дата в формате "День.Месяц.Год"
      date_obj = datetime.strptime(date_str, '%d.%m.%Y')
      weekday_num = date_obj.isoweekday()
      return weekday_num  

    time = ['08:30 - 10:00',
                '10:10 - 11:40',
                '11:50 - 13:20',
                '13:30 - 15:00',
                '15:10 - 16:40',
                '16:45 - 18:15']
    
    if day_of_week() == 3:
        time = ['08:30 - 10:00',
                '10:10 - 11:40',
                '11:50 - 12:20',
                '12:30 - 14:00',
                '14:10 - 15:40',
                '16:50 - 17:20']
    
    if (self.extra_index):
      for index in self.extra_index:
        time.insert(index + 1, time[index])

    return tuple(time)

class Processing(Preparation):

  def __init__(self) -> None:
    super().__init__()
    
  def crop_table(self,group:str) -> CropTable:
    
    def __get_extra_index() -> tuple: 
      """Данный метод является функцией, которая возвращает кортеж индексов из обрезаной под определненный диапазон таблицы , где стоят дополнительные предметы
      """
      lesson = Table[0][::2]
      lesson_2 = Table[2][::2]
      
      return tuple([i for i,(l1,l2) in enumerate(zip(lesson,lesson_2)) if l1 and l2 ])
    
    
    key_1,key_2 = self._get_dictionary_span()[group]
    
    column_index = self._get_changed_table_for_indexes().bindex(group).column# Индекс колонки для группы 
    Table = list(map(lambda x : x[key_1:key_2],self.__TABLE__))[column_index:column_index+5] # Обрезка для 
    Table = list(map(lambda x : [''] + x if len(x) % 2 != 0 else x,Table)) 
    extra_index = __get_extra_index()
    counting_column = list(map(lambda x : x[key_1:key_2],self.__TABLE__))
    counting_column = list(map(lambda x : [''] + x if len(x) % 2 != 0 else x,counting_column))[0]
    
    return CropTable(group=group,
                     crop_table_obj=Table,
                     column_index = column_index,
                     extra_index=extra_index,
                     counting_column_for_number=counting_column,
                     date_str=self.__TABLE__[0][0])
  
 
 
print(Processing().crop_table('1ИСИП-21-9').get_numbers())




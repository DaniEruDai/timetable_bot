from GoogleTable import get_table, Table
import re
from itertools import chain,zip_longest
from datetime import datetime


class _CropTableTeachers():
  """
Класс CropTable предназначен для работы с таблицами и обработки данных в них. 
\nОн может быть использован, например, для выделения определенных данных из таблицы, фильтрации их и преобразования в нужный формат.
  """

  def __init__(self,table : Table,teacher:str,column_index:int,keys:tuple,date:str) -> None:
    self.key_1,self.key_2 = keys
    self.__column_index = column_index
    self.__TABLE__ = table
    self.teacher  = teacher
    self.date = date
    
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
  def __find_range(lst:list) -> tuple:
    first, last = None, None
    for i, s in enumerate(lst):
        if s != '':
            if first is None:
                first = i
            last = i
    return (first, last+1) if first is not None else (None, None)
  
  def get_lessons(self) -> list:
    lesson = self.__even_it_out(self.__TABLE__[self.__column_index][self.key_1:self.key_2])[1::2]

    return lesson

  def get_default(self) -> list:
    default = self.__even_it_out(self.__TABLE__[self.__column_index][self.key_1:self.key_2])[::2]
    return default

  def get_cabinets(self) -> list: 
    cabinets = self.__even_it_out(self.__TABLE__[self.__column_index+1][self.key_1:self.key_2])[::2]
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

  def get_dictionary(self) -> dict:
    lessons = self.get_lessons()
    r1,r2 = self.__find_range(lessons)
    lessons_bool = list(map(lambda i : True if i == '' else False,lessons))
    
    
    if all(lessons_bool):
      return None
    return  {'default' : self.get_default()[r1:r2],
            'lesson':lessons[r1:r2],
            'cabinet' : self.get_cabinets()[r1:r2],
            'time':self.get_time()[r1:r2],
            'number': self.get_numbers()[r1:r2],
            'date' : self.date}


class TeachersTable:

  def __init__(self) -> None:
    self.__TABLE__ = self.__update_table(get_table('преподавателям')[:9])

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

  def __get_date_for_teachers(self):
    string = re.search(r'\d{2}\.\d{2}\.\d{4}', ' '.join(self.__TABLE__[0])).group()
    return string
  
  def get_teacher_names(self) -> tuple:
    string_from_table = ' '.join(tuple(chain(*self.__TABLE__)))
    result = re.findall(r'[А-ЯЁ][а-яё]+\s+[А-ЯЁ]\.\s+[А-ЯЁ]\.', string_from_table)
    return result

  def get_all_dictionary(self) -> dict | None:
   
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
        table=self.__TABLE__,
        date=self.__get_date_for_teachers())

      dictionary[t_1] = data.get_dictionary()
    
    return dictionary

def get_dictionary_for_teachers():
  return TeachersTable().get_all_dictionary()
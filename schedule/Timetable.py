from GoogleTable import GoogleTable, table
import re
from itertools import chain
import datetime

class TableExceptions:
  class VoidTable(Exception):
    ...

class Preparation:
  
  def __init__(self) -> None:
    self.table = table(GoogleTable('1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU').columns()[:24])
    
  def all_groups(self) -> list:
    string_from_table = ' '.join(tuple(chain(*self.table)))
    result = re.findall(r'\S\w*-[\.А-Я-0-9]+', string_from_table)
    return result

  def __exception_groups__(self) -> list :
    exception_groups = []
    for column in self.table:
      string_from_column = ' '.join(column)
      result = re.findall(r'\S\w*-[\.А-Я-0-9]+', string_from_column)
      if not result:
        continue
      exception_groups.append(result[-1])
    return exception_groups

  def __dictionary_keys__(self) -> dict:
    dkey = {}
    groups_1 = self.all_groups()
    groups_2 = groups_1[1:]
    groups_2.append('')
    t = table(self.table)
    for f,s in zip(groups_1,groups_2):
      value = t.bindex(f)[1]+1,t.bindex(s)[1]
      if f in self.__exception_groups__():
        value = t.bindex(f)[1]+1,t.bindex(f)[1]+12
      dkey[f] = value
    return dkey 
  
  def day_of_week(self):
    print(self.table[0])
    
    
class Processing(Preparation):
    
  def __init__(self,group) -> None:
    super().__init__()
    self.group = group
    key_1,key_2 = self.__dictionary_keys__()[self.group]
    self.main_index = table(self.table).bindex(self.group)[0]
    self.number = self.table[0][key_1:key_2][::2]
    self.table = table(list(map(lambda x : x[key_1:key_2],self.table)))[self.main_index:self.main_index+5] # Обрезка всей таблицы
  
  def __void_cell__(self) -> list :
    return [i for i, x in enumerate(self.lessons()) if x == ""]

  def lessons(self)-> list:
    lesson_2 = self.table[2][::2]
    lesson = self.table[0][::2]
    
    indices  = [i for i, x in enumerate(lesson_2) if x != ""]
    iter_count =0
    for i in indices:
      
      if lesson[i] == '' :
        lesson[i] = lesson_2[i]
      else:
        lesson.insert(i+iter_count,lesson_2[i])
        iter_count += 1

    return lesson

  def teachers(self)-> list:
    teachers = self.table[0][1::2]
    teachers_2 = self.table[2][1::2]
  
    iter_count = 1
    indices  = [i for i, x in enumerate(teachers_2) if x != ""]
    for i in indices:
      if teachers[i] == '' :
        teachers[i] = teachers_2[i]
      else:
        teachers.insert(i+iter_count,teachers_2[i])
        iter_count += 1
         
        
    return teachers

  def cabinets(self)->list:
    cabinets = self.table[4][::2]
    cabinets_2 = self.table[1][::2]
    cabinets_3 =self.table[3][::2]
  
    result =[]
    for _, (с1, с2, с3) in enumerate(zip(cabinets, cabinets_2, cabinets_3)):
      if с1:
          result.append(с1)
      else:
          if с2 and с3:
              result.append(с2)
              result.append(с3)
          elif с2:
              result.append(с2)
          elif с3:
              result.append(с3)
    
    for i in self.__void_cell__():
      result.insert(i,'')         
              
      
    return result

  def numbers(self)-> list:
    ...
  
  def time(self):
    
    
    
    length = len(self.lessons())
    if day_of_week() == 3:
        time = ['08:30 - 10:00',
                '10:10 - 11:40',
                '11:50 - 12:20',
                '12:30 - 14:00',
                '14:10 - 15:40',
                '16:50 - 17:20'][:length]
    else:
        time = ['08:30 - 10:00',
                '10:10 - 11:40',
                '11:50 - 13:20',
                '13:30 - 15:00',
                '15:10 - 16:40',
                '16:45 - 18:15'][:length]

    return time

  
# for i in ('1ТЭО-21-9','ПРУМ-21-9','ЭП-22-9','1ИСИП-21-9'):
#   print(f'\n---------------{i}-------------------------\n')



print(Processing('1ИСИП-21-9').numbers()) 
  


  











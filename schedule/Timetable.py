from GoogleTable import GoogleTable, table
import re
from itertools import chain


class TableExceptions:
  class VoidTable(Exception):
    ...



class Preparation:
  
  def __init__(self) -> None:
    self.table = table(GoogleTable('1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU').columns(True)[:24])

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

  def header(self):
    checker = [ellement for ellement in list(chain(*self.table)) if 'расписание' in ellement.lower()]
    if checker:
      return checker[0]
    raise TableExceptions.VoidTable('Таблица пустая!')
  
class Processing(Preparation):
    
  def __init__(self,group) -> None:
    super().__init__()  
    key_1,key_2 = self.__dictionary_keys__()[self.group]
    self.table = table(list(map(lambda x : x[key_1:key_2],self.table))) # Обрезка всей таблицы
    self.group = group
    
    
    
  
    
  

  
print(Processing('1ОГР-21-9').indexes())
  
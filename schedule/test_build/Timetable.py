from GoogleTable import GoogleTable, table
import re
from itertools import chain
from datetime import datetime

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
  
class Processing(Preparation):
    
  def __init__(self,group) -> None:
    super().__init__()
    self.key_1,self.key_2 = self.__dictionary_keys__()[group]
    self.main_index = table(self.table).bindex(group)[0]
    
    
    self.number = self.table[0][self.key_1:self.key_2]
    self.date_str = self.table[0][0]
    
    
    self.table = table(list(map(lambda x : x[self.key_1:self.key_2],self.table)))[self.main_index:self.main_index+5] # Обрезка всей таблицы
    self.table = list(map(lambda x : [''] + x if len(x) % 2 != 0 else x,self.table))
    
  def lessons(self) -> list:
    self.extraindex = []
    lesson = self.table[0][::2]
    lesson_2 = self.table[2][::2]
    result = []
    
    for i,(l1,l2) in enumerate(zip(lesson,lesson_2)):
      
      if not l1 and not l2:
        result.append(l1)
        
      elif l1 and l2:
        self.extraindex.append(i)
        result.append(l1)
        result.append(l2)
      
      elif l1 and not l2:
        result.append(l1)
      
      elif l2 and not l1:
        result.append(l2)
        
    return result

  def __extraindex__(self) -> list: 
    extraindex = []
    lesson = self.table[0][::2]
    lesson_2 = self.table[2][::2]
    
    for i,(l1,l2) in enumerate(zip(lesson,lesson_2)):
      if l1 and l2:
        extraindex.append(i)
    return extraindex
  
  def teachers(self) -> list:
    teachers = self.table[0][1::2]
    teachers_2 = self.table[2][1::2]
  
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
        
    return result

  def cabinets(self) -> list:
    cabinets = self.table[4][::2]
    cabinets_2 = self.table[1][::2]
    cabinets_3 =self.table[3][::2]
    
    
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
      
  def numbers(self) -> list:
    
    result = self.number
    result = [i for i in result if i != '']
    
    
    if (extraindex := self.__extraindex__()):
      for index in extraindex:
        result.insert(index+1,f'{result[index]}.2')
        result[index] = f'{result[index]}.1'
    return result
   
  def time(self) -> list:
  
    def day_of_week()-> int:
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
    
    if (extraindex := self.__extraindex__()):
      for index in extraindex:
        time.insert(index + 1, time[index])

    return time


# print(f"{Processing('ДП-20-9').numbers()}")


alld= Preparation().all_groups()
issues = []
for i in alld:
  try:
    print(f'--------------------------{i}------------------------------')
    print(f"{Processing(i).numbers()}")
    print(f"{Processing(i).time()}")
    print(f"{Processing(i).lessons()}\n\n")
    print('-----------------------------------------------------------')
    
  except Exception as e: issues.append([i,e])

print('Все окончено')

print('Ошибки : \n')
for d in issues:
  print(f'{d}\n')

  











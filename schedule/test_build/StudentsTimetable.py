from GoogleTable import GoogleTable, table,TableExceptions
import re
from itertools import chain
from datetime import datetime
from itertools import zip_longest
import json


class Students:
  
  def __init__(self) -> None:
    self.table = table(GoogleTable('1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU').columns()[:24])
      
  def all_groups(self) -> list:
    string_from_table = ' '.join(tuple(chain(*self.table)))
    result = re.findall(r'\S\w*-[\.А-Я-0-9]+', string_from_table)
    return result

  def __exception_groups(self) -> list :
    exception_groups = []
    for column in self.table:
      string_from_column = ' '.join(column)
      result = re.findall(r'\S\w*-[\.А-Я-0-9]+', string_from_column)
      if not result:
        continue
      exception_groups.append(result[-1])
    return exception_groups

  def __format_table(self) -> table:
    def process_column(column):
      for element in column:
        match = re.search(r'\S\w*-[\.А-Я-0-9]+', element)
        yield match.group() if match else None
    return table([tuple(process_column(column)) for column in self.table])
  
  def update_json(self):
    dictionary = {}
    groups = self.all_groups()
    formated_table = self.__format_table()
    for gr_1,gr_2 in zip_longest(groups,groups[1:],fillvalue=''):
      localy_dict = {}
      try:
        column_index = formated_table.bindex(gr_1).column # Индекс основной колонки
        up_index = formated_table.bindex(gr_1).row+1 # Индекс верхней границы
        down_index = formated_table.bindex(gr_2).row # Индекс нижней границы
        if gr_1 in self.__exception_groups():
          down_index = formated_table.bindex(gr_1).row +12
      except TableExceptions.VoidValue:
        pass
      
      
      
      local_table = list(map(lambda x : [''] + x if len(x) % 2 != 0 else x,self.table))
      local_table = table(list(map(lambda x : x[up_index:down_index],local_table)))[column_index:column_index+5] # Обрезка всей таблицы
      
      localy_dict['teacher'] = self.teachers(local_table)
      localy_dict['cabinet'] =  self.cabinets(local_table)
      localy_dict['number'] =  self.numbers(local_table,up_index,down_index)
      localy_dict['lesson'] =  self.lessons(local_table)
      localy_dict['time'] =  self.lessons(local_table)
      
      dictionary[gr_1] = localy_dict
      
    with open('result.json','w') as js:
      json.dump(dictionary,js,ensure_ascii=False,indent=4)

      
  def get_extra_item_index(self,local_table) -> list: 
    extraindex = []
    lesson = local_table[0][::2]
    lesson_2 = local_table[2][::2]
    
    for i,(l1,l2) in enumerate(zip(lesson,lesson_2)):
      if l1 and l2:
        extraindex.append(i)
    return extraindex
  
  
  
  """Методы для структурирования информации"""
  def lessons(self,local_table) -> list:
    self.extraindex = []
    lesson = local_table[0][::2]
    lesson_2 = local_table[2][::2]
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

  def teachers(self,local_table) -> list:
    teachers = local_table[0][1::2]
    teachers_2 = local_table[2][1::2]
  
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

  def cabinets(self,local_table) -> list:
    cabinets = local_table[4][::2]
    cabinets_2 = local_table[1][::2]
    cabinets_3 =local_table[3][::2]
    
    
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
      
  def numbers(self,local_table,key_1,key_2) -> list:
    result = self.table[0][key_1:key_2]
    result = [i for i in result if i != '']
    
    
    
    if (extraindex := self.get_extra_item_index(local_table)):
      for i in extraindex:
        result.insert(i+1,f'{result[i]}.2')
        result[i] = f'{result[i]}.1'
    return result
   
  def time(self,local_table) -> list:
  
    def day_of_week()-> int:
      date_str = re.search(r'\d{2}\.\d{2}\.\d{4}', self.table[0][0]).group() # дата в формате "День.Месяц.Год"
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
    
    if (extraindex := self.get_extra_item_index(local_table)):
      for index in extraindex:
        time.insert(index + 1, time[index])

    return time


print(Students().update_json())



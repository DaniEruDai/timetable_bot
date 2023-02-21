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
    self.group = group
    key_1,key_2 = self.__dictionary_keys__()[self.group]
    main_index = table(self.table).bindex(self.group)[0]
    self.table = table(list(map(lambda x : x[key_1:key_2],self.table)))[main_index:main_index+5] # Обрезка всей таблицы
    
    
  def lessons(self):
    
    def clear(massive):
      return [ell for ell in massive if ell!='']
      
    di = {
      'lessons': [self.table[0][::2],self.table[2][::2]],
      'teachers': [self.table[0][1::2],self.table[2][1::2]],
      'cabinets': [self.table[4][::2],self.table[1][::2],self.table[3][::2]]
    }
    
    
    lessons = self.table[0][::2],self.table[2][::2]
    
    main_lessons = self.table[0][::2]
    extra_lessons = self.table[2][::2]
    
    teachers = [self.table[0][1::2],self.table[2][1::2]]
    
    main_teachers = self.table[0][1::2]
    extra_teachers = self.table[2][1::2]
    
    cabinets = [self.table[4][::2],self.table[3][::2],self.table[1][::2]]
    
    main_cabinets = self.table[4][::2]
    extra2_cabinets = self.table[3][::2]
    extra1_cabinets = self.table[1][::2]
    
    
    
    
    
    L_index = [i for i, ltr in enumerate(di['lessons'][1]) if ltr != '']
    C_index = [i for i, ltr in enumerate(di['cabinets'][1]) if ltr != '']
    
    for i in L_index+C_index:
      cab = clear([main_cabinets[i],extra1_cabinets[i],extra2_cabinets[i]])
      main_cabinets[i] = cab
      teach = clear([main_teachers[i],extra_teachers[i]])
      main_teachers[i] = teach
      les = clear([main_lessons[i],extra_lessons[i]])
      main_lessons[i] = les
      
      
      
      
    for i,k in enumerate(main_lessons):
      if isinstance(k,list):
        continue
      main_lessons[i] = [k]
    
    main_lessons = list(chain(*main_lessons))
    
    print(main_lessons)
    # print(extra_lessons)
    
    
    print(main_teachers)
    # print(extra_teachers)
    
    print(main_cabinets)
    print(extra1_cabinets)
    # print(extra2_cabinets)
    
  
    
      
   
    
  
    
    
  

  
print(Preparation().all_groups())
  
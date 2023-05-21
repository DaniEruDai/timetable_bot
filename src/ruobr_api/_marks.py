from datetime import datetime
from dateutil.relativedelta import relativedelta
import emoji

class Marks:
  
  def __init__(self,list_of_marks : iter, date : str) -> None:
    self.__length_of_date = len(str(date))
    self.__date = date
    
    
    
    if self.__length_of_date == 4:
      start = datetime.strptime(f'0109{self.__date}', "%d%m%Y").date()
      dates = [start.strftime('%m.%Y')]+ [(start + relativedelta(months=date)).strftime('%m.%Y') for date in range(1, 9)]
    
    
    exp = {4:lambda cls :cls.date.strftime('%m.%Y') in dates,
              7:lambda cls :cls.date.strftime('%m.%Y') == date,
              10:lambda cls : cls.date.strftime('%d.%m.%Y') == date
              }[self.__length_of_date]
    
      
    self.__filtering = list(filter(exp, list_of_marks))
    self.__lessons = set(i.lesson for i in self.__filtering)

  def get_average_score(self)-> list:
    
    result = []
    for lesson in self.__lessons:
      temp_list = [lesson]
      summ = 0
      counter = 0
      for obj in self.__filtering:
        if obj.lesson == lesson:
          summ += obj.mark
          counter+=1
          
      temp_list.append(round(summ/counter,2))
      result.append(temp_list)
    return result

  def get_results_for_period(self) -> list:
    result = []
    for lesson in self.__lessons:
      temp_list = [lesson]
      marks = []
      for obj in self.__filtering:
        if obj.lesson == lesson:
          marks.append(obj.mark)
          
      temp_list.append(marks)
      result.append(temp_list)
    return result
  
  def get_text(self):
    
    MN = {
    1: f'январь {emoji.emojize(":snowflake:")}',
    2: f'феварль {emoji.emojize(":cold_face:")}',
    3: f'март {emoji.emojize(":ribbon:")}',
    4: f'апрель {emoji.emojize(":clown_face:")}',
    5: f'май {emoji.emojize(":man_dancing:")}',
    6: f'июнь {emoji.emojize(":fire:")}',
    7: f'июль {emoji.emojize(":person_surfing:")}',
    8: f'август {emoji.emojize(":tear-off_calendar:")}',
    9: f'сентябрь {emoji.emojize(":umbrella:")}',
    10: f'окятбрь {emoji.emojize(":jack-o-lantern:")}',
    11: f'ноябрь {emoji.emojize(":fog:")}',
    12: f'декабрь {emoji.emojize(":Christmas_tree:")}'}
    
    
    result = []
    for i in [self.get_average_score,self.get_results_for_period][self.__length_of_date not in (4,7)]():
      result.append(f'{i[0]} - {i[1]}')
    
    result.sort()
    if result:
      match len(self.__date):
        case 4:
          text =  f'Оценки за {self.__date} - {int(self.__date)+1} учебный год\n\n'
        case 7:
          text = f'Оценки за {MN[int(self.__date.split(".")[0])]}\n\n'
        case 10:
          text =  f'Оценки за {self.__date}\n\n'

      return text + "\n".join(result)
    else : 
      return f"Оценок за {self.__date} нет!"

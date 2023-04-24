class Schedule:
  def __init__(self,data : list):
    self.data = data

  def get_text(self)-> str:
    dictionary = {'time' : [] , 'lesson' : []}
    data = sorted(self.data, key= lambda x : x['start'])
    for i in data:
      dictionary['time'].append(f"{i['start'].split('T')[1][:5]} - {i['end'].split('T')[1][:5]}")
      dictionary['lesson'].append(f'{i["title"].splitlines()[0]}')

    rows = []
    for i in range(len(dictionary['time'])):
      row = f'|{dictionary["time"][i]}| {dictionary["lesson"][i]}'
      rows.append(row)
    return '\n'.join(rows)  

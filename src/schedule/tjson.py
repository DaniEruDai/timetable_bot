import json

def read_json(filename) -> dict:
  with open(filename,'r',encoding='UTF-8') as f:
    _object = json.loads(f.read())
  return _object

def write_json(filename , dictionary : dict =  None) -> None:
  with open(filename,'w',encoding='UTF-8') as f:
    json.dump(obj=dictionary,fp = f,ensure_ascii=False,indent=4)
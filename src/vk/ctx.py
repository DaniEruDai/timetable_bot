class CtxStorage():
  """
Данный класс CtxStorage представляет собой простой механизм хранения данных, доступных в рамках контекста выполнения программы.
  """
  @staticmethod
  def set(name : str , value : object):
    setattr(CtxStorage,str(name),value)

  @staticmethod
  def delete(name : str):
    delattr(CtxStorage,str(name))
  
  @staticmethod
  def get(name : str):
    return getattr(CtxStorage,str(name))
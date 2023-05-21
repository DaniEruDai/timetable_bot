class RuobrException(Exception):
    class NoDateException(Exception):
        pass

    class DateException(Exception):
        pass

    class AuthException(Exception):
        pass
    
    class EmptyScheduleException(Exception):
      ...
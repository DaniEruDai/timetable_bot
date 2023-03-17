from recipientgsheets import RecipientGoogleSheets
from filters import *
from fucntions import *



class __Hunter:

    def __init__(self, group):
        self._group = group
        self.__timetable = RecipientGoogleSheets('1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU')
        self._date = cut_date(self.__timetable.get_line()[0])
        self._table = initial_filtering(self.__timetable.get_all(), '')
        self._column_index = self.__timetable.indexes(group)[0]
        self.__exclusion_groups = self.__exclusion_groups()
        self.__dictionary_groups = self.__dictionary_groups()

        self.keys = self.__cutter_keys()
        
    def allgr(self):
      preparatory_list = [list(filter(groups, row)) for row in self._table if list(filter(groups, row))]
      return [a for b in preparatory_list for a in b]
    
    
    def __exclusion_groups(self) -> tuple:
        return tuple(tuple(filter(groups, row))[-1] for row in self._table if tuple(filter(groups, row)))

    def __dictionary_groups(self) -> dict:
        preparatory_list = [list(filter(groups, row)) for row in self._table if list(filter(groups, row))]
        preparatory_list = [a for b in preparatory_list for a in b]
        preparatory_list_2 = preparatory_list[1::]
        for ellement in preparatory_list_2:
            preparatory_list_2[preparatory_list_2.index(ellement)] = self.__timetable.indexes(ellement)[1]
        dictionary_groups = dict(zip(preparatory_list, preparatory_list_2))
        for key in self.__exclusion_groups:
            dictionary_groups[key] = self.__timetable.indexes(key)[1] + 21
        return dictionary_groups

    def __cutter_keys(self):
        group = self._group
        column = self._table[self._column_index]
        key_1 = column.index(group) + 1
        key_2 = self.__dictionary_groups[group]

        return key_1, key_2


class __Butcher(__Hunter):

    def __init__(self, group):
        super().__init__(group)
        self.lessons = self._lesson()
        self.main_index = tl_indexes(self.lessons)

    def __b_num(self):
        key_1, key_2 = self.keys
        serial_start = [f' {i} ' for i in self._table[0][key_1:key_2] if i != '']
        return serial_start

    def _teacher(self):
        key_1, key_2 = self.keys
        teacher = self._table[self._column_index][key_1:key_2]
        teacher_2 = self._table[self._column_index + 2][key_1:key_2]
        bad_cut(teacher, teacher_2)
        teacher_length = len(teacher) // 2
        teacher = teacher[1::2]
        teacher_2 = teacher_2[1::2]
        for i, t in enumerate(teacher_2):
            if teacher[i] == '' and t != '':
                teacher[i] = t
            elif t != '':
                teacher.insert(i + 1, t)

        del teacher_2

        if teacher_length != len(self.__b_num()):
            teacher.insert(0, '')
        return teacher

    def __les(self):
        key_1, key_2 = self.keys
        lesson = self._table[self._column_index + 2][key_1:key_2]
        lesson = [i for i in lesson if i != '']
        return lesson

    def _lesson(self):
        key_1, key_2 = self.keys
        lesson = self._table[self._column_index][key_1:key_2]
        lesson_2 = self._table[self._column_index + 2][key_1:key_2]
        bad_cut(lesson, lesson_2)
        lesson_length = len(lesson) // 2
        lesson = lesson[::2]
        lesson_2 = lesson_2[::2]

        for i, les in enumerate(lesson_2):
            if lesson[i] == '' and les != '':
                lesson[i] = les
            elif les != '':
                lesson.insert(i + 1, les)

        del lesson_2

        eng = list(set([s for s in lesson if 'Ино' in s]))
        if eng:
            eng, = eng
            for i, les in enumerate(lesson):
                if les == eng:
                    lesson[i] = 'Иностранный язык'

        if lesson_length != len(self.__b_num()):
            lesson.insert(0, '')

        return lesson

    def _cabinet(self):
        key_1, key_2 = self.keys
        cabinet = self._table[self._column_index + 4][key_1:key_2]
        cabinet_2 = self._table[self._column_index + 1][key_1:key_2]
        cabinet_3 = self._table[self._column_index + 3][key_1:key_2]
        bad_cut(cabinet, cabinet_2, cabinet_3)
        cabinet_length = len(cabinet) // 2
        cabinet = cabinet[::2]
        cabinet_2 = cabinet_2[::2]
        cabinet_3 = cabinet_3[::2]

        for i, c in enumerate(cabinet_2):
            if cabinet[i] == '' and c != '':
                cabinet[i] = c
            elif c != '':
                cabinet.insert(i + 1, c)

        for i, c in enumerate(cabinet_3):
            if cabinet[i] == '' and c != '':
                cabinet[i] = c
            elif c != '':
                cabinet.insert(i + 1, c)

        for i, c in enumerate(cabinet):
            if c == '##':
                cabinet[i] = ''

        del cabinet_2, cabinet_3

        if cabinet_length != len(self.__b_num()):
            cabinet.insert(0, '')

        return cabinet

    def _number(self):
        key_1, key_2 = self.keys
        serial_start = [f' {i} ' for i in self._table[0][key_1:key_2] if i != '']

        for i, l in enumerate(serial_start):
            for y in self.main_index:
                if i == y:
                    serial_start.insert(i + 1, f'{serial_start[i].strip()}.2')
                    serial_start[y] = f'{serial_start[i].strip()}.1'

        once_indexes = all_tl_indexes(self.lessons)
        if once_indexes:
            for i in once_indexes:
                if self.__les() == [self.lessons[i], self._teacher()[i]]:
                    serial_start[i] = f'{serial_start[i].strip()}.2'
                else:
                    serial_start[i] = f'{serial_start[i].strip()}.1'

        return serial_start

    def _time(self):
        length = len(self.lessons)
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

        for index in self.main_index:
            time.insert(index + 1, time[index])

        return time

    def _cleaner(self):
        teacher = self._teacher()
        lesson = self.lessons
        cabinet = self._cabinet()
        number = self._number()
        time = self._time()

        indexes = []
        for t, ls, c in zip(enumerate(teacher), lesson, cabinet):
            if c == ls == t[1]:
                indexes.append(t[0])

            if t[1] == 'Чудакова А. Г.':
                if c == '':
                    cabinet[t[0]] = '121a'

        for i, n in enumerate(indexes):
            indexes[i] = n - i

        for i in indexes:
            number.pop(i)
            time.pop(i)
            cabinet.pop(i)
            lesson.pop(i)
            teacher.pop(i)

        return number, cabinet, lesson, teacher, time


class Scarecrow(__Butcher):

    def __init__(self, group, parameters = (
            ('number', 'time', 'cabinet', 'lesson', 'teacher'), ('(&)', ' {&}', ' |&| ', '&', ' - &'))):
        super().__init__(group)
        self.parameters, self.design = parameters

    def __configurator(self):
        data = self._cleaner()
        config = {
            'time': data[4],
            'number': data[0],
            'lesson': data[2],
            'teacher': data[3],
            'cabinet': data[1]
        }
        return [config[key] for key in self.parameters]

    def __create_string(self):
        data = self.__configurator()
        rows = [[catalog[index] for catalog in data] for index in range(len(data[0]))]
        rows = after_restoration(rows, self.design)
        for index, ellement in enumerate(rows):
            coincidence = cleaner(del_service_marks(self.design), rows[index])
            rows[index] = coincidence
            rows[index] = ''.join(ellement)

        if not rows:
            rows = 'Расписания нет , приятного отдыха!'
        return rows

    def get_text_without_information(self):
        string = self.__create_string()
        if isinstance(string, str):
            return string
        else:
            return '\n'.join(string)

    def get_information(self):
        return self._date

    def get_group(self):
        return self._group

    def get_text(self):
        return f'{self.get_information()}\nДля группы : {self.get_group()}\n\n{self.get_text_without_information()}'


alld= Scarecrow('1ИСИП-21-9').allgr()
issues = []
for i in alld:
  try:
    print('-----------------------------------------------------------')
    print(f"{Scarecrow(i).get_text()}\n\n")
    print('-----------------------------------------------------------')
    
  except Exception as e: issues.append([i,e])

print('Все окончено')

print('Ошибки : \n')
for d in issues:
  print(f'{d}\n')
def tl_indexes(lessons):
    words = [[s for s in lessons if 'Ино' in s], [s for s in lessons if 'Инж' in s]]
    indexes = []
    for word in words:
        if len(word) == 2:
            for w in list({*word}):
                indexes.append(lessons.index(w))
    return indexes

def all_tl_indexes(lessons):
    words = [[s for s in lessons if 'Ино' in s], [s for s in lessons if 'Инж' in s]]
    indexes = []
    for word in words:
        if len(word) == 1:
            for w in list({*word}):
                indexes.append(lessons.index(w))
    return indexes

def bad_cut(*catalogs):
    for catalog in catalogs:
        if len(catalog) in (1, 3, 5, 7, 9, 11, 13, 15):
            catalog.insert(0, '')

def initial_filtering(table, change: str):
    after_filtering = []

    for column in table:
        for ellement in column:
            if 'nan' in column:
                for _ in range(column.count('nan')):
                    nan_index = column.index('nan')
                    column[nan_index] = f'{change}'

            if ellement.endswith('.0'):
                column[column.index(ellement)] = ellement[:-2]

        after_filtering.append(column)

    return after_filtering

def after_restoration(old, design):
    old, design = list(old), list(design)
    for index, ellement in enumerate(design):
        if len(ellement) == 0:
            design[index] = '  '
        elif len(ellement) == 1:
            if ellement == '&':
                design[index] = f'{ellement}'
            else:
                design[index] = f'{ellement} '

    for row in old:
        if len(row) == len(design):
            for index, ellement in enumerate(row):
                temp_list = [s for s in design[index] if '&'.lower() in s.lower()]
                if temp_list:
                    left, right = design[index].split('&')
                    row[index] = f'{left}{ellement}{right}'
                else:
                    row[index] = f'{design[index][0]}{ellement}{design[index][1]}'
        old[old.index(row)] = row
    return old

def del_service_marks(catalog):
    catalog = list(catalog)
    catalog_edit = ','.join(catalog)
    catalog_edit = catalog_edit.replace('&', '')
    return catalog_edit.split(',')

def cleaner(comparator, catalog) -> int:
    for x, y in zip(comparator, catalog):
        if x == y:
            catalog[catalog.index(x)] = ' '
    return catalog

def text_size(list_subjects, font):
    font = font
    if isinstance(list_subjects, str):
        text = list_subjects
        length = (font.getbbox(text))[2]
        heigth = (size := font.getbbox(text))[1] + size[3]
    else:
        length = (font.getbbox(max(list_subjects, key=len)))[2]
        heigth = sum([(size := font.getbbox(item))[1] + size[3] for item in list_subjects])

    return length, heigth

def cut_date(datestr):
    if 'Untitled' in datestr:
        datestr = datestr.replace('Untitled', '')

    if 'Пара' in datestr:
        datestr = datestr.replace('Пара', '').strip()
    return datestr



from datetime import date
def day_of_week() -> int:
  return(date.today().isoweekday())


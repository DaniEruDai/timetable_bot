def groups(ellement):
    if ellement.isupper() and ellement.endswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
        return True

    elif ellement in ('ОПИр-22-9', 'ОПИр-21-9', 'ОПИр-20-9'):
        return True

    else:
        return False


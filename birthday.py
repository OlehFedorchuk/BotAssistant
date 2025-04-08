def validate_birthday(value):
    '''
    Birthday validation:
    - Use the format DD.MM.YYYY
    - Day, Month and Year must be correct
    '''
    parts = value.split('.')
    if len(parts) != 3:
        raise ValueError('Invalid date format. Use DD.MM.YYYY')
    day_str, month_str, year_str = parts
    if not (day_str.isdigit() and month_str.isdigit() and year_str.isdigit()):
        raise ValueError('Invalid date format. Use DD.MM.YYYY')
    day = int(day_str)
    month = int(month_str)
    year = int(year_str)
    if not (1 <= month <= 12):
        raise ValueError('Month must be between 1 and 12')
    if len(year_str) != 4:
        raise ValueError('Year must have 4 digits')
    if month == 2:
        max_day = 29 if (year % 4 == 0 and (
            year % 100 != 0 or year % 400 == 0)) else 28
    elif month in [4, 6, 9, 11]:
        max_day = 30
    else:
        max_day = 31
    if not (1 <= day <= max_day):
        raise ValueError(f'Day must be between 1 and {max_day}')
    return datetime(year, month, day).date()


class Birthday(Field):
    '''Class for sorting the Birthday'''

    def __init__(self, value):
        validated_date = validate_birthday(value)
        super().__init__(validated_date)

    def __str__(self):
        return self.value.strftime('%d.%m.%Y')


@exception_handler
def add_birthday_to_contact(book, name, birthday_str):
    '''
    Add or update Birthday
    '''
    record = book.find_record(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_birthday(birthday_str)
    return f'Birthday {birthday_str} added to contact {name}'


def show_birthday(book, name):
    record = book.find_record(name)
    if record and record.birthday:
        return f"{record.name.value}'s birthday is {record.birthday}"
    return 'Birthday is not set for this contact'


def upcoming_birthday(book):
    '''
    Returns list of contacts to send birthday wishes
    '''
    list_bday = book.get_upcoming_birthday()
    if not list_bday:
        return 'No upcoming birthday in the next week'
    today = datetime.now().date()
    lines = []
    for record in list_bday:
        bday_this_year = record.birthday.value.replace(year=today.year)
        if bday_this_year < today:
            bday_this_year = record.birthday.value.replace(year=today.year + 1)
        days_left = (bday_this_year - today).days
        lines.append(
            f'{record.name.value}:{record.birthday}(in {days_left} days)')
    return '\n'.join(lines)

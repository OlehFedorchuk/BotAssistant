from collections import UserDict
from datetime import datetime
import pickle

def validate_phone(value):
    """
    Phone number validation:
    - The number must consist of numbers only
    - The number length must be from 9 to 14 digits
    """
    if not value.isdigit() or not (9 <= len(value) <= 14):
        raise ValueError('The phone has to be 9 to 14 digits')
    return value

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

# -------------------------- Exception handler -----------------------------------------------
def exception_handler(func):
    """Decorator for catching exceptions and returning a friendly error message"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'Contact not found'
        except Exception as e:
            return f"{e}"
    return wrapper


class Field:
    """Clase class for the record fields"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Class for storing the name of contact"""

    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    """Class for sorting the phone"""

    def __init__(self, value):
        super().__init__(value)

class Birthday(Field):
    '''Class for sorting the Birthday'''

    def __init__(self, value):
        validated_date = validate_birthday(value)
        super().__init__(validated_date)

    def __str__(self):
        return self.value.strftime('%d.%m.%Y')

class Record:
    """Class for sorting the information about a contact, including name and phone list"""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

# -------------------------- Class methods -----------------------------------------------
    def add_phone(self, phone):
        # Validation after creating Phone object
        validated_phone = validate_phone(phone)
        self.phones.append(Phone(validated_phone))

    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)

    def remove_phone(self, phone):
        # !!!-- list comprehension
        self.phones = [k for k in self.phones if k.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for i, k in enumerate(self.phones):
            if k.value == old_phone:
                validated_phone = validate_phone(new_phone)
                self.phones[i] = Phone(validated_phone)
                return
        raise ValueError('Phone not found')

    def find_phone(self, phone):
        return next((k for k in self.phones if k.value == phone), None)

    def __str__(self):
        phone_str = ', '.join(str(k)
                              for k in self.phones) if self.phones else 'No phones'
        bday_str = f', Birthday: {self.birthday}' if self.birthday else ''
        return f'Contact name: {self.name}, phones: {phone_str} {bday_str}'

# ------- add_contact, change_contact, show_phone, search_contacts, show_all, delete_contact ------------------------
class AddressBook(UserDict):
    """Класс для управления записями контактов."""
    def add_record(self, record):
        self.data[record.name.value] = record
        
    def find_record(self, name):
        return self.data.get(name)
    
    def delete_record(self, name):
        if name in self.data:
            del self.data[name]
            
    def upcoming_birthday(self, days = 7):
        '''
        Returns a list of contacts with a birthday
        '''
        list_bday = []
        today = datetime.now().date()
        for record in self.data.values():
            if record.birthday:
                bday_this_year = record.birthday.value.replace(year = today.year)
                if bday_this_year < today:
                    bday_this_year = record.birthday.value.replace(year = today.year + 1)
                if 0 <= (bday_this_year - today).days <= days:
                    list_bday.append(record)
                    
        return list_bday
def __str__(self):
        if not self.data:
            return 'List is empty'
        return '\n'.join(str(record) for record in self.data.values())

@exception_handler
def add_contact(book, name, phone):
    record = book.find_record(name) or Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return f'Contact {name} with number {phone} has been added'


@exception_handler
def change_contact(book, name, old_phone, new_phone):
    record = book.find_record(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f'Contact {name} updated'
    raise KeyError  # 'Contact not found'


def show_phone(book, name):
    record = book.find_record(name)
    return str(record) if record else 'Contact was not found'


def search_contacts(book, query):
    results = [record for record in book.data.values(
    ) if query.lower() in record.name.value.lower()]
    if results:
        return "\n".join(str(record) for record in results)
    raise KeyError  # "Contact not found"


def show_all(book):
    return str(book) if book else 'The contact list is empty'


@exception_handler
def delete_contact(book, name):
    if book.find_record(name):
        book.delete_record(name)
        return f'Contact {name} was deleted'
    raise KeyError  # 'Contact not found'


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

def show_birthday (book, name):
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
        lines.append(f'{record.name.value}:{record.birthday}(in {days_left} days)')
    return '\n'.join(lines)

def save_data (book, filename='addressbook.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(book, f)
        
def load_datа (filename='addressbook.pkl'):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
def main():
    # book = AddressBook()
    book = load_datа()  # Download at the start

    print('Hi! I am a console assistant bot')
    while True:
        user_input = input(
            'Enter command(hello, add, change, phone, search, all, delete, add-birthday, show-birthday, birthdays exit), name, phone number: ')
        parts = user_input.strip().split()
        if not parts:
            continue
        command, *args = parts

        if command in ('exit', 'close'):
            save_data(book)  # saving data before going out
            print('Goodbye')
            break
        elif command == "hello":
            print("Hello! How can I help you?")
        elif command == 'add' and len(args) >= 2:
            print(add_contact(book, args[0], args[1]))
        elif command == 'change' and len(args) >= 3:
            print(change_contact(book, args[0], args[1], args[2]))
        elif command == 'phone' and len(args) >= 1:
            print(show_phone(book, args[0]))
        elif command == 'search' and len(args) >= 1:
            print(search_contacts(book, args[0]))
        elif command == 'all':
            print(show_all(book))
        elif command == 'delete' and len(args) >= 1:
            print(delete_contact(book, args[0]))
        elif command == 'add-birthday' and len(args) >= 2:
            print(add_birthday_to_contact(book, args[0], args[1]))
        elif command == 'show-birthday' and len(args) >= 1:
            print(show_birthday(book, args[0]))
        elif command == 'birthdays':
            print(upcoming_birthday(book))
        else:
            print('Unknown command or insufficient arguments. Please try again')


if __name__ == '__main__':
    main()

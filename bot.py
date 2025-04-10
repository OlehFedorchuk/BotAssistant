from collections import UserDict
from datetime import datetime
import pickle
import difflib

# -------------------------- Валідація даних -----------------------------------------------


def validate_phone(value):
    """
    Валідація номера телефону:
    - Номер повинен складатися тільки з цифр
    - Довжина номера повинна бути від 9 до 14 цифр
    """
    if not value.isdigit() or not (9 <= len(value) <= 14):
        raise ValueError('Номер телефону має містити від 9 до 14 цифр')
    return value


def validate_birthday(value):
    '''
    Валідація дати народження:
    - Використовуйте формат DD.MM.YYYY
    - День, Місяць та Рік мають бути коректними
    '''
    parts = value.split('.')
    if len(parts) != 3:
        raise ValueError('Невірний формат дати. Використовуйте DD.MM.YYYY')
    day_str, month_str, year_str = parts
    if not (day_str.isdigit() and month_str.isdigit() and year_str.isdigit()):
        raise ValueError('Невірний формат дати. Використовуйте DD.MM.YYYY')
    day = int(day_str)
    month = int(month_str)
    year = int(year_str)
    if not (1 <= month <= 12):
        raise ValueError('Місяць має бути від 1 до 12')
    if len(year_str) != 4:
        raise ValueError('Рік має складатися з 4 цифр')
    if month == 2:
        max_day = 29 if (year % 4 == 0 and (
            year % 100 != 0 or year % 400 == 0)) else 28
    elif month in [4, 6, 9, 11]:
        max_day = 30
    else:
        max_day = 31
    if not (1 <= day <= max_day):
        raise ValueError(f'День має бути від 1 до {max_day}')
    return datetime(year, month, day).date()

# -------------------------- Обробка виключень -----------------------------------------------


def exception_handler(func):
    """Декоратор для обробки виключень та повернення зрозумілого повідомлення про помилку"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'Контакт не знайдено'
        except Exception as e:
            return f"{e}"
    return wrapper

# -------------------------- Класи полів та запису -----------------------------------------------


class Field:
    """Базовий клас для полів запису"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Клас для збереження імені контакту"""

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

    def add_phone(self, phone):
        # Validation after creating Phone object
        validated_phone = validate_phone(phone)
        self.phones.append(Phone(validated_phone))

    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)

    def remove_phone(self, phone):
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

    def upcoming_birthday(self, days=7):
        '''
        Returns a list of contacts with a birthday
        '''
        list_bday = []
        today = datetime.now().date()
        for record in self.data.values():
            if record.birthday:
                bday_this_year = record.birthday.value.replace(year=today.year)
                if bday_this_year < today:
                    bday_this_year = record.birthday.value.replace(
                        year=today.year + 1)
                if 0 <= (bday_this_year - today).days <= days:
                    list_bday.append(record)
        return list_bday


def __str__(self):
    if not self.data:
        return 'List is empty'
    return '\n'.join(str(record) for record in self.data.values())

# -------------------------- Функції для роботи з контактами -----------------------------------------------


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
    return str(book) if book else 'Список контактів порожній'


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


def save_data(book, filename='addressbook.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(book, f)


def load_datа(filename='addressbook.pkl'):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

# -------------------------- Функція для визначення команди -----------------------------------------------


def guess_command(user_input, known_commands):
    """
    Using difflib.get_close_matches we search for the closest match of the entered command.
If a similar command is found, we return it, otherwise we return None.
    """
    # We get the first token as a potential team
    tokens = user_input.strip().split()
    if not tokens:
        return None, []
    input_cmd = tokens[0].lower()

    # If the entered command exactly matches one of the known ones, we return it
    if input_cmd in known_commands:
        return input_cmd, tokens[1:]

    # Using difflib to find the closest command
    close_matches = difflib.get_close_matches(
        input_cmd, known_commands, n=1, cutoff=0.6)
    if close_matches:
        return close_matches[0], tokens[1:]
    return None, tokens[1:]

# -------------------------- Основна функція -----------------------------------------------


def main():
    # Завантаження адресної книги з файлу (або створення нової)
    book = load_data()

    # Список доступних команд
    known_commands = [
        "hello", "add", "change", "phone", "search",
        "all", "delete", "add-birthday", "show-birthday",
        "birthdays", "exit", "close"
    ]

    print('Привіт! Я консольний помічник.')
    while True:
        user_input = input(
            'Введіть команду (наприклад, "hello", "add", "change", "phone", "search", "all", "delete", "add-birthday", "show-birthday", "birthdays", "exit"): ')
        if not user_input.strip():
            continue

        # Спроба визначити команду за допомогою помічника
        guessed_command, args = guess_command(user_input, known_commands)

        if guessed_command is None:
            print('Невідома команда. Будь ласка, спробуйте ще раз.')
            continue

        # Якщо введена команда не співпадає з тим, що ввів користувач, питаємо підтвердження
        tokens = user_input.strip().split()
        if tokens[0].lower() != guessed_command:
            response = input(
                f'Можливо, ви мали на увазі "{guessed_command}"? (y/n): ')
            if response.lower() != 'y':
                print('Команду не розпізнано. Будь ласка, спробуйте ще раз.')
                continue

        command = guessed_command

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

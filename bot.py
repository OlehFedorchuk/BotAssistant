from collections import UserDict
from datetime import datetime
import pickle
import re
import difflib
from colorama import init, Fore, Back, Style


# Ініціалізація Colorama
init(autoreset=True)


def display_commands_table():
    """Відображає список доступних команд у табличному вигляді"""
    commands = [
        ("Основні команди", [
            ("hello", "Привітання"),
            ("exit", "Вийти з програми"),
            ("close", "Закрити програму")
        ]),
        ("Робота з контактами", [
            ("add", "Додати контакт"),
            ("change", "Змінити контакт"),
            ("edit-name", "Редагувати ім'я"),
            ("delete", "Видалити контакт"),
            ("search", "Пошук"),
            ("all", "Показати всі контакти")
        ]),
        ("Робота з нотатками", [
            ("add-note", "Додати нотатку"),
            ("edit-note", "Редагувати нотатку"),
            ("remove-note", "Видалити нотатку"),
            ("show-note", "Показати нотатку")
        ]),
        ("Робота з днями народження", [
            ("add-birthday", "Додати день народження"),
            ("show-birthday", "Показати день народження"),
            ("birthdays", "Показати найближчі дні народження")
        ]),
        ("Робота з електронною поштою", [
            ("add-email", "Додати електронну пошту"),
            ("edit-email", "Редагувати електронну пошту"),
            ("remove-email", "Видалити електронну пошту")
        ])
    ]

    # Лямбда для форматування рядків
    def format_row(
        cmd, desc): return f"{Fore.GREEN}{cmd:<15}{Fore.WHITE}{desc}{Style.RESET_ALL}"

    # Вивід кожної категорії команд
    for category, cmds in commands:
        print(Back.LIGHTCYAN_EX + Fore.WHITE +
              f"{category}".center(50) + Style.RESET_ALL)
        print(Fore.CYAN + "." * 50 + Style.RESET_ALL)
        for cmd, desc in cmds:
            # Використання лямбда-функції для форматування
            print(format_row(cmd, desc))
        print(Fore.CYAN + "." * 50 + Style.RESET_ALL)
        print("\n")


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

    def __init__(self, name, email=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.note = ''
        self.email = Email(email) if email else None

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

    def set_email(self, email_str: str):
        self.email = Email(email_str)

    def edit_email(self, new_email_str: str):
        self.email = Email(new_email_str)

    def remove_email(self):
        self.email = None

    def edit_name(self, new_name):
        self.name = Name(new_name)

    def add_note(self, note):
        self.note = note

    def edit_note(self, note):
        self.note = note

    def remove_note(self):
        self.note = ''

    def show_note(self):
        return self.note

    def __str__(self):

        phone_str = ', '.join(str(k)
                              for k in self.phones) if self.phones else '📵  No phones'
        bday_str = f'🎂 Birthday: {self.birthday}' if self.birthday else ''
        note_str = f'📝 Note: {self.note}' if self.note else '📝 Note: Not set'
        phone_str = ', '.join(str(k)
                              for k in self.phones) if self.phones else '📵 No phones'
        bday_str = f'🎂 Birthday: {Style.RESET_ALL} {self.birthday}' if self.birthday else '🎂 Birthday: Not set'
        email_str = f'✉️  Email: {self.email.value}' if self.email else '✉️  Email: Not set'
        return (
            f"{Fore.CYAN}{'.' * 50}{Style.RESET_ALL}\n"
            f"👤{Fore.CYAN} Contact name:{Style.RESET_ALL} {self.name}\n"
            f"📞{Fore.CYAN} Phones:{Style.RESET_ALL} {phone_str}\n"
            f"{Fore.CYAN}{bday_str}\n"
            f"{Fore.CYAN}{email_str}{Style.RESET_ALL}\n"
            f"{Fore.CYAN}{note_str}{Style.RESET_ALL}\n"
            f"{Fore.CYAN}{'.' * 50}{Style.RESET_ALL}\n"
        )
# ------- add_contact, change_contact, show_phone, search_contacts, show_all, delete_contact ------------------------


class Email:
    def __init__(self, email: str):
        self.value = email

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, email: str):
        if self.validate_email(email):
            self._value = email
        else:
            raise Fore.RED + \
                ValueError(f"Невірний формат email: {email}") + Style.RESET_ALL

    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None


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

    def rename_record(self, old_name, new_name):
        if old_name in self.data:
            record = self.data.pop(old_name)
            record.edit_name(new_name)
            self.data[new_name] = record
        else:
            raise KeyError

    def __str__(self):
        if not self.data:
            return Fore.YELLOW + 'List is empty' + Style.RESET_ALL
        return '\n'.join(str(record) for record in self.data.values())


@exception_handler
def add_contact(book, name, phone):
    record = book.find_record(name) or Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return Fore.GREEN + f'Contact {name} with number {phone} has been added' + Style.RESET_ALL


@exception_handler
def change_contact(book, name, old_phone, new_phone):
    record = book.find_record(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return Fore.GREEN + f'Contact {name} updated' + Style.RESET_ALL
    raise KeyError  # 'Contact not found'


@exception_handler
def edit_name(book, old_name, new_name):
    book.rename_record(old_name, new_name)
    return Fore.GREEN + f'Name changed from {old_name} to {new_name}' + Style.RESET_ALL


@exception_handler
def add_note(book, name, note):
    record = book.find_record(name)
    if record:
        record.add_note(note)
        return Fore.GREEN + f'Note added to contact {name}' + Style.RESET_ALL
    raise KeyError


@exception_handler
def edit_note(book, name, note):
    record = book.find_record(name)
    if record:
        record.edit_note(note)
        return Fore.GREEN + f'Note added to contact {name}' + Style.RESET_ALL
    raise KeyError


@exception_handler
def remove_note(book, name):
    record = book.find_record(name)
    if record:
        record.remove_note()
        return Fore.GREEN + f'Note removed from contact {name}' + Style.RESET_ALL
    raise KeyError


def show_note(book, name):
    record = book.find_record(name)
    if record and record.note:
        return f'Note for {name}: {record.note}'
    return Fore.YELLOW + 'Note not found' + Style.RESET_ALL


def show_phone(book, name):
    record = book.find_record(name)
    return str(record) if record else Fore.YELLOW + 'Contact was not found' + Style.RESET_ALL


def search_contacts(book, query):
    results = [record for record in book.data.values(
    ) if query.lower() in record.name.value.lower()
        or any(query in phone.value for phone in record.phones)
        or (record.email and query.lower() in record.email.value.lower())]
    if results:
        return "\n".join(str(record) for record in results)
    raise KeyError  # "Contact not found"


def show_all(book):
    return str(book) if book else 'The contact list is empty'


@exception_handler
def delete_contact(book, name):
    if book.find_record(name):
        book.delete_record(name)
        return Fore.GREEN + f'Contact {name} was deleted' + Style.RESET_ALL
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
    return Fore.GREEN + f'Birthday {birthday_str} added to contact {name}' + Style.RESET_ALL


def show_birthday(book, name):
    record = book.find_record(name)
    if record and record.birthday:
        return f"{record.name.value}'s birthday is {record.birthday}"
    return 'Birthday is not set for this contact'


def upcoming_birthday(book):
    '''
    Returns list of contacts to send birthday wishes
    '''
    list_bday = book.upcoming_birthday()
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

# ============ Added functions of saving and personalization`` ==================================


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
    За допомогою difflib.get_close_matches шукаємо найближчу відповідність введеної команди.
    Якщо знайдено схожу команду, повертаємо її, інакше повертаємо None.
    """
    # Отримуємо перший токен як потенційну команду
    tokens = user_input.strip().split()
    if not tokens:
        return None, []
    input_cmd = tokens[0].lower()

    # Якщо введена команда точно збігається з однією з відомих, повертаємо її
    if input_cmd in known_commands:
        return input_cmd, tokens[1:]

    # Використовуємо difflib для пошуку найближчої команди
    close_matches = difflib.get_close_matches(
        input_cmd, known_commands, n=1, cutoff=0.6)
    if close_matches:
        return close_matches[0], tokens[1:]
    return None, tokens[1:]


def main():
    # book = AddressBook()
    book = load_datа()  # Download at the start

# Список доступних команд
    known_commands = [
        "hello", "add", "change", "phone", "search",
        "edit_name", "add-note", "edit-note", "remove-note",
        "all", "delete", "add-birthday", "show-birthday",
        "add-email", "edit-email", "remove-email",
        "birthdays", "show-note", "exit", "close"
    ]

    print(Fore.BLUE + 'Hi! I am a console assistant bot' + Style.RESET_ALL)
    print()
    display_commands_table()
    while True:

        user_input = input(Fore.CYAN + "Enter command:" + Style.RESET_ALL)
        print()

        if not user_input.strip():
            print(Fore.YELLOW + 'Empty input. Please try again.' + Style.RESET_ALL)
            continue

        # Спроба визначити команду за допомогою помічника
        guessed_command, args = guess_command(user_input, known_commands)

        if guessed_command is None:
            print(
                Fore.RED + 'Невідома команда. Будь ласка, спробуйте ще раз.' + Style.RESET_ALL)
            continue

        # Якщо введена команда не співпадає з тим, що ввів користувач, питаємо підтвердження
        tokens = user_input.strip().split()

        if tokens[0].lower() != guessed_command:
            response = input(
                Fore.YELLOW + f'Можливо, ви мали на увазі "{guessed_command}"? (y/n): ' + Style.RESET_ALL)

            if response.lower() != 'y':
                print(
                    Fore.RED + 'Команду не розпізнано. Будь ласка, спробуйте ще раз.' + Style.RESET_ALL)
                continue

        command = guessed_command

        if command in ('exit', 'close'):
            save_data(book)  # saving data before going out
            print('Goodbye')
            break
        elif command == "hello":
            print("Hello! How can I help you?" + Style.RESET_ALL)
        elif command == 'add' and len(args) >= 2:
            print(add_contact(book, args[0], args[1]))
        elif command == 'change' and len(args) >= 3:
            print(change_contact(book, args[0], args[1], args[2]))
        elif command == 'edit-name' and len(args) >= 2:
            print(edit_name(book, args[0], args[1]))
        elif command == 'add-note' and len(args) >= 2:
            print(add_note(book, args[0], ' '.join(args[1:])))
        elif command == 'edit-note' and len(args) >= 2:
            print(edit_note(book, args[0], ' '.join(args[1:])))
        elif command == 'remove-note' and len(args) >= 1:
            print(remove_note(book, args[0]))
        elif command == 'show-note' and len(args) >= 1:
            print(show_note(book, args[0]))
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
        elif command == 'add-email' and len(args) >= 2:
            record = book.find_record(args[0])
            if record:
                try:
                    record.set_email(args[1])
                    print(
                        Fore.GREEN + f"Email {args[1]} додано до контакту {args[0]}" + Style.RESET_ALL)
                except ValueError as e:
                    print(Fore.RED + f"Помилка: {e}" + Style.RESET_ALL)
            else:
                print(
                    Fore.RED + f"Контакт {args[0]} не знайдено" + Style.RESET_ALL)
        elif command == 'edit-email' and len(args) >= 2:
            record = book.find_record(args[0])
            if record:
                try:
                    record.edit_email(args[1])
                    print(
                        Fore.GREEN + f"Email {args[1]} оновлено для контакту {args[0]}" + Style.RESET_ALL)
                except ValueError as e:
                    print(Fore.RED + f"Помилка: {e}" + Style.RESET_ALL)
            else:
                print(
                    Fore.RED + f"Контакт {args[0]} не знайдено" + Style.RESET_ALL)
        elif command == 'remove-email' and len(args) >= 1:
            record = book.find_record(args[0])
            if record:
                record.remove_email()
                print(
                    Fore.GREEN + f"Email видалено для контакту {args[0]}" + Style.RESET_ALL)
            else:
                print(
                    Fore.RED + f"Контакт {args[0]} не знайдено" + Style.RESET_ALL)
        else:
            print(
                Fore.RED + 'Unknown command or insufficient arguments. Please try again' + Style.RESET_ALL)


if __name__ == '__main__':
    main()

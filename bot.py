from collections import UserDict
from datetime import datetime
import pickle
import re
import difflib
from colorama import init, Fore, Back, Style
from tabulate import tabulate

init(autoreset=True)

# Function to display a table of available commands


def display_commands_table():
    # Define the list of commands grouped by categories
    commands = [
        ("Main commands", [
            ("hello", "Greeting"),  # Greet the user
            ("exit", "Exit the program"),  # Exit the program
            ("close", "Close the program"),  # Close the program
        ]),
        ("Contact management", [
            ("add", "Add contact"),  # Add a new contact
            ("edit-name", "Edit a contact's name"),  # Edit a contact's name
            ("delete", "Delete a contact"),  # Delete a contact
            ("search", "Search for a contact"),  # Search for a contact
            ("all", "Show all contacts"),  # Display all contacts
        ]),
        ("Phone management", [
            ("phone", "Show a contact's phone"),  # Show a contact's phone
            ("edit-phone", "Edit a phone"),  # Edit a contact's phone number
            # Remove a contact's phone number
            ("remove-phone", "Remove a phone"),
        ]),
        ("Address management", [
            ("add-address", "Add address"),  # Add an address to a contact
            ("edit-address", "Edit address"),  # Edit a contact's address
            ("remove-address", "Remove address"),  # Remove a contact's address
        ]),
        ("Note management", [
            ("add-note", "Add a note"),  # Add a note to a contact
            ("edit-note", "Edit a note"),  # Edit a note
            ("remove-note", "Remove a note"),  # Remove a note
            ("show-note", "Show a note"),  # Display a note
        ]),
        ("Tag management", [
            ("add-tag", "Add a tag to a note"),  # Add a tag to a note
            ("remove-tag", "Remove a tag from a note"),  # Remove a tag from a note
            ("show-tags", "Show all tags of a note"),  # Show all tags of a note
            ("search-tag", "Search for contacts with a specific tag"),  # Search for contacts with a specific tag
            ("all-tags", "Show all unique tags"),  # Show all unique tags
        ]),
        ("Birthday management", [
            ("add-birthday", "Add a birthday"),  # Add a birthday to a contact
            ("show-birthday", "Show a birthday"),  # Show a contact's birthday
            ("birthdays", "Show upcoming birthdays"),  # Show upcoming birthdays
        ]),
        ("Email management", [
            ("add-email", "Add email"),  # Add an email to a contact
            ("edit-email", "Edit email"),  # Edit a contact's email
            ("remove-email", "Remove email"),  # Remove a contact's email
        ]),
        ("Tags management", [
            ("add-tag", "add-tag"),  # add a tag to a contact
            ("remove-tag", "remove-tag"),  # remove a tag from a contact
            ("show-tags", "show-tags"),  # show existing tags
            ("search-tag", "search-tag"),  # find a contact by tag
            ("sort-notes", "sort-notes")  # sorts notes by tags
        ])
    ]

    # Helper function to format rows for display
    def format_row(cmd, desc):
        return f"{Fore.GREEN}{cmd:<15}{Fore.WHITE}{desc}{Style.RESET_ALL}"

    # Print commands grouped by category
    for category, cmds in commands:
        print(Back.LIGHTCYAN_EX + Fore.WHITE +
              f"{category}".center(50) + Style.RESET_ALL)
        print(Fore.CYAN + "." * 50 + Style.RESET_ALL)
        for cmd, desc in cmds:
            print(format_row(cmd, desc))
        print(Fore.CYAN + "." * 50 + Style.RESET_ALL)
        print("\n")

# Function to display a table of contacts
def format_all_contacts_as_table(book):
    """
    Formats all contacts in the address book as a table.
    """
    if not book.data:
        return Fore.YELLOW + "The contact list is empty." + Style.RESET_ALL

    headers = [
        Fore.CYAN + "Name" + Style.RESET_ALL,
        Fore.CYAN + "Phones" + Style.RESET_ALL,
        Fore.CYAN + "Birthday" + Style.RESET_ALL,
        Fore.CYAN + "Email" + Style.RESET_ALL,
        Fore.CYAN + "Note" + Style.RESET_ALL,
        Fore.CYAN + "Address" + Style.RESET_ALL
    ]
    data = []
    for record in book.data.values():
        data.append([
            Fore.CYAN + record.name.value + Style.RESET_ALL,
            Fore.CYAN + ', '.join(phone.value for phone in record.phones) + Style.RESET_ALL if record.phones else Fore.YELLOW + "No phones" + Style.RESET_ALL,
            Fore.CYAN + str(record.birthday) + Style.RESET_ALL if record.birthday else Fore.YELLOW + "Not set" + Style.RESET_ALL,
            Fore.CYAN + record.email.value + Style.RESET_ALL if record.email else Fore.YELLOW + "Not set" + Style.RESET_ALL,
            Fore.CYAN + record.note + Style.RESET_ALL if record.note else Fore.YELLOW + "Not set" + Style.RESET_ALL,
            Fore.CYAN + record.address + Style.RESET_ALL if record.address else Fore.YELLOW + "Not set" + Style.RESET_ALL
        ])
    return tabulate(data, headers, tablefmt="grid")

def format_contact_as_table(contact):
    """
    Formats a single contact as a table with colors.
    """
    headers = [Fore.CYAN + "Field" + Style.RESET_ALL, Fore.CYAN + "Value" + Style.RESET_ALL]
    data = [
        [Fore.GREEN + "Name" + Style.RESET_ALL, Fore.CYAN + contact.name.value + Style.RESET_ALL],
        [Fore.GREEN + "Phones" + Style.RESET_ALL, Fore.CYAN + ', '.join(phone.value for phone in contact.phones) + Style.RESET_ALL if contact.phones else Fore.YELLOW + "No phones" + Style.RESET_ALL],
        [Fore.GREEN + "Birthday" + Style.RESET_ALL, Fore.CYAN + str(contact.birthday) + Style.RESET_ALL if contact.birthday else Fore.YELLOW + "Not set" + Style.RESET_ALL],
        [Fore.GREEN + "Email" + Style.RESET_ALL, Fore.CYAN + contact.email.value + Style.RESET_ALL if contact.email else Fore.YELLOW + "Not set" + Style.RESET_ALL],
        [Fore.GREEN + "Note" + Style.RESET_ALL, Fore.CYAN + contact.note + Style.RESET_ALL if contact.note else Fore.YELLOW + "Not set" + Style.RESET_ALL],
        [Fore.GREEN + "Address" + Style.RESET_ALL, Fore.CYAN + contact.address + Style.RESET_ALL if contact.address else Fore.YELLOW + "Not set" + Style.RESET_ALL]
    ]
    return tabulate(data, headers, tablefmt="grid")

def guess_command(user_input, know_commands):
    '''
    Розширенний автопідбір: повертає список можливих команд, що містять введений текст
    або схожі на нього
    '''
    tokens = user_input.strip().split()
    if not tokens:
        return None, []

    input_cmd = tokens[0].lower()
    args = tokens[1:]

    if input_cmd in know_commands:
        return input_cmd, args

    contains_matches = [cmd for cmd in know_commands if input_cmd in cmd]

    unclear_matches = difflib.get_close_matches(input_cmd, know_commands, n=len(know_commands),
                                                cutoff=0.5)

    all_matches = list(dict.fromkeys(contains_matches + unclear_matches))

    if all_matches:
        return all_matches, args

    return None, args


# Function to validate phone numbers

def validate_phone(value):
    # Ensure the phone number is numeric and has a valid length
    if not value.isdigit() or not (9 <= len(value) <= 14):
        raise ValueError('The phone has to be 9 to 14 digits')
    return value


# Function to validate birthday dates
def validate_birthday(value):
    # Split the date into day, month, and year
    parts = value.split('.')
    if len(parts) != 3:
        raise ValueError('Invalid date format. Use DD.MM.YYYY')
    day_str, month_str, year_str = parts
    if not (day_str.isdigit() and month_str.isdigit() and year_str.isdigit()):
        raise ValueError('Invalid date format. Use DD.MM.YYYY')
    day = int(day_str)
    month = int(month_str)
    year = int(year_str)
    # Validate month and year
    if not (1 <= month <= 12):
        raise ValueError('Month must be between 1 and 12')
    if len(year_str) != 4:
        raise ValueError('Year must have 4 digits')
    # Determine the maximum number of days in the given month
    if month == 2:
        max_day = 29 if (year % 4 == 0 and (
            year % 100 != 0 or year % 400 == 0)) else 28
    elif month in [4, 6, 9, 11]:
        max_day = 30
    else:
        max_day = 31
    # Validate the day
    if not (1 <= day <= max_day):
        raise ValueError(f'Day must be between 1 and {max_day}')
    return datetime(year, month, day).date()


# Decorator to handle exceptions in functions
def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'Contact not found'
        except Exception as e:
            return f"{e}"
    return wrapper


# Base class for fields like Name, Phone, Birthday, etc.
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


# Class for contact names
class Name(Field):
    def __init__(self, value):
        super().__init__(value)


# Class for phone numbers
class Phone(Field):
    def __init__(self, value):
        super().__init__(value)


# Class for birthdays
class Birthday(Field):
    def __init__(self, value):
        # Validate and store the birthday date
        validated_date = validate_birthday(value)
        super().__init__(validated_date)

    def __str__(self):
        # Format the birthday for display
        return self.value.strftime('%d.%m.%Y')


class Tag(Field):
    def __init__(self, value):
        super().__init__(value)


class Record:
    """
    Represents a single contact record in the address book.
    Contains fields such as name, phones, birthday, email, notes, and address.
    """

    def __init__(self, name, email=None, address=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.note = ''
        self.tags = set()
        self.email = Email(email) if email else None
        self.address = address

    def set_address(self, address):
        """Sets the address for the contact."""
        self.address = address

    def edit_address(self, new_address):
        """Edits the address of the contact."""
        self.address = new_address

    def remove_address(self):
        """Removes the address from the contact."""
        self.address = None

    def add_phone(self, phone):
        """Adds a phone number to the contact."""
        validated_phone = validate_phone(phone)
        self.phones.append(Phone(validated_phone))

    def add_birthday(self, birthday_str):
        """Adds a birthday to the contact."""
        self.birthday = Birthday(birthday_str)

    def remove_phone(self, phone):
        """
        Removes a phone number from the contact.
        Raises an error if the phone number is not found.
        """
        for i, k in enumerate(self.phones):
            if k.value == phone:
                del self.phones[i]
                return
        raise ValueError(f"Phone number {phone} not found.")

    def edit_phone(self, old_phone, new_phone):
        """Edits an existing phone number."""
        for i, k in enumerate(self.phones):
            if k.value == old_phone:
                validated_phone = validate_phone(new_phone)
                self.phones[i] = Phone(validated_phone)
                return
        raise ValueError('Phone not found')

    def find_phone(self, phone):
        """Finds a phone number in the contact."""
        return next((k for k in self.phones if k.value == phone), None)

    def set_email(self, email_str: str):
        """Sets an email address for the contact."""
        self.email = Email(email_str)

    def edit_email(self, new_email_str: str):
        """Edits the email address of the contact."""
        self.email = Email(new_email_str)

    def remove_email(self):
        """Removes the email address from the contact."""
        if self.email is None:
            raise ValueError('Email is alredy removed or not set')
        self.email = None

    def edit_name(self, new_name):
        """Edits the name of the contact."""
        self.name = Name(new_name)

    def add_note(self, note):
        """Adds a note to the contact."""
        self.note = note

    def edit_note(self, note):
        """Edits the note of the contact."""
        self.note = note

    def remove_note(self):
        """Removes the note from the contact."""
        self.note = ''

    def show_note(self):
        """Returns the note of the contact."""
        return self.note

    def add_tag(self, tag):
        """Adds a tag to the note"""
        self.tags.add(Tag(tag))

    def remove_tag(self, tag):
        """Removes a tag from the note"""
        self.tags = {t for t in self.tags if t.value != tag}

    def get_tags(self):
        """Returns a list of note tags"""
        return [tag.value for tag in self.tags]

    def has_tag(self, tag):
        """Checks if the note has a specific tag"""
        return any(t.value == tag for t in self.tags)

    def __str__(self):
        """
        Returns a string representation of the contact,
        including name, phones, birthday, email, notes, tags, and address.
        """
        phone_str = ', '.join(str(k)
                              for k in self.phones) if self.phones else '📵 No phones'
        bday_str = f'🎂 Birthday:{Style.RESET_ALL}{self.birthday}' if self.birthday else '🎂 Birthday: Not set'
        note_str = f'📝 Note: {Style.RESET_ALL}{self.note}' if self.note else '📝 Note: Not set'
        email_str = f'✉️  Email:{Style.RESET_ALL}{self.email.value}' if self.email else '✉️  Email: Not set'
        address_str = f'🏠 Address: {Style.RESET_ALL}{self.address}' if self.address else '🏠 Address: Not set'
        tags_str = f'🏷️ Tags: {Style.RESET_ALL}{", ".join(self.get_tags())}' if self.tags else '🏷️ Tags: No tags'
        return (
            f"{Fore.CYAN}{'.' * 50}{Style.RESET_ALL}\n"
            f"👤{Fore.CYAN} Contact name:{Style.RESET_ALL} {self.name} \n"
            f"📞{Fore.CYAN} Phones:{Style.RESET_ALL} {phone_str}\n"
            f"{Fore.CYAN}{bday_str}{Style.RESET_ALL}\n"
            f"{Fore.CYAN}{email_str}{Style.RESET_ALL}\n"
            f"{Fore.CYAN}{note_str}{Style.RESET_ALL}\n"
            f"{Fore.CYAN}{tags_str}{Style.RESET_ALL}\n"
            f"{Fore.CYAN}{address_str}{Style.RESET_ALL}\n"
            f"{Fore.CYAN}{tags_str}{Style.RESET_ALL}\n"
            f"{Fore.CYAN}{'.' * 50}{Style.RESET_ALL}\n"
        )


class Email:
    """
    Represents an email address for a contact.
    Validates the email format before storing it.
    """

    def __init__(self, email: str):
        self.value = email  # Initialize the email value

    @property
    def value(self):
        """Getter for the email value."""
        return self._value

    @value.setter
    def value(self, email: str):
        """Setter for the email value with validation."""
        if self.validate_email(email):
            self._value = email
        else:
            raise ValueError(f"Invalid email format: {email}")

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validates the email format using a regular expression.
        Returns True if the email is valid, otherwise False.
        """
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None


class AddressBook(UserDict):
    """
    Represents the address book, which is a collection of contact records.
    Inherits from UserDict to provide dictionary-like behavior.
    """

    def add_record(self, record):
        """Adds a new contact record to the address book."""
        self.data[record.name.value] = record

    def find_record(self, name):
        """Finds a contact record by name."""
        return self.data.get(name)

    def delete_record(self, name):
        """Deletes a contact record by name."""
        if name in self.data:
            del self.data[name]

    def search_by_tag(self, tag):
        """Поиск контактов по тегу"""
        results = []
        for record in self.data.values():
            if record.has_tag(tag):
                results.append(record)
        return results

    def get_all_tags(self):
        """Получение всех уникальных тегов"""
        all_tags = set()
        for record in self.data.values():
            all_tags.update(record.get_tags())
        return sorted(all_tags)

    def get_contacts_by_tags(self, tags):
        """Получение контактов, имеющих все указанные теги"""
        results = []
        for record in self.data.values():
            if all(record.has_tag(tag) for tag in tags):
                results.append(record)
        return results

    def upcoming_birthday(self, days=7):
        """
        Finds contacts with upcoming birthdays within the specified number of days.
        Returns a list of records with upcoming birthdays.
        """
        list_bday = []
        today = datetime.now().date()
        for record in self.data.values():
            if record.birthday:
                # Calculate the birthday for the current year
                bday_this_year = record.birthday.value.replace(year=today.year)
                if bday_this_year < today:
                    # If the birthday has already passed this year, calculate for the next year
                    bday_this_year = record.birthday.value.replace(
                        year=today.year + 1)
                # Check if the birthday is within the specified range
                if 0 <= (bday_this_year - today).days <= days:
                    list_bday.append(record)

        return list_bday

    def rename_record(self, old_name, new_name):
        """
        Renames a contact record by changing its name.
        Moves the record to the new name in the address book.
        """
        if old_name in self.data:
            record = self.data.pop(old_name)
            record.edit_name(new_name)
            self.data[new_name] = record
        else:
            raise KeyError

    def __str__(self):
        """
        Returns a string representation of all contacts in the address book.
        If the address book is empty, returns a message indicating that.
        """
        if not self.data:
            return Fore.YELLOW + 'List is empty' + Style.RESET_ALL
        return '\n'.join(str(record) for record in self.data.values())


@exception_handler
def add_address(book, name, address):
    """
    Adds an address to an existing contact.
    Raises an error if the contact is not found.
    """
    record = book.find_record(name)
    if record:
        record.set_address(address)
        return Fore.GREEN + f'Address added to contact {name}' + Style.RESET_ALL
    raise KeyError


@exception_handler
def edit_address(book, name, new_address):
    """
    Edits the address of an existing contact.
    Raises an error if the contact is not found.
    """
    record = book.find_record(name)
    if record:
        record.edit_address(new_address)
        return Fore.GREEN + f'Address updated for contact {name}' + Style.RESET_ALL
    raise KeyError


@exception_handler
def remove_address(book, name):
    """
    Removes the address from an existing contact.
    Raises an error if the contact is not found.
    """
    record = book.find_record(name)
    if record:
        record.remove_address()
        return Fore.GREEN + f'Address removed from contact {name}' + Style.RESET_ALL
    raise KeyError


@exception_handler
def remove_phone(book, name, phone):
    """
    Removes a phone number from an existing contact.
    Raises an error if the contact or phone number is not found.
    """
    record = book.find_record(name)
    if record:
        record.remove_phone(phone)
        return Fore.GREEN + f"Phone number {phone} removed from contact {name}" + Style.RESET_ALL
    raise KeyError("Contact not found")


@exception_handler
def add_contact(book, name, phone):
    """
    Adds a new contact to the address book.
    If the contact already exists, adds the phone number to the existing contact.
    """
    record = book.find_record(name) or Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return Fore.GREEN + f'Contact {name} with number {phone} has been added' + Style.RESET_ALL


@exception_handler
def change_contact(book, name, old_phone, new_phone):
    """
    Changes an existing phone number for a contact.
    Raises an error if the contact or phone number is not found.
    """
    record = book.find_record(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return Fore.GREEN + f'Contact {name} updated' + Style.RESET_ALL
    raise KeyError  # 'Contact not found'


@exception_handler
def edit_name(book, old_name, new_name):
    """
    Edits the name of an existing contact.
    Moves the contact record to the new name in the address book.
    """
    book.rename_record(old_name, new_name)
    return Fore.GREEN + f'Name changed from {old_name} to {new_name}' + Style.RESET_ALL


@exception_handler
def add_note(book, name, note):
    """
    Adds a note to an existing contact.
    Raises an error if the contact is not found.
    """
    record = book.find_record(name)
    if record:
        record.add_note(note)
        return Fore.GREEN + f'Note added to contact {name}' + Style.RESET_ALL
    raise KeyError


@exception_handler
def edit_note(book, name, note):
    """
    Edits the note of an existing contact.
    Raises an error if the contact is not found.
    """
    record = book.find_record(name)
    if record:
        record.edit_note(note)
        return Fore.GREEN + f'Note updated for contact {name}' + Style.RESET_ALL
    raise KeyError


@exception_handler
def remove_note(book, name):
    """
    Removes the note from an existing contact.
    Raises an error if the contact is not found.
    """
    record = book.find_record(name)
    if record:
        record.remove_note()
        return Fore.GREEN + f'Note removed from contact {name}' + Style.RESET_ALL
    raise KeyError


def show_note(book, name):
    """
    Displays the note of a specific contact.
    Returns a message if the note is not found.
    """
    record = book.find_record(name)
    if record and record.note:
        return f'Note for {name}: {record.note}'
    return Fore.YELLOW + 'Note not found' + Style.RESET_ALL


def show_phone(book, name):
    """
    Displays the phone numbers of a specific contact.
    Returns a message if the contact or phone numbers are not found.
    """
    record = book.find_record(name)
    if record:
        if record.phones:
            return ', '.join(phone.value for phone in record.phones)
        return Fore.YELLOW + 'No phone numbers found for this contact' + Style.RESET_ALL
    return Fore.YELLOW + 'Contact was not found' + Style.RESET_ALL


def search_contacts(book, query):
    """
    Searches for contacts in the address book by name, phone number, email, or notes.
    Returns a list of matching contacts or raises an error if no matches are found.
    """
    query_lower = query.lower()
    results = []

    for record in book.data.values():
        name_match = query_lower in record.name.value.lower()
        phone_match = any(query_lower in str(phone.value).lower()
                          for phone in record.phones)
        email_match = record.email and query_lower in record.email.value.lower()
        note_match = query_lower in record.note.lower() if record.note else False

        if name_match or phone_match or email_match or note_match:
            results.append(str(record))

    if results:
        return "\n".join(results)

    raise KeyError("Contact not found")


def show_all(book):
    """
    Displays all contacts in the address book.
    Returns a message if the address book is empty.
    """
    return str(book) if book else 'The contact list is empty'


@exception_handler
def delete_contact(book, name):
    """
    Deletes a contact from the address book by name.
    Raises an error if the contact is not found.
    """
    if book.find_record(name):
        book.delete_record(name)
        return Fore.GREEN + f'Contact {name} was deleted' + Style.RESET_ALL
    raise KeyError  # 'Contact not found'


@exception_handler
def add_birthday_to_contact(book, name, birthday_str):
    """
    Adds a birthday to a specific contact.
    Creates a new contact if the contact does not already exist.
    """
    record = book.find_record(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_birthday(birthday_str)
    return Fore.GREEN + f'Birthday {birthday_str} added to contact {name}' + Style.RESET_ALL


@exception_handler
def remove_email(book, name):
    """
    Removes the email address from an existing contact.
    Raises an error if the contact is not found or the email is already removed.
    """
    record = book.find_record(name)
    if record:
        try:
            record.remove_email()
            return Fore.GREEN + f"Email removed for contact {name}" + Style.RESET_ALL
        except ValueError as e:
            return Fore.YELLOW + f"Warning: {e}" + Style.RESET_ALL
    raise KeyError("Contact not found")


def show_birthday(book, name):
    """
    Displays the birthday of a specific contact.
    Returns a message if the birthday is not set.
    """
    record = book.find_record(name)
    if record and record.birthday:
        return f"{record.name.value}'s birthday is {record.birthday}"
    return 'Birthday is not set for this contact'


def upcoming_birthday(book):
    """
    Displays a list of contacts with upcoming birthdays within the next 7 days.
    Returns a message if no upcoming birthdays are found.
    """
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
            f'{record.name.value}: {record.birthday} (in {days_left} days)')
    return '\n'.join(lines)


def search_notes(book, query):
    '''
    search for contacts with tags
    '''
    results = []
    for record in book.data.values():
        note_text = record.note.lower()
        tag_list = [t.lower() for t in record.tags]
        if query.lower() in note_text or query.lower() in ' '.join(tag_list):
            results.append(record)

    if results:
        return '\n'.join(str(r) for r in results)
    return Fore.YELLOW + 'No tags found matching your query' + Style.RESET_ALL


@exception_handler
def add_tags(book, name, *tags):
    '''
    Adding tags to contact list, tags are not duplicated
    '''
    record = book.find_record(name)
    if not record:
        raise KeyError
    for tag in tags:
        record.add_tag(tag)
    return Fore.GREEN + f"Tags added to {name}: {', '.join(tags)}" + Style.RESET_ALL


@exception_handler
def remove_tags(book, name, tag):
    '''
    Deleting tegs from contacts list, if there are any tegs
    '''
    record = book.find_record(name)
    if not record:
        raise KeyError
    if tag.lower() not in record.tags:
        return Fore.YELLOW + f"Tag '{tag}' not found for {name}" + Style.RESET_ALL
    record.remove_tag(tag)
    return Fore.GREEN + f"Tag '{tag}' removed form {name}" + Style.RESET_ALL


@exception_handler
def show_tags(book, name):
    record = book.find_record(name)
    if not record:
        raise KeyError
    return f"Tags for {name}: {record.show_tags()}"


@exception_handler
def search_by_tag(book, tag):
    tag = tag.lower()
    result = [r for r in book.data.values() if tag in r.tags]
    if result:
        return "\n".join(str(r) for r in result)
    return Fore.YELLOW + f"No contacts found with tag '{tag}'"


def sort_notes_by_tags(book):
    '''
    Sorts notes by tags, displaying a list of contacts grouped by tegs
    '''
    tag_dict = {}
    for record in book.data.values():
        for tag in record.tags:
            tag_dict.setdefault(tag, []).append(record)

    if not tag_dict:
        return Fore.YELLOW + "No tags found in the notebook" + Style.RESET_ALL

    output = []
    for tag in sorted(tag_dict):
        output.append(Fore.BLUE + f"\nTag: #{tag}" + Style.RESET_ALL)
        for record in tag_dict[tag]:
            note = record.note if record else "No note"
            output.append(f"- {record.name.value}: {note}")
    return '\n'.join(output)
# ============ Added functions of saving and personalization`` ==================================


def save_data(book, filename='addressbook.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(book, f)


def load_data(filename='addressbook.pkl'):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def guess_command(user_input, known_commands, threshold=0.8):
    """
    Returns the most similar command and list of arguments.
    If similarity ≥ threshold, the command is applied automatically.
    """
    tokens = user_input.strip().split()
    if not tokens:
        return None, [], False  # Handle empty input gracefully

    input_cmd = tokens[0].lower()
    args = tokens[1:]

    # Exact match
    if input_cmd in known_commands:
        return input_cmd, args, True

    # Fuzzy matching for similar commands
    matches = []
    for cmd in known_commands:
        ratio = difflib.SequenceMatcher(None, input_cmd, cmd).ratio()
        if ratio >= threshold:
            matches.append((cmd, ratio))

    # Sort matches by similarity (highest first)
    matches.sort(key=lambda x: x[1], reverse=True)

    if matches:
        # If there's only one confident match and it's above a stricter threshold
        if len(matches) == 1 and matches[0][1] >= 0.9:
            return matches[0][0], args, True
        # Otherwise, return the top matches for user confirmation
        return [match[0] for match in matches], args, False

    # No matches found
    return None, args, False

@exception_handler
def add_tag(book, name, tag):
    """Добавляет тег к заметке контакта"""
    record = book.find_record(name)
    if record:
        record.add_tag(tag)
        return Fore.GREEN + f'Тег "{tag}" добавлен к заметке контакта {name}' + Style.RESET_ALL
    raise KeyError

@exception_handler
def remove_tag(book, name, tag):
    """Удаляет тег из заметки контакта"""
    record = book.find_record(name)
    if record:
        record.remove_tag(tag)
        return Fore.GREEN + f'Тег "{tag}" удален из заметки контакта {name}' + Style.RESET_ALL
    raise KeyError

def show_tags(book, name):
    """Показывает все теги заметки контакта"""
    record = book.find_record(name)
    if record:
        tags = record.get_tags()
        if tags:
            return f'Tags of contact {name}\'s note: {", ".join(tags)}'
        return Fore.YELLOW + 'Note has no tags' + Style.RESET_ALL
    return Fore.YELLOW + 'Contact not found' + Style.RESET_ALL

def search_by_tag(book, tag):
    """Search for contacts by tag"""
    results = book.search_by_tag(tag)
    if results:
        return "\n".join(str(record) for record in results)
    return Fore.YELLOW + f'Contacts with tag "{tag}" not found' + Style.RESET_ALL

def show_all_tags(book):
    """Shows all unique tags"""
    tags = book.get_all_tags()
    if tags:
        return f'All tags: {", ".join(tags)}'
    return Fore.YELLOW + 'Tags not found' + Style.RESET_ALL

def main():
    # book = AddressBook()
    book = load_data()  # Download at the start

    # List of known commands supported by the bot
    known_commands = [
        "hello",
        "add", "search",
        "edit-name", 
        "add-note", "edit-note", "remove-note","show-note",
        "add-tag", "remove-tag", "show-tags", "search-tag", "all-tags",
        "all", 
        "delete", 
        "add-birthday", "show-birthday",
        "add-email", "edit-email", "remove-email",
        "add-address", "edit-address", "remove-address",
        "birthdays",
        "edit-phone", "remove-phone",
        "phone",
        "exit", "close"
    ]

    # Display a welcome message and the list of available commands
    print(Fore.BLUE + 'Hi! I am a console assistant bot' + Style.RESET_ALL)
    print()
    display_commands_table()

    suggestion_dict = {}
    pending_command = None
    last_arg = []

    # Main loop to process user commands
    while True:
        # Prompt the user for a command
        user_input = input(Fore.CYAN + "Enter command:" + Style.RESET_ALL)
        print()

        if not user_input.strip():
            # Handle empty input
            print(Fore.YELLOW + 'Empty input. Please try again.' + Style.RESET_ALL)
            continue
        # === Step 1 =====
        if pending_command:
            args = user_input.strip().split()
            command = pending_command
            pending_command = None
            print(Fore.MAGENTA + f"[DEBAG] Обрано команду: {command}")
            print(f"[DEBAG] Аргумент (args): {args}" + Style.RESET_ALL)

        # === Step 2 ======
        elif suggestion_dict:
            parts = user_input.strip().split()
            if parts and parts[0].isdigit():
                selection = int(parts[0])
                if selection in suggestion_dict:
                    command = suggestion_dict[selection]
                    args = parts[1:] if len(parts) > 1 else last_arg
                    suggestion_dict = {}
                    pending_command = command
                    print(Fore.MAGENTA + f'[DEBUG] Обрано команду: {pending_command}' +
                          Style.RESET_ALL)
                    print(Fore.CYAN +
                          f"Введіть аргументи для команди '{pending_command}':")
                else:
                    print(Fore.RED + "Incorrect number" + Style.RESET_ALL)
                    continue
            else:
                print(
                    Fore.RED + "Please enter a valid selection number" + Style.RESET_ALL)

        # Check for exact match with "exit" or "close"
        if user_input.lower() in ('exit', 'close'):
            save_data(book)  # Save the address book data before exiting
            print('Goodbye')
            break

        # Guess the command and extract arguments
        guess_result, args, is_confident = guess_command(user_input, known_commands)

        if guess_result is None:
            print(Fore.RED + 'Unknown command. Please try again.' + Style.RESET_ALL)
            continue

        if isinstance(guess_result, list):
            # If multiple suggestions are returned
            print(Fore.YELLOW + "Did you mean one of these commands?")
            for i, cmd in enumerate(guess_result, 1):
                print(f"{i}. {cmd}")
            choice = input(Fore.CYAN + "Enter the number of the correct command, or press Enter to cancel: " + Style.RESET_ALL)
            if choice.isdigit() and 1 <= int(choice) <= len(guess_result):
                guessed_command = guess_result[int(choice) - 1]
            else:
                print(Fore.RED + "Command selection canceled. Please try again." + Style.RESET_ALL)
                continue
        elif not is_confident:
            # If the match is not confident, ask for confirmation
            response = input(Fore.YELLOW + f'Maybe you meant "{guess_result}"? (y/n): ' + Style.RESET_ALL)
            if response.lower() != 'y':
                print(Fore.RED + "Command canceled. Please try again." + Style.RESET_ALL)
                continue
        else:
            guessed_command = guess_result
            
        command = guessed_command
        # Handle the "exit" and "close" commands to terminate the program
        if command in ('exit', 'close'):
            save_data(book)  # Save the address book data before exiting
            print('Goodbye')
            break

        # Process other commands
        elif command == "hello":
            print("Hello! How can I help you?" + Style.RESET_ALL)
        elif command == 'add' and len(args) >= 2:
            print(add_contact(book, args[0], args[1]))
        elif command == 'edit-phone' and len(args) >= 3:
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
            print(format_all_contacts_as_table(book))
        elif command == 'delete' and len(args) >= 1:
            print(delete_contact(book, args[0]))
        elif command == 'add-birthday' and len(args) >= 2:
            print(add_birthday_to_contact(book, args[0], args[1]))
        elif command == 'show-birthday' and len(args) >= 1:
            print(show_birthday(book, args[0]))
        elif command == 'birthdays':
            print(upcoming_birthday(book))
        elif command == 'remove-phone' and len(args) >= 2:
            print(remove_phone(book, args[0], args[1]))
        elif command == 'add-tag' and len(args) >= 2:
            print(add_tags(book, args[0], *args[1:]))
        elif command == 'remove-tag' and len(args) >= 2:
            print(remove_tags(book, args[0], args[1]))
        elif command == 'show-tags' and len(args) >= 1:
            print(show_tags(book, args[0]))
        elif command == 'search-tag' and len(args) >= 1:
            print(search_by_tag(book, args[0]))
        elif command == 'sort-notes':
            print(sort_notes_by_tags(book))
        elif command == 'add-email' and len(args) >= 2:
            record = book.find_record(args[0])
            if record:
                try:
                    record.set_email(args[1])
                    print(
                        Fore.GREEN + f"Email {args[1]} added to contact {args[0]}" + Style.RESET_ALL)
                except ValueError as e:
                    print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
            else:
                print(
                    Fore.RED + f"Contact {args[0]} not found" + Style.RESET_ALL)
        elif command == 'edit-email' and len(args) >= 2:
            record = book.find_record(args[0])
            if record:
                try:
                    record.edit_email(args[1])
                    print(
                        Fore.GREEN + f"Email {args[1]} updated for contact {args[0]}" + Style.RESET_ALL)
                except ValueError as e:
                    print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
            else:
                print(
                    Fore.RED + f"Contact {args[0]} not found" + Style.RESET_ALL)
        elif command == 'remove-email' and len(args) >= 1:
            print(remove_email(book, args[0]))

        elif command == 'add-address' and len(args) >= 2:
            print(add_address(book, args[0], ' '.join(args[1:])))
        elif command == 'edit-address' and len(args) >= 2:
            print(edit_address(book, args[0], ' '.join(args[1:])))
        elif command == 'remove-address' and len(args) >= 1:
            print(remove_address(book, args[0]))
        elif command == 'add-tag' and len(args) >= 2:
            print(add_tag(book, args[0], args[1]))
        elif command == 'remove-tag' and len(args[0]) >= 2:
            print(remove_tag(book, args[0], args[1]))
        elif command == 'show-tags' and len(args) >= 1:
            print(show_tags(book, args[0]))
        elif command == 'search-tag' and len(args) >= 1:
            print(search_by_tag(book, args[0]))
        elif command == 'all-tags':
            print(show_all_tags(book))
        else:
            print(
                Fore.RED + 'Unknown command or insufficient arguments. Please try again' + Style.RESET_ALL)


if __name__ == '__main__':
    main()

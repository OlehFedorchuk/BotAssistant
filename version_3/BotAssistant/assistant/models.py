import re
from collections import UserDict
from datetime import datetime
from assistant.validator import validate_phone, validate_birthday, validate_email
from colorama import init, Fore, Back, Style

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
        self.email = Email(email) if email else None
        self.tags = set()
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

    def add_tags(self, *tags):
        self.tags.update(tag.lower() for tag in tags)

    def remove_tag(self, tag):
        self.tags.discard(tag.lower())

    def show_tags(self):
        return ', '.join(sorted(self.tags)) if self.tags else "No tags"

    def __str__(self):
        """
        Returns a string representation of the contact,
        including name, phones, birthday, email, notes, and address.
        """
        phone_str = ', '.join(str(k)
                              for k in self.phones) if self.phones else '📵 No phones'
        bday_str = f'🎂 Birthday:{Style.RESET_ALL}{self.birthday}' if self.birthday else '🎂 Birthday: Not set'
        note_str = f'📝 Note: {Style.RESET_ALL}{self.note}' if self.note else '📝 Note: Not set'
        email_str = f'✉️  Email:{Style.RESET_ALL}{self.email.value}' if self.email else '✉️  Email: Not set'
        address_str = f'🏠 Address: {Style.RESET_ALL}{self.address}' if self.address else '🏠 Address: Not set'
        tags_str = f'Tags: {self.show_tags()}' if self.tags else 'Tags: Not set'

        return (
            f"{Fore.CYAN}{'.' * 50}{Style.RESET_ALL}\n"
            f"👤{Fore.CYAN} Contact name:{Style.RESET_ALL} {self.name} \n"
            f"📞{Fore.CYAN} Phones:{Style.RESET_ALL} {phone_str}\n"
            f"{Fore.CYAN}{bday_str}{Style.RESET_ALL}\n"
            f"{Fore.CYAN}{email_str}{Style.RESET_ALL}\n"
            f"{Fore.CYAN}{note_str}{Style.RESET_ALL}\n"
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
        if validate_email(email):
            self._value = email
        else:
            raise ValueError(f"Invalid email format: {email}")


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

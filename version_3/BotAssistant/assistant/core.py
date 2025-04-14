from datetime import datetime
from colorama import init, Fore, Back, Style
from assistant.models import Record
from assistant.utils import exception_handler


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
def set_email(book, name, email):
    record = book.find_record(name)
    if record:
        record.set_email(email)
        return Fore.GREEN + f"Email {email} added to contact {name}" + Style.RESET_ALL
    raise KeyError("Contact not found")


@exception_handler
def edit_email(book, name, new_email):
    record = book.find_record(name)
    if record:
        record.set_email(new_email)
        return Fore.GREEN + f"Email {new_email} added to contact {name}" + Style.RESET_ALL
    raise KeyError("Contact not found")


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
    record.add_tags(*tags)
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

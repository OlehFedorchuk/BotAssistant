
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

class Phone(Field):
    """Class for sorting the phone"""
    def __init__(self, value):
        super().__init__(value)

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
        self.phones = [k for k in self.phones if k.value != phone] #!!!-- list comprehension
        
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
        phone_str = ', '.join(str(k) for k in self.phones) if self.phones else 'No phones'
        bday_str = f', Birthday: {self.birthday}' if self.birthday else ''
        return f'Contact name: {self.name}, phones: {phone_str} {bday_str}'

# ------- add_contact, change_contact, show_phone, search_contacts, show_all, delete_contact ------------------------     
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
    raise KeyError # 'Contact not found'

def show_phone(book, name):
    record = book.find_record(name)
    return str(record) if record else 'Contact was not found'

def search_contacts(book, query):
    results = [record for record in book.data.values() if query.lower() in record.name.value.lower()]
    if results:
        return "\n".join(str(record) for record in results)
    raise KeyError #"Contact not found"

def show_all(book):
    return str(book) if book else 'The contact list is empty'

@exception_handler
def delete_contact(book, name):
    if book.find_record(name):
        book.delete_record(name)
        return f'Contact {name} was deleted'
    raise KeyError #'Contact not found'


def main():
    # book = AddressBook()
    book = load_datа() # Download at the start
    
    print('Hi! I am a console assistant bot')
    while True:
        user_input = input('Enter command(hello, add, change, phone, search, all, delete, add-birthday, show-birthday, birthdays exit), name, phone number: ')
        parts = user_input.strip().split()
        if not parts:
            continue
        command, *args = parts
        
        if command in ('exit', 'close'):
            save_data(book) # saving data before going out
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
        elif command == 'show-birthday'and len(args) >= 1:
            print(show_birthday(book, args[0]))
        elif command == 'birthdays':
            print(upcoming_birthday(book))
        else:
            print('Unknown command or insufficient arguments. Please try again')
if __name__ == '__main__':
    main()
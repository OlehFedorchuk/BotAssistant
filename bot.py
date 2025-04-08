



class Phone(Field):
    """Class for sorting the phone"""
    def __init__(self, value):
        super().__init__(value)


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
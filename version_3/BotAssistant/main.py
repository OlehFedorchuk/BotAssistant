from assistant.storage import load_data, save_data
from assistant.utils import display_commands_table, guess_command
from assistant.core import (
    add_address, add_birthday_to_contact, add_contact, add_note,
    add_tags, change_contact, delete_contact, edit_address,
    edit_name, edit_note, remove_address, remove_email, remove_note,
    remove_phone, remove_tags, search_by_tag, search_contacts,
    show_all, show_birthday, set_email, edit_email, show_note, show_phone,
    sort_notes_by_tags, upcoming_birthday
)
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import InMemoryHistory
from colorama import init, Fore, Style

init(autoreset=True)


class SmartBotCompleter(Completer):
    def __init__(self, known_commands, address_book):
        self.commands = known_commands
        self.book = address_book

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.strip()
        words = text.split()

        if not words:
            return

        if len(words) == 1 and not document.text_before_cursor.endswith(' '):
            prefix = words[0].lower()
            for cmd in self.commands:
                if cmd.startswith(prefix):
                    yield Completion(cmd, start_position=- len(prefix))
        elif len(words) >= 2:
            command = words[0].lower()
            arg_prefix = words[-1].lower()

            contact_commands = {
                'name': [
                    'add', 'delete', 'search', 'edit-name', 'edit-phone', 'remove-phone',
                    'add-note', 'edit-note', 'remove-note', 'show-note',
                    'add-birthday', 'show-birtday',
                    'add-email', 'edit-email', 'remove-email',
                    'add-address', 'edit-addres', 'remove-address',
                    'phone', 'add-tag', 'remove-tag'
                ],
                'phone': ['edit-phone', 'remove-phone'],
                'email': ['edit-email', 'remove-email'],
                'tag': ['add-tag', 'remove-tag', 'show-tag', 'search-tag']
            }

            if command in contact_commands['name']:
                for name in self.book.data:
                    if name.lower().startswith(arg_prefix):
                        yield Completion(name, start_position=-len(arg_prefix))

            if command in contact_commands['phone']:
                for record in self.book.data.values():
                    for phone in record.phones:
                        if phone.value.startswith(arg_prefix):
                            yield Completion(phone.value, start_position=-len(arg_prefix))

            if command in contact_commands['email']:
                for record in self.book.data.values:
                    if record.email and record.email.value.lower().startwith(arg_prefix):
                        yield Completion(record.email.value, start_position=-len(arg_prefix))

            if command in contact_commands['tag']:
                all_tags = set()
                for record in self.book.data.values():
                    for tag in getattr(record, 'tag', []):
                        if tag.lower().startswith(arg_prefix):
                            all_tags.add(tag)
                for tag in sorted(all_tags):
                    yield Completion(tag, start_position=-len(arg_prefix))

            if command == 'add-birthday' and len(words) == 3:
                sample_dates = ['12.04.1990', '01.02.2003', '25.03.2003']
                for date in sample_dates:
                    if date.startswith(arg_prefix):
                        yield Completion(date, start_position=-len(arg_prefix))

            if command == 'add-email' and len(words) == 3:
                common_domains = ['@gmail.com', '@ukr.net', '@yahoo.com',]
                if '@' not in arg_prefix:
                    for domain in common_domains:
                        suggestion = arg_prefix + domain
                        yield Completion(suggestion, start_position=-len(arg_prefix))


def main():
    """
    The main function that runs the console assistant bot.
    Handles user input, processes commands, and interacts with the AddressBook.
    """

    # Load the address book data from a file or create a new one if the file doesn't exist
    book = load_data()

    # List of known commands supported by the bot
    known_commands = [
        "hello",
        "add", "search",
        "edit-name",
        "add-note", "edit-note", "remove-note", "show-note",
        "all",
        "delete",
        "add-birthday", "show-birthday",
        "add-email", "edit-email", "remove-email",
        "add-address", "edit-address", "remove-address",
        "birthdays",
        "edit-phone", "remove-phone",
        "phone",
        "add-tag", "remove-tag", "search-tag", "sort-notes",
        "exit", "close"
    ]

    command_completer = SmartBotCompleter(known_commands, book)
    history = InMemoryHistory()

    # Display a welcome message and the list of available commands
    print(Fore.BLUE + 'Hi! I am a console assistant bot' + Style.RESET_ALL)
    print()
    display_commands_table()

    # Main loop to process user commands
    while True:
        user_input = prompt("Enter command:", completer=command_completer, history=history,
                            complete_while_typing=True)
        print()

        if not user_input.strip():
            # Handle empty input
            print(Fore.YELLOW + 'Empty input. Please try again.' + Style.RESET_ALL)
            continue

        command = None
        args = []
        guess_result, args, _ = guess_command(user_input, known_commands)

        if guess_result is None:
            print(Fore.RED + 'Unknow command. Please try again.' + Style.RESET_ALL)

        command = guess_result

        def require_args(min_args, func):
            try:
                if len(args) >= min_args:
                    print(func())
                else:
                    print(Fore.RED + 'Not enough arguments.' + Style.RESET_ALL)
            except Exception as e:
                print((Fore.RED + f'[ERROR] {e}' + Style.RESET_ALL))

        if command:
            command = command.lower()

        match command:
            case "hello": print("Hello! How can I help you?" + Style.RESET_ALL)
            case 'add': require_args(2, lambda: add_contact(book, args[0], args[1]))
            case 'edit-phone': require_args(3, lambda: change_contact(book, *args[:3]))
            case "edit-name": require_args(2, lambda: edit_name(book, *args[:2]))
            case "add-note": require_args(2, lambda: add_note(book, args[0], ' '.join(args[1:])))
            case "edit-note": require_args(2, lambda: edit_note(book, args[0], ' '.join(args[1:])))
            case "remove-note": require_args(1, lambda: remove_note(book, args[0]))
            case "show-note": require_args(1, lambda: show_note(book, args[0]))
            case "phone": require_args(1, lambda: show_phone(book, args[0]))
            case "search": require_args(1, lambda: search_contacts(book, args[0]))
            case "all": print(show_all(book))
            case "delete": require_args(1, lambda: delete_contact(book, args[0]))
            case "add-birthday": require_args(2, lambda: add_birthday_to_contact(book, args[0], args[1]))
            case "show-birthday": require_args(1, lambda: show_birthday(book, args[0]))
            case "birthdays": print(upcoming_birthday(book))
            case "remove-phone": require_args(2, lambda: remove_phone(book, args[0], args[1]))
            case "add-email": require_args(2, lambda: set_email(book, args[0], args[1]))
            case "edit-email": require_args(2, lambda: edit_email(book, args[0], args[1]))
            case "remove-email": require_args(1, lambda: remove_email(book, args[0]))
            case "add-address": require_args(2, lambda: add_address(book, args[0], ' '.join(args[1:])))
            case "edit-address": require_args(2, lambda: edit_address(book, args[0], ' '.join(args[1:])))
            case "remove-address": require_args(1, lambda: remove_address(book, args[0]))
            case "add-tag": require_args(2, lambda: add_tags(book, args[0], *args[1:]))
            case "remove-tag": require_args(2, lambda: remove_tags(book, args[0], args[1]))
            case "search-tag": require_args(1, lambda: search_by_tag(book, args[0]))
            case "sort-notes": print(sort_notes_by_tags(book))
            case "exit" | "close":
                save_data(book)
                print(Fore.GREEN + "Goodbye!" + Style.RESET_ALL)
                break
            case _: print(Fore.RED + 'Unknown or unsupported command.' + Style.RESET_ALL)


if __name__ == "__main__":
    main()

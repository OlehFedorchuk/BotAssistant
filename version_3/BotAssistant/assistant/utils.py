import difflib
from colorama import Fore, Back, Style

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
            ("add-tag", "add tags"),  # Add a tag to a contact
            ("remove-tag", "remove tags"),  # Remove a tag from a contact
            ("show-tag", "show tags "),  # Show existing tags
            ("search-tag", "search tags"),  # Find a contact by tag
            ("sort-notes", "sort notes")  # Sorts notes by tag
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


def guess_command(user_input, known_commands, threshold=0.8):
    """
    Returns the most similar command and list of arguments.
    If similarity ≥ threshold, the command is applied automatically.
    """
    tokens = user_input.strip().split()
    if not tokens:
        return None, [], False
    input_cmd = tokens[0].lower()

    if input_cmd in known_commands:
        return input_cmd, tokens[1:], True

    best_match = None
    highest_ratio = 0.0

    for cmd in known_commands:
        ratio = difflib.SequenceMatcher(None, input_cmd, cmd).ratio()
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = cmd

    return best_match if highest_ratio >= 0.6 else None, tokens[1:], highest_ratio >= threshold

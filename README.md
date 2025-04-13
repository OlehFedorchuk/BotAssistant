# 🧠 Console Assistant Bot

A powerful and interactive **console assistant** written in Python. This project helps manage **contacts**, **notes**, **birthdays**, **emails**, and more — all via terminal commands. It’s your personal address book with smart CLI features!

---

## 📦 Features

- 📇 **Contact Management**: Add, edit, delete, and search for contacts.
- 📞 **Phone Number Support**: Validate and manage multiple numbers per contact.
- 📧 **Email Management**: Add, edit, and remove email addresses.
- 🎂 **Birthday Tracker**: Save birthdays and get notifications for upcoming ones.
- 📝 **Notes System**: Attach and manage notes for each contact.
- 🏠 **Address Management**: Add, edit, and remove addresses for contacts.
- 💾 **Auto Save**: Data is automatically saved and loaded using `pickle`.
- 💡 **Command Suggestions**: Mistyped a command? The bot suggests the closest match!
- 🎨 **Colorful UI**: Uses `colorama` for terminal UI highlights.

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.9+

---

### 🧰 Setup Virtual Environment

To isolate project dependencies, it’s recommended to use a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```
---

### 📥 Install Dependencies

This project relies on the following Python libraries:

- **colorama**: For colorful terminal output.
- **difflib**: For fuzzy matching of commands.
- **pickle**: For saving and loading data.
- **re**: For validating email formats.

After setting up the virtual environment, install the required dependencies:

```bash
pip install -r requirements.txt
```
---

## 🛠️ Available Commands

| Category  | Command         | Description                   | Example Parameters           |
| --------- | --------------- | ----------------------------- | ---------------------------- |
| General   | `hello`         | Greet the bot                 |                              |
|           | `exit`, `close` | Exit and save the assistant   |                              |
| Contacts  | `add`           | Add new contact               | name phone                   |
|           | `edit-name`     | Change contact name           | old name new name            |
|           | `delete`        | Delete a contact              | name                         |
|           | `search`        | Search by name or phone       | name, phone, email, note     | 
|           | `all`           | Show all contacts             | no input required            |
| Notes     | `add-note`      | Add a note to a contact       | name note                    |
|           | `edit-note`     | Edit existing note            | name new note                |
|           | `remove-note`   | Remove contact’s note         | name containing note         |
|           | `show-note`     | Display contact’s note        | name                         |
| Birthdays | `add-birthday`  | Add a birthday to a contact   | name date of birth           |
|           | `show-birthday` | Show a contact’s birthday     | name                         |
|           | `birthdays`     | View upcoming birthdays       | no input required            |
| Emails    | `add-email`     | Add email to contact          | name email                   |
|           | `edit-email`    | Change email                  | name new email               |
|           | `remove-email`  | Remove email                  | name                         |
| Phone     | `phone`         | Show a contact’s phone        | name                         |
|           | `edit-phone`    | Edit a contact’s phone number | name old phone new phone     |
|           | `remove-phone`  | Remove a phone                | name phone                   |
| Address   | `add-address`   | Add address                   | name address                 |
|           | `edit-address`  | Edit address                  | name old address new address |
|           | `remove-address`| Remove address                | name address                 |

## 💾 Data Persistence

All your data is stored locally in a `addressbook.pkl` file using Python's `pickle` module. Every time you exit the program, your data is saved automatically.

---

## 🧪 Input Validation

The app validates:

- **Phone Numbers** (only digits, length 9–14)
- **Birthdays** (must be in `DD.MM.YYYY` format)
- **Emails** (standard email regex check)

---

## 💡 Smart Features

- If you enter a wrong command (e.g. `ad` instead of `add`), the bot will suggest the most likely correct one using fuzzy matching (`difflib`).
- Uses `colorama` to make terminal interaction more user-friendly and readable.

---

## 📂 Project Structure

```
bot.py         # Main application file
addressbook.pkl      # Data saved automatically here
```

---

## 📖 Examples

### Add a new contact
```bash
> add John 123456789
Contact John with number 123456789 has been added
```

### Edit a contact's phone number
```bash
> edit-phone John 123456789 987654321
Contact John updated
```

### Add a note to a contact
```bash
> add-note John "This is a note for John"
Note added to contact John
```

### Show all contacts
```bash
> all
👤 Contact name: John
📞 Phones: 987654321
📝 Note: This is a note for John
```

### Search for a contact
```bash
> search John
👤 Contact name: John
📞 Phones: 987654321
📝 Note: This is a note for John
```

### Delete a contact
```bash
> delete John
Contact John was deleted
```

### Add a birthday to a contact
```bash
> add-birthday John 01.01.1990
Birthday 01.01.1990 added to contact John
```

### Show upcoming birthdays
```bash
> birthdays
John: 01.01.1990 (in 5 days)
```

---

## 🙌 Acknowledgements

- Powered by Python & Colorama 🌈

---

## 📃 License

This project is open-source and free to use under the MIT License.

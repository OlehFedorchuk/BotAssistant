# 🧠 Console Assistant Bot

A powerful and interactive **console assistant** written in Python. This project helps manage **contacts**, **notes**, **birthdays**, **emails**, and more — all via terminal commands. It’s your personal address book with smart CLI features!

---

## 📦 Features

- 📇 **Contact Management**: Add, edit, delete, and search for contacts.
- 📞 **Phone Number Support**: Validate and manage multiple numbers per contact.
- 📧 **Email Management**: Add, edit, and remove email addresses.
- 🎂 **Birthday Tracker**: Save birthdays and get notifications for upcoming ones.
- 📝 **Notes System**: Attach and manage notes for each contact.
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

## 🛠️ Available Commands

| Category  | Command         | Description                   |
| --------- | --------------- | ----------------------------- |
| General   | `hello`         | Greet the bot                 |
|           | `exit`, `close` | Exit and save the assistant   |
| Contacts  | `add`           | Add new contact               |
|           | `change`        | Edit a contact’s phone number |
|           | `edit-name`     | Change contact name           |
|           | `delete`        | Delete a contact              |
|           | `search`        | Search by name or phone       |
|           | `all`           | Show all contacts             |
| Notes     | `add-note`      | Add a note to a contact       |
|           | `edit-note`     | Edit existing note            |
|           | `remove-note`   | Remove contact’s note         |
|           | `show-note`     | Display contact’s note        |
| Birthdays | `add-birthday`  | Add a birthday to a contact   |
|           | `show-birthday` | Show a contact’s birthday     |
|           | `birthdays`     | View upcoming birthdays       |
| Emails    | `add-email`     | Add email to contact          |
|           | `edit-email`    | Change email                  |
|           | `remove-email`  | Remove email                  |

---

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

## 🙌 Acknowledgements

- Powered by Python & Colorama 🌈

---

## 📃 License

This project is open-source and free to use under the MIT License.

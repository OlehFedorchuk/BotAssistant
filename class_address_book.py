class AddressBook(UserDict):
    """Класс для управления записями контактов."""

    def add_record(self, record):
        self.data[record.name.value] = record

    def find_record(self, name):
        return self.data.get(name)

    def delete_record(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthday(self, days=7):
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
            return 'List is empty'
        return '\n'.join(str(record) for record in self.data.values())

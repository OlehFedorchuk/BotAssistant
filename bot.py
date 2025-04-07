import re
class Field:
    """Class for the record fields"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Class for storing the name of contact"""

    def __init__(self, value):
        super().__init__(value)

class Phone:
    def __init__(self, value: str):
        self._value = None
        self.value = value  

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value: str):
        if self.validate_phone(new_value):
            self._value = new_value
        else:
            raise ValueError("Invalid phone number format")

    @staticmethod
    def validate_phone(phone: str) -> bool:
        pattern = r"^(\+?\d{10,11})$"
        return re.match(pattern, phone) is not None

    def __str__(self):
        return self.value
    

    
def main():
    pass



if __name__ == "__main__":
    main()
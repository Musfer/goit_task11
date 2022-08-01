from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, name):
        self.value = name


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, phone_number=""):
        super().__init__(self)
        self.value = phone_number


class Birthday(Field):
    def __init__(self, birthday=""):
        super().__init__(self)
        try:
            birthday = datetime.strptime(birthday, '%m.%d.%Y')
        except ValueError:
            birthday = datetime.strptime(birthday, '%m.%d')
            birthday = birthday.replace(year=1)
        self.value = birthday


class Record:
    def __init__(self, name: Name, phones: list[Phone] = [], birthday: Birthday = None) -> None:
        self.name = name
        self.phones = phones
        self.birthday = birthday

    def __repr__(self):
        string = ""
        string += f"{self.name.value}:"
        if self.phones:
            string += f"\n\tPhone numbers: {', '.join([x.value for x in self.phones])}"
        if self.birthday:
            birthday = self.birthday.value
            if birthday.year > 1:
                string += f"\n\tBirthday: {birthday.strftime('%d %B %Y')}"
            else:
                string += f"\n\tBirthday: {birthday.strftime('%d %B')}"
            when_to_congratulate = self.days_to_birthday()
            if when_to_congratulate == 0:
                string += f"\n\tToday is {self.name.value}'s birthday."
            elif when_to_congratulate == 1:
                string += f"\n\t{self.name.value} has birthday tomorrow."
            else:
                string += f"\n\t{self.name.value}'s birthday is in {when_to_congratulate} days."
        string += "\n"
        return string

    def add_number(self, number: Phone):
        self.phones.append(number)

    def del_number(self, number: Phone):
        for x in self.phones:
            if x.value == number.value:
                self.phones.remove(x)

    def set_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def days_to_birthday(self):
        next_birthday = self.birthday.value.replace(year=datetime.now().year)
        next_birthday = next_birthday.replace(hour=0, minute=0, second=0, microsecond=0)
        current_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if next_birthday < current_day:
            next_birthday = next_birthday.replace(year=datetime.now().year+1)
        return (next_birthday-current_day).days


class AddressBook(UserDict):

    def __init__(self):
        super().__init__(self)
        self.showing_records = False  # when True 'enter' shows next N contacts
        self.show = None

    def add_record(self, record: Record):
        self.data[record.name.value] = record
        self.reset_iterator(2)

    def reset_iterator(self, n: int):
        self.show = self.iterator(n)

    def delete_record(self, name: str):
        self.data.pop(name)

    def iterator(self, n: int):
        string = ""
        for i, contact in enumerate(self.data.keys()):
            if not i % n:
                string = ""
            string += str(self.data.get(contact))
            if not (i+1) % n or i == len(self.data.keys())-1:
                yield string

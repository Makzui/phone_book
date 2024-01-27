from datetime import datetime
from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not self.is_valid_phone(value):
            raise ValueError
        super().__init__(value)

    @staticmethod
    def is_valid_phone(value):
        return len(value) == 10 and value.isdigit()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not self.is_valid_phone(new_value):
            raise ValueError
        self._value = new_value


class Birthday(Field):
    def __init__(self, value=None):
        if value and not self.is_valid_birthday(value):
            raise ValueError
        super().__init__(value)

    @staticmethod
    def _validate_birthday_format(value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value and not self.is_valid_birthday(new_value):
            raise ValueError
        self._value = new_value


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break

    def edit_phone(self, old_phone, new_phone):
        if not Phone.is_valid_phone(new_phone):
            raise ValueError
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            phone_to_edit.value = new_phone
        else:
            raise ValueError

    def find_phone(self, phone):
        return next((p for p in self.phones if p.value == phone), None)

    def days_to_birthday(self):
        if not self.birthday.value:
            return None
        today = datetime.today()
        next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day)
        if next_birthday < today:
            next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day)
        delta = next_birthday - today
        return delta.days

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __iter__(self):
        return self.iterator()

    def iterator(self, part_record=1):
        records = list(self.data.values())
        num_records = len(records)
        current_index = 0
        while current_index < num_records:
            yield records[current_index:current_index + part_record]
            current_index += part_record




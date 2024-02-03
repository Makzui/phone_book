from datetime import datetime
from collections import UserDict
import json

class Field:
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid value")
        self.__value = value

    def __str__(self):
        return str(self.__value)

    def is_valid(self, value):
        return True

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid value")
        self.__value = value


class Name(Field):
    pass


class Phone(Field):
    def is_valid(self, value):
        return value is not None and len(value) == 10 and value.isdigit()

    def __init__(self, value):
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value=None):
        if value:
            self._validate_birthday_format(value)
        super().__init__(value)

    def _validate_birthday_format(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError


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
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return
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

    def save_to_json(self, filename):
        with open(filename, "w") as fh:
            json.dump(list(self.data.values()), fh, indent=4, default=lambda x: x.__dict__)

    def load_from_json(self, filename):
        with open(filename, "r") as fh:
            data = json.load(fh)
            for item in data:
                record = Record(item['name'])
                for phone in item['phones']:
                    record.add_phone(phone)
                record.birthday = Birthday(item['birthday'])
                self.add_record(record)

    def search_by_name(self, search_string):
        results = []
        for record in self.data.values():
            if search_string.lower() in record.name.value.lower():
                results.append(record)
        return results

    def search_by_phone(self, search_string):
        results = []
        for record in self.data.values():
            for phone in record.phones:
                if search_string in phone.value:
                    results.append(record)
                    break  
        return results


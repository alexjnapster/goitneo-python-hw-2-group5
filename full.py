from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Номер телефону повинен містити 10 цифр")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Дата народження повинна бути у форматі РРРР-ММ-ДД")

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        found = False
        for p in self.phones:
            if p.value == old_phone:
                p.value = Phone(new_phone).value
                found = True
                break
        if not found:
            raise ValueError(f"Телефон {old_phone} не знайдено")

    def __str__(self):
        phones_str = ', '.join(p.value for p in self.phones)
        birthday_str = f", День народження: {self.birthday.value.strftime('%Y-%m-%d')}" if self.birthday else ""
        return f"Ім'я контакту: {self.name.value}, Телефони: {phones_str}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def get_birthdays_per_week(self):
        today = datetime.now()
        one_week_ahead = today + timedelta(days=7)
        birthdays_this_week = {}
        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                if today <= birthday_this_year <= one_week_ahead:
                    day_of_week = birthday_this_year.strftime("%A")
                    if day_of_week in ["Saturday", "Sunday"]:
                        day_of_week = "Monday"
                    if day_of_week not in birthdays_this_week:
                        birthdays_this_week[day_of_week] = []
                    birthdays_this_week[day_of_week].append(record.name.value)
        for day, names in sorted(birthdays_this_week.items()):
            print(f"{day}: {', '.join(names)}")

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)
    return inner

@input_error
def add_contact(book, name, phone, birthday=None):
    if name in book:
        book[name].add_phone(Phone(phone))
        if birthday:
            book[name].birthday = Birthday(birthday)
    else:
        book.add_record(Record(name, birthday))
        book[name].add_phone(Phone(phone))
    return "Контакт успішно додано."

@input_error
def show_all_contacts(book):
    if book:
        return "\n".join(str(record) for record in book.values())
    else:
        return "Контактів не знайдено."

def main():
    book = AddressBook()
    while True:
        command = input("Введіть команду: ").lower()
        if command in ["close", "exit"]:
            print("До побачення!")
            break
        elif command == "hello":
            print("Як я можу вам допомогти?")
        elif command.startswith("add "):
            _, name, phone, *birthday = command.split()
            birthday = birthday[0] if birthday else None
            print(add_contact(book, name, phone, birthday))
        elif command == "all":
            print(show_all_contacts(book))
        elif command == "birthdays":
            book.get_birthdays_per_week()
        else:
            print("Невідома команда.")

if __name__ == "__main__":
    main()

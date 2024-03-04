def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Будь ласка, надайте ім'я та телефон."
        except KeyError:
            return "Контакт не знайдено."
        except IndexError:
            return "Надано невірний ввід."
    return inner

@input_error
def add_contact(args, contacts):
    if len(args) != 3:
        raise ValueError
    name, phone, birthday = args
    contacts[name] = {"phone": phone, "birthday": birthday}
    return "Контакт додано."

@input_error
def change_contact(args, contacts):
    if len(args) != 2:
        raise ValueError
    name, new_phone = args
    if name not in contacts:
        raise KeyError
    contacts[name]["phone"] = new_phone
    return "Контакт оновлено."

@input_error
def show_phone(args, contacts):
    if len(args) != 1:
        raise IndexError
    name = args[0]
    if name not in contacts:
        raise KeyError
    return contacts[name]["phone"]

@input_error
def show_all(contacts):
    if not contacts:
        return "Контакти не знайдено."
    return "\n".join([f"{name}: {contact['phone']}" for name, contact in contacts.items()])

def main():
    contacts = {}
    print("Ласкаво просимо до помічника-бота!")
    while True:
        user_input = input("Введіть команду: ")
        def parse_input(user_input):
            # Implement the logic to parse the user input
            pass

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("До побачення!")
            break
        elif command == "hello":
            print("Як я можу вам допомогти?")
        elif command == "add":
            response = add_contact(args, contacts)
            print(response)
        elif command == "change":
            response = change_contact(args, contacts)
            print(response)
        elif command == "phone":
            response = show_phone(args, contacts)
            print(response)
        elif command == "all":
            response = show_all(contacts)
            print(response)
        else:
            print("Невірна команда.")

if __name__ == "__main__":
    main()

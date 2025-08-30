from typing import Callable, Dict, List, Tuple

Contacts = Dict[str, str]

def input_error(func: Callable) -> Callable:
    """Декоратор: перетворює типові помилки введення на дружні повідомлення."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command."
        except KeyError:
            return "Contact not found."
    return inner

def parse_input(user_input: str) -> Tuple[str, List[str]]:
    parts = user_input.strip().split()
    if not parts:
        return "", []
    cmd, *args = parts
    return cmd.lower(), args

@input_error
def add_contact(args: List[str], contacts: Contacts) -> str:
    name, phone = args  # розпаковка сама кине ValueError якщо аргументів ≠ 2
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args: List[str], contacts: Contacts) -> str:
    name, phone = args
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return "Contact updated."

@input_error
def show_phone(args: List[str], contacts: Contacts) -> str:
    name = args[0]  # IndexError якщо args порожній
    if name not in contacts:
        raise KeyError
    return f"{name}: {contacts[name]}"

@input_error
def show_all(args: List[str], contacts: Contacts) -> str:
    if not contacts:
        return "No contacts yet."
    return "\n".join(f"{n}: {p}" for n, p in contacts.items())

@input_error
def hello(args: List[str], contacts: Contacts) -> str:
    return "How can I help you?"

def main():
    contacts: Contacts = {}
    commands = {
        "hello": hello,
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
    }
    exit_cmds = {"exit", "close", "quit", "bye", "goodbye", "good-bye"}

    while True:
        cmd, args = parse_input(input("Enter a command: "))

        if not cmd:
            print("Enter the argument for the command.")
            continue

        # вихід
        if cmd in exit_cmds or (cmd == "good" and args and args[0].lower() == "bye"):
            print("Good bye!")
            break

        handler = commands.get(cmd)
        if not handler:
            print("Unknown command. Available: hello, add, change, phone, all, exit")
            continue

        result = handler(args, contacts)
        if result:
            print(result)

if __name__ == "__main__":
    main()

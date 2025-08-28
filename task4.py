# assistant_bot.py
from typing import Callable, Dict, List, Tuple

Contacts = Dict[str, str]


def input_error(func: Callable) -> Callable:
    """
    Декоратор для обробки типових помилок введення користувача.
    Повертає дружні повідомлення замість падіння програми.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError as e:
            # Якщо хендлер задав власний текст помилки — покажемо його,
            # інакше виведемо універсальну підказку:
            return str(e) if str(e) else "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command."
    return inner


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    """
    Розбиває рядок користувача на команду та аргументи.
    """
    parts = user_input.strip().split()
    if not parts:
        return "", []
    cmd, *args = parts
    return cmd.lower(), args


@input_error
def add_contact(args: List[str], contacts: Contacts) -> str:
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args[0], args[1]
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: List[str], contacts: Contacts) -> str:
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args[0], args[1]
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args: List[str], contacts: Contacts) -> str:
    if not args:
        # Узгоджено з вимогами — нехай це мепиться на IndexError
        raise IndexError
    name = args[0]
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
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "hello": hello,
        # зручні синоніми виходу:
        "exit": None, "close": None, "good": None, "goodbye": None, "good-bye": None, "bye": None,
        "quit": None,
    }

    while True:
        user_input = input("Enter a command: ").strip()
        cmd, args = parse_input(user_input)

        # Порожній ввід — підказка і продовжуємо
        if not cmd:
            print("Enter the argument for the command")
            continue

        # Обробка виходу (врахуємо 'good bye' як два слова)
        if cmd in ("exit", "close", "quit", "bye"):
            print("Good bye!")
            break
        if cmd == "good" and args and args[0].lower() == "bye":
            print("Good bye!")
            break

        handler = commands.get(cmd)
        if handler is None and cmd not in ("exit", "close", "quit", "bye", "good"):
            print("Unknown command. Available: hello, add, change, phone, all, exit")
            continue

        if handler:
            result = handler(args, contacts)
            if result:
                print(result)
        else:
            # handler is None only for exit-like commands which are handled above
            pass


if __name__ == "__main__":
    main()

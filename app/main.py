import sys
from collections.abc import Callable
import shutil

Builtin = Callable[[list[str]], bool]

BUILTIN = ["echo", "exit", "type"]


def echo(arguments: list[str]) -> bool:
    print(" ".join(arguments))
    return True


def exit_shell(_: list[str]) -> bool:
    return False


def type_command(arguments: list[str]) -> bool:
    if not arguments:
        print("type: missing argument")
        return True

    command = arguments[0]
    if command in BUILTIN:
        print(f"{command} is a shell builtin")
    elif executable := shutil.which(command):
        print(f"{command} is {executable}")
    else:
        print(f"{command}: not found")
    return True


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        try:
            line = input()
        except EOFError:
            break

        if not line:
            continue

        parts = line.split()
        command = parts[0]
        arguments = parts[1:]

        if command == "exit":
            break
        elif command == "echo":
            echo(arguments)
        elif command == "type":
            type_command(arguments)
        elif executable := shutil.which(command):
            print(f"{command} is {executable}")
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()
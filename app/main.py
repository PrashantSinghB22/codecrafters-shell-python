import sys
import os
import subprocess
from typing import Union


class Shell(object):
    """Basic Shell class"""

    __return_code: int = 0
    __path: list[str] = []
    __METHODS: list[str] = []

    def __init__(self) -> None:
        super().__init__()
        self.__path = os.environ["PATH"].split(":")
        self.__METHODS = [
            f
            for f in dir(self)
            if callable(getattr(self, f)) and "__" not in f and not f.startswith("_")
        ]  # pyright: ignore[reportConstantRedefinition, reportAny, reportAttributeAccessIssue, reportUnknownMemberType]
        self.METHODS: list = self.__METHODS

    def exit(self) -> None:
        sys.exit(0)

    def echo(self, *args: list[str]) -> None:
        print(f"{' '.join(args)}")  # pyright: ignore[reportCallIssue, reportArgumentType]
        self.__return_code = 0

    def __walk_path(self, command: str) -> str:
        for p in self.__path:
            path: str = os.path.join(p, command)
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path
        return ""

    def _valid_command(self, command: str) -> function | str | None:
        if command in self.__METHODS:
            return getattr(self, command)
        elif exe := self.__walk_path(command):
            return exe
        else:
            return None

    def type(self, *args) -> None:  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        command: str = args[0]  # pyright: ignore[reportUnknownVariableType]
        targ = self._valid_command(command)
        if callable(targ):
            print(f"{command} is a shell builtin")
        elif targ:
            print(f"{command} is {targ}")
        else:
            print(f"{command}: not found")
            self.__return_code = 0

    def pwd(self)-> None:
        print(os.getcwd())
        self.__return_code = 0

    def cd(self, *args) -> None:
        directory = args[0]
        try :
            os.chdir(directory)
            self.__return_code = 0
        except FileNotFoundError:
            print(f"cd: {directory}: No such file or directory")


    


def main():
    my_shell = Shell()
    while True:
        _ = sys.stdout.write("$ ")
        usr_input = input()
        first = usr_input.split()[0]
        if run := my_shell._valid_command(first):
            if callable(run):
                run(*usr_input.split()[1:])
            else:
                print(subprocess.check_output(usr_input.split()).decode(), end="")

        else:
            print(f"{first}: command not found")


if __name__ == "__main__":
    main()











    









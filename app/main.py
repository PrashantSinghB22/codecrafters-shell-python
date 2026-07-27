import os
import sys
import subprocess
import shlex

builtins = {"echo", "exit", "type", "pwd", "cd"}


def find_executable(name):
    path = os.environ["PATH"]
    directories = path.split(os.pathsep)

    for directory in directories:
        full_path = os.path.join(directory, name)

        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path

    return None

def handle_exit():
    sys.exit()

def handle_echo(parts):
    print(" ".join(parts[1:]))

def handle_pwd():
    print(os.getcwd())

def handle_type(parts):
    name = parts[1]

    if name in builtins:
        print(f"{name} is a shell builtin")
    else: 
        executable = find_executable(name)

        if executable:
            print(f"{name} is {executable}")

        else:
            print(f"{name}: not found")

def run_external(parts):
    executable = find_executable(parts[0])

    if executable:
        
        subprocess.run(parts, executable=executable)
    else:
        print(f"{parts[0]}: command not found")

def handle_cd(parts):
    directory = parts[1]

    if directory == "~":
        directory = os.getenv("HOME")

    if os.path.isdir(directory):
        os.chdir(directory)
    else:
        print(f"cd: {directory}: No such file or directory")




def main():
    while True:
        sys.stdout.write("$ ")
        command_line = input()

        parts = shlex.split(command_line)

        if not parts:
            continue

        command = parts[0]

        if command == "exit":
            handle_exit()

        elif command == "echo":
            handle_echo(parts)

        elif command == "type":
            handle_type(parts)

        elif command == "pwd":
            handle_pwd()

        elif command == "cd":
            handle_cd(parts)

        else:
            run_external(parts)



if __name__ == "__main__":
    main()
import os
import sys
import subprocess
import shlex

builtins = {"echo", "exit", "type", "pwd", "cd"}


def find_executable(name):
    path = os.environ["PATH"]

    for directory in path.split(os.pathsep):
        full_path = os.path.join(directory, name)

        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path

    return None


def output(text, stdout_file):
    if stdout_file is None:
        print(text)
    else:
        with open(stdout_file, "w") as f:
            print(text, file=f)


def handle_exit():
    sys.exit()


def handle_echo(parts, stdout_file):
    output(" ".join(parts[1:]), stdout_file)


def handle_pwd(stdout_file):
    output(os.getcwd(), stdout_file)


def handle_type(parts, stdout_file):
    name = parts[1]

    if name in builtins:
        output(f"{name} is a shell builtin", stdout_file)
    else:
        executable = find_executable(name)

        if executable:
            output(f"{name} is {executable}", stdout_file)
        else:
            output(f"{name}: not found", stdout_file)


def handle_cd(parts):
    directory = parts[1]

    if directory == "~":
        directory = os.getenv("HOME")

    if os.path.isdir(directory):
        os.chdir(directory)
    else:
        print(f"cd: {directory}: No such file or directory")


def run_external(parts, stdout_file, stderr_file):
    executable = find_executable(parts[0])

    if executable is None:
        print(f"{parts[0]}: command not found")
        return

    stdout = None
    stderr = None
    try:
        if stdout_file is not None:
            stdout = open(stdout_file, "w")

        if stderr_file is not None:
            stderr = open(stderr_file, "w")

        subprocess.run(
            parts,
            executable = executable,
            stdout = stdout,
            stderr = stderr
        )

    finally:
        if stdout is not None:
            stdout.close()
        if stderr is not None:
            stderr.close()

    


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        try:
            command_line = input()
        except EOFError:
            break

        parts = shlex.split(command_line)

        if not parts:
            continue

        stdout_file = None
        stderr_file = None

        if ">" in parts:
            index = parts.index(">")
            stdout_file = parts[index + 1]
            parts = parts[:index]

        elif "1>" in parts:
            index = parts.index("1>")
            stdout_file = parts[index + 1]
            parts = parts[:index]
        elif "2>" in parts:
            index = parts.index("2>")
            stderr_file = parts[index + 1]
            parts = parts[:index]

        if not parts:
            continue

        command = parts[0]

        if command == "exit":
            handle_exit()

        elif command == "echo":
            handle_echo(parts, stdout_file)

        elif command == "type":
            handle_type(parts, stdout_file)

        elif command == "pwd":
            handle_pwd(stdout_file)

        elif command == "cd":
            handle_cd(parts)

        else:
            run_external(parts, stdout_file)


if __name__ == "__main__":
    main()
    
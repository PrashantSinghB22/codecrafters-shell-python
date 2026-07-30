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


def output(text, stdout_file, append_stdout):
    if stdout_file is None:
        print(text)
    else:
        mode = "a" if append_stdout else "w"
        with open(stdout_file, mode) as f:
            print(text, file=f)


def handle_exit():
    sys.exit()


def handle_echo(parts, stdout_file, append_stdout):
    output(" ".join(parts[1:]), stdout_file)


def handle_pwd(stdout_file, append_stdout):
    output(os.getcwd(), stdout_file)


def handle_type(parts, stdout_file, append_stdout):
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
        print(f"cd: {directory}: No such file or directory", file=sys.stderr)


def run_external(parts, stdout_file, stderr_file, append_stdout):
    executable = find_executable(parts[0])

    if executable is None:
        print(f"{parts[0]}: command not found", file=sys.stderr)
        return

    stdout = None
    stderr = None

    try:
        if stdout_file is not None:
            mode = "a" if append_stdout else "w"
            stdout = open(stdout_file, mode)

        if stderr_file is not None:
            stderr = open(stderr_file, "w")

        subprocess.run(
            parts,
            executable=executable,
            stdout=stdout,
            stderr=stderr,
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
        append_stdout = False

        

        if "1>>" in parts:
            index = parts.index(">>")
            stdout_file = parts[index+1]
            append_stdout = True

        elif ">>" in parts:
            index = parts.index(">>")
            stdout_file = parts[index+1]
            append_stdout = True

        elif "1>" in parts:
            index = parts.index(">")
            stdout_file = parts[index + 1]
            parts = parts[:index]

        elif ">" in parts:
            index = parts.index("1>")
            stdout_file = parts[index + 1]
            parts = parts[:index]

        if "2>" in parts:
            index = parts.index("2>")
            stderr_file = parts[index + 1]
            parts = parts[:index]

        if stdout_file is not None:
            open(stdout_file, "w").close()

        if stderr_file is not None:
            open(stderr_file, "w").close()

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
            run_external(parts, stdout_file, stderr_file)


if __name__ == "__main__":
    main()

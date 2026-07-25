import sys


COMMANDS = {
    "exit": lambda _: sys.exit(),
    "echo": lambda args: print(" ".join(args)),
    "type": lambda args: print(f"{args[0]} is a shell builtin")
    if args[0] in COMMANDS
    else print(f"{args[0]}: not found"),
}


def execute(cmd, *args):
    if cmd in COMMANDS:
        COMMANDS[cmd](*args)
    else:
        sys.stdout.write(f"{cmd}: command not found\n")


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        line = sys.stdin.readline()
        line.strip()

        if not line:
            continue

        cmd, *args = line.split()

        execute(cmd, args)


if __name__ == "__main__":
    main()

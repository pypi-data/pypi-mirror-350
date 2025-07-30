import sys
import os
from vcs.commands.add import add
from vcs.commands.init import init
from vcs.commands.commit import commit
from vcs.commands.log import log
from vcs.commands.show import show
from vcs.commands.checkout import checkout
VCS_DIR = ".vcs"
CONFIG_FILE = os.path.join(VCS_DIR, "config")

def is_config_present():
    return os.path.exists(CONFIG_FILE) and os.path.getsize(CONFIG_FILE) > 0


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [options]")
        return

    command = sys.argv[1]

    if command == "init":
        init()
    elif command == "auth": 
        if len(sys.argv) != 4:
            print("Usage: vcs auth <username> <email>")
            return
        username = sys.argv[2]
        email = sys.argv[3]
        config_content = f"username: {username}\nemail: {email}\n"
        os.makedirs(VCS_DIR, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            f.write(config_content)
        print(f"Configured user: {username} <{email}>")

    elif command == "add":
        if len(sys.argv) < 3:
            print("Error: 'add' requires a filename.")
        else:
            for file in sys.argv[2:]:
                add(file)
    elif command == "commit":
        if len(sys.argv) < 4 or sys.argv[2] != "-m":
            print('Error: Usage: vcs commit -m "your message"')
        elif not is_config_present():
            print("Error: Author not configured. Use `vcs auth <username> <email>` first.")
        else:
            message = " ".join(sys.argv[3:])
            commit(message)
    elif command == "log":
        if not is_config_present():
            print("Error: Author not configured. Use `vcs auth <username> <email>` first.")
        else:
            log()
    elif command == "show":
        if len(sys.argv) != 3:
            print("Usage: vcs show <commit_hash>")
        else:
            commit_hash = sys.argv[2]
            show(commit_hash)
    elif command == "checkout":
        if len(sys.argv) != 3:
            print("Usage: vcs checkout <commit_hash>")
        else:
            commit_hash = sys.argv[2]
            checkout(commit_hash)
    else:
        print(f"Unknown command: {command}")
        print("Available commands: init, auth, add, commit, log, show, checkout")

if __name__ == "__main__":
    main()

import os
import zlib
import datetime
VCS_DIR = ".vcs"
OBJECTS_DIR = os.path.join(VCS_DIR, "objects")
INDEX_FILE = os.path.join(VCS_DIR, "index")
HEAD_FILE = os.path.join(VCS_DIR, "head")
def read_object(hash):
    dir_name = os.path.join(OBJECTS_DIR, hash[:2])
    file_name = os.path.join(dir_name, hash[2:])
    if not os.path.exists(file_name):
        return None

    with open(file_name, "rb") as f:
        compressed = f.read()
        decompressed = zlib.decompress(compressed)
        return decompressed

def parse_commit_object(data):
    """Parses a raw commit object and returns a dict with its fields."""
    lines = data.decode().split("\n")
    info = {
        "tree": None,
        "parent": None,
        "author_name": None,
        "author_email": None,
        "timestamp": None,
        "message": ""
    }

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("tree "):
            info["tree"] = line[5:].strip()
        elif line.startswith("parent "):
            info["parent"] = line[7:].strip()
        elif line.startswith("author "):
            # Format: author John Doe <john@example.com> 1716722244 +0000
            parts = line[7:].strip().rsplit(" ", 2)
            name_email = parts[0]
            timestamp = parts[1]
            if "<" in name_email and ">" in name_email:
                name = name_email[:name_email.find("<")].strip()
                email = name_email[name_email.find("<")+1:name_email.find(">")].strip()
                info["author_name"] = name
                info["author_email"] = email
                info["timestamp"] = timestamp
        elif line.strip() == "":
            # Remaining lines are the message
            info["message"] = "\n".join(lines[i+1:]).strip()
            break
        i += 1

    return info


def log():
    if not os.path.exists(HEAD_FILE):
        print("No commits yet.")
        return

    current_hash = open(HEAD_FILE).read().strip()

    while current_hash:
        obj = read_object(current_hash)
        if not obj:
            print(f"Error: Cannot read object {current_hash}")
            break

        # Strip header like "commit 123\0"
        null_idx = obj.find(b'\0')
        content = obj[null_idx+1:]  # skip the header
        commit_data = parse_commit_object(content)

        print(f"commit {current_hash}")
        print(f"Author: {commit_data['author_name']} <{commit_data['author_email']}>")
        if commit_data["timestamp"]:
            dt = datetime.datetime.utcfromtimestamp(int(commit_data["timestamp"]))
            print(f"Date:   {dt.strftime('%a %b %d %H:%M:%S %Y +0000')}")
        print()
        print(f"    {commit_data['message']}")
        print()

        current_hash = commit_data.get("parent")  # move to parent commit
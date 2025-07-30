import os
import zlib
from datetime import datetime

VCS_DIR = ".vcs"
OBJECTS_DIR = os.path.join(VCS_DIR, "objects")

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
            info["message"] = "\n".join(lines[i+1:]).strip()
            break
        i += 1

    return info

def show(commit_hash):
    obj = read_object(commit_hash)
    if not obj:
        print(f"fatal: object {commit_hash} not found")
        return

    commit_data = parse_commit_object(obj)

    print(f"commit {commit_hash}")
    print(f"Tree: {commit_data['tree']}")
    if commit_data["parent"]:
        print(f"Parent: {commit_data['parent']}")

    # Optional: Convert timestamp to readable date
    try:
        dt = datetime.utcfromtimestamp(int(commit_data["timestamp"]))
        time_str = dt.strftime("%a %b %d %H:%M:%S %Y +0000")
    except:
        time_str = commit_data["timestamp"]

    print(f"Author: {commit_data['author_name']} <{commit_data['author_email']}>")
    print(f"Date:   {time_str}\n")
    print(f"    {commit_data['message']}\n")

    # Optional: show tree snapshot (you can extend this later)
    # For now, just print the tree hash

import hashlib
import os
import zlib
import time

VCS_DIR = ".vcs"
OBJECTS_DIR = os.path.join(VCS_DIR, "objects")
INDEX_FILE = os.path.join(VCS_DIR, "index")
HEAD_FILE = os.path.join(VCS_DIR, "HEAD")
CONFIG_FILE = os.path.join(VCS_DIR, "config")


def hash_file_contents(content):
    return hashlib.sha1(content).hexdigest()


def read_user_config():
    if not os.path.exists(CONFIG_FILE):
        raise Exception("Error: Author not configured. Use `vcs auth <name> <email>` first.")
    
    with open(CONFIG_FILE, "r") as f:
        lines = f.readlines()
        username = email = None
        for line in lines:
            if line.startswith("username:"):
                username = line.split(":", 1)[1].strip()
            elif line.startswith("email:"):
                email = line.split(":", 1)[1].strip()
    
    if not username or not email:
        raise Exception("Error: Incomplete author information in config.")
    
    return username, email


class Tree:
    def __init__(self):
        self.entries = []

    def add_blob(self, mode, name, hash):
        self.entries.append((mode, name, hash))

    def add_tree(self, mode, name, hash):
        self.entries.append((mode, name, hash))

    def serialize(self):
        content = b""
        for mode, name, hash in self.entries:
            entry = f"{mode} {name}\0".encode() + bytes.fromhex(hash)
            content += entry
        return content

    def store(self):
        content = self.serialize()
        header = f"tree {len(content)}\0".encode()
        full_content = header + content
        hash = hash_file_contents(full_content)

        dir_name = os.path.join(OBJECTS_DIR, hash[:2])
        file_name = os.path.join(dir_name, hash[2:])

        if not os.path.exists(file_name):
            os.makedirs(dir_name, exist_ok=True)
            compressed_content = zlib.compress(full_content)

            with open(file_name, "wb") as f:
                f.write(compressed_content)

        return hash


class Commit:
    def __init__(self, tree_hash, message, author_name, author_email, parent=None):
        self.tree_hash = tree_hash
        self.message = message
        self.author_name = author_name
        self.author_email = author_email
        self.parent = parent

    def serialize(self):
        lines = [f"tree {self.tree_hash}"]
        if self.parent:
            lines.append(f"parent {self.parent}")
        timestamp = int(time.time())
        author_line = f"{self.author_name} <{self.author_email}> {timestamp} +0000"
        lines.append(f"author {author_line}")
        lines.append(f"committer {author_line}")
        lines.append("")
        lines.append(self.message)
        return "\n".join(lines).encode()

    def store(self):
        content = self.serialize()
        header = f"commit {len(content)}\0".encode()
        full_content = header + content
        hash = hash_file_contents(full_content)

        dir_name = os.path.join(OBJECTS_DIR, hash[:2])
        file_name = os.path.join(dir_name, hash[2:])

        if not os.path.exists(file_name):
            os.makedirs(dir_name, exist_ok=True)
            compressed_content = zlib.compress(full_content)
            with open(file_name, "wb") as f:
                f.write(compressed_content)

        with open(HEAD_FILE, "w") as f:
            f.write(hash)

        return hash


def parse_index():
    entries = []
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as f:
            for line in f:
                hash, path = line.strip().split(" ", 1)
                entries.append((path, hash))
    return entries


def build_tree(entries):
    root = {}

    for path, blob_hash in entries:
        parts = path.split(os.sep)
        current = root
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        current[parts[-1]] = blob_hash

    def build_subtree(subtree):
        tree = Tree()
        for name, value in sorted(subtree.items()):
            if isinstance(value, dict):
                sub_hash = build_subtree(value)
                tree.add_tree("40000", name, sub_hash)
            else:
                tree.add_blob("100644", name, value)
        return tree.store()

    return build_subtree(root)


def commit(message):
    try:
        author_name, author_email = read_user_config()
    except Exception as e:
        print(e)
        return

    entries = parse_index()
    if not entries:
        print("Nothing to commit. Index is empty.")
        return

    tree_hash = build_tree(entries)

    parent = None
    if os.path.exists(HEAD_FILE):
        with open(HEAD_FILE, "r") as f:
            parent = f.read().strip()

    commit_obj = Commit(tree_hash, message, author_name, author_email, parent)
    commit_hash = commit_obj.store()
    print(f"[{commit_hash}] {message}")

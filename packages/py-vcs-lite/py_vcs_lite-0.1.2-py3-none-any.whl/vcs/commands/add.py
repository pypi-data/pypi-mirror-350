import hashlib
import os
import zlib
VCS_DIR = ".vcs"
OBJECTS_DIR = os.path.join(VCS_DIR, "objects")
INDEX_FILE = os.path.join(VCS_DIR, "index")


def hash_file_contents(content):
    return hashlib.sha1(content).hexdigest()


def store_object(content):
    # Create blob header
    header = f"blob {len(content)}\0".encode()
    full_content = header + content

    # Hash the full content (header + body)
    hash = hash_file_contents(full_content)

    # Determine object path: .vcs/objects/xx/yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
    dir_name = os.path.join(OBJECTS_DIR, hash[:2])
    file_name = os.path.join(dir_name, hash[2:])

    if not os.path.exists(file_name):
        os.makedirs(dir_name, exist_ok=True)
        compressed_content = zlib.compress(full_content)

        with open(file_name, "wb") as f:
            f.write(compressed_content)

    return hash



def update_index(file_path, hash):
    file_path = os.path.relpath(file_path)  # Store as relative path
    entries = {}

    # Load existing index entries
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as f:
            for line in f:
                h, path = line.strip().split(" ", 1)
                entries[path] = h

    # Update entry
    entries[file_path] = hash

    # Write back sorted index
    with open(INDEX_FILE, "w") as f:
        for path in sorted(entries):
            f.write(f"{entries[path]} {path}\n")


def _add_single_file(file_path):
    file_path = os.path.relpath(file_path)
    with open(file_path, "rb") as f:
        content = f.read()

    hash = store_object(content)
    update_index(file_path, hash)

    print(f"added {file_path}")
    return hash
def add(file_path):
    if not os.path.exists(file_path):
        print(f"fatal: path '{file_path}' does not exist")
        return

    if os.path.isdir(file_path):
        for root, _, files in os.walk(file_path):
            if VCS_DIR in root:
                continue  # Skip .vcs directory

            for file in files:
                full_path = os.path.join(root, file)
                # Avoid adding files inside .vcs
                if VCS_DIR in os.path.relpath(full_path).split(os.sep):
                    continue

                _add_single_file(full_path)
    else:
        _add_single_file(file_path)

import os
import zlib
import shutil

VCS_DIR = ".vcs"
OBJECTS_DIR = os.path.join(VCS_DIR, "objects")
HEAD_FILE = os.path.join(VCS_DIR, "HEAD")
INDEX_FILE = os.path.join(VCS_DIR, "index")


def read_object(hash):
    dir_name = os.path.join(OBJECTS_DIR, hash[:2])
    file_name = os.path.join(dir_name, hash[2:])
    if not os.path.exists(file_name):
        return None

    with open(file_name, "rb") as f:
        compressed = f.read()
        decompressed = zlib.decompress(compressed)
        return decompressed


def parse_tree(tree_bytes):
    entries = []
    i = 0
    length = len(tree_bytes)
    while i < length:
        space_index = tree_bytes.find(b' ', i)
        mode = tree_bytes[i:space_index].decode()
        i = space_index + 1

        null_index = tree_bytes.find(b'\0', i)
        name = tree_bytes[i:null_index].decode()
        i = null_index + 1

        sha_raw = tree_bytes[i:i + 20]
        hash_hex = sha_raw.hex()
        i += 20

        entries.append((mode, name, hash_hex))
    return entries


def write_file(path, content):
    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    with open(path, "wb") as f:
        f.write(content)


def restore_tree(tree_hash, path=""):
    tree_obj = read_object(tree_hash)
    if not tree_obj:
        print(f"Error: Tree object {tree_hash} not found")
        return

    null_index = tree_obj.find(b'\0')
    content = tree_obj[null_index + 1:]

    entries = parse_tree(content)
    for mode, name, obj_hash in entries:
        full_path = os.path.join(path, name)
        if mode == "40000":
            if not os.path.exists(full_path):
                os.makedirs(full_path)
            restore_tree(obj_hash, full_path)
        else:
            blob_obj = read_object(obj_hash)
            if blob_obj:
                null_index_blob = blob_obj.find(b'\0')
                file_content = blob_obj[null_index_blob + 1:]
                write_file(full_path, file_content)


def build_index_from_tree(tree_hash, base_path=""):
    entries_list = []

    tree_obj = read_object(tree_hash)
    if not tree_obj:
        return entries_list

    null_index = tree_obj.find(b'\0')
    content = tree_obj[null_index + 1:]

    entries = parse_tree(content)
    for mode, name, obj_hash in entries:
        full_path = os.path.join(base_path, name)
        if mode == "40000":
            entries_list.extend(build_index_from_tree(obj_hash, full_path))
        else:
            entries_list.append((full_path, obj_hash))

    return entries_list


def update_index_from_commit_tree(tree_hash):
    entries = build_index_from_tree(tree_hash)
    with open(INDEX_FILE, "w") as f:
        for path, h in sorted(entries):
            f.write(f"{h} {path}\n")


def get_all_files_and_dirs(base_path="."):
    all_paths = set()
    for root, dirs, files in os.walk(base_path, topdown=True):
        if ".vcs" in dirs:
            dirs.remove(".vcs")

        rel_root = os.path.relpath(root, base_path)
        if rel_root == ".":
            rel_root = ""

        for d in dirs:
            all_paths.add(os.path.join(rel_root, d))
        for f in files:
            all_paths.add(os.path.join(rel_root, f))
    return all_paths


def cleanup_working_directory(commit_paths):
    current_paths = get_all_files_and_dirs()
    commit_path_set = set(commit_paths)

    to_delete = sorted(current_paths - commit_path_set, reverse=True)

    for path in to_delete:
        full_path = os.path.join(".", path)
        if os.path.isfile(full_path):
            os.remove(full_path)
            print(f"Removed file: {path}")
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path)
            print(f"Removed directory: {path}")


def checkout(commit_hash):
    commit_obj = read_object(commit_hash)
    if not commit_obj:
        print(f"Error: Commit {commit_hash} not found")
        return

    null_index = commit_obj.find(b'\0')
    content = commit_obj[null_index + 1:]
    lines = content.decode().split('\n')

    tree_hash = None
    for line in lines:
        if line.startswith("tree "):
            tree_hash = line[5:].strip()
            break

    if not tree_hash:
        print(f"Error: No tree found in commit {commit_hash}")
        return

    # Get list of paths that should exist
    entries = build_index_from_tree(tree_hash)
    commit_paths = [path for path, _ in entries]

    # Clean up everything else
    cleanup_working_directory(commit_paths)

    # Restore files from the commit
    restore_tree(tree_hash)

    # Update HEAD and index
    with open(HEAD_FILE, "w") as f:
        f.write(commit_hash)

    update_index_from_commit_tree(tree_hash)

    print(f"Checked out commit {commit_hash}")

import os
import shutil

def get_all_files_and_dirs(base_path="."):
    """
    Recursively collect all files and directories in base_path,
    excluding the .vcs directory.
    Returns a set of paths relative to base_path.
    """
    all_paths = set()
    for root, dirs, files in os.walk(base_path, topdown=True):
        # Exclude .vcs directory from walking
        if ".vcs" in dirs:
            dirs.remove(".vcs")
        
        # Relative root path
        rel_root = os.path.relpath(root, base_path)
        if rel_root == ".":
            rel_root = ""
        
        # Add directories (relative path)
        for d in dirs:
            all_paths.add(os.path.join(rel_root, d))
        # Add files (relative path)
        for f in files:
            all_paths.add(os.path.join(rel_root, f))
    return all_paths


def cleanup_working_directory(commit_files):
    """
    Remove any file or directory in the working directory that is NOT
    listed in commit_files.
    
    commit_files: set of file/directory paths that should exist
    """
    current_files = get_all_files_and_dirs()
    # Convert commit_files list to set for faster lookup
    commit_files_set = set(commit_files)

    # Calculate the difference: files/dirs to remove
    to_remove = current_files - commit_files_set

    # Remove files and directories
    for path in sorted(to_remove, reverse=True):
        # reverse sort to remove files before directories
        full_path = os.path.join(".", path)
        if os.path.isfile(full_path):
            os.remove(full_path)
            print(f"Removed file: {full_path}")
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path)
            print(f"Removed directory: {full_path}")

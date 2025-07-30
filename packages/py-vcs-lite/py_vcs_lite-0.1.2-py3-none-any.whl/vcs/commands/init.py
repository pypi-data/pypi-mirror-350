import os


def init(PATH=os.getcwd()):
    current_dir = os.getcwd()
    dirs=(os.listdir(current_dir))
    if ".vcs" in dirs:
        print("[!] Version control system already initialized in this directory.")
        return
    print(f"[✓] Initialized version control system at {PATH}")
    main_folder = ".vcs"
    subfolders = ["objects", "commits"]
    files = ["index", "HEAD", "config", "logs"]
    os.makedirs(main_folder, exist_ok=True)
    for folder in subfolders:
        os.makedirs(os.path.join(main_folder, folder), exist_ok=True)
    for file in files:
        with open(os.path.join(main_folder, file), 'w') as f:
            f.write("")
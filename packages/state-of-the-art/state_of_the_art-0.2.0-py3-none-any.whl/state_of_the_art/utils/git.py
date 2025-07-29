import os


def get_commit_hash():
    home = os.path.expanduser("~")
    with open(f"{home}/.commit_hash", "r") as f:
        return f.read().strip()

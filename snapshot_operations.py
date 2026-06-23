import json
from snapshot import Snapshot

def load_snapshots(filename):
    try:
        with open(filename, "r") as file:
            snapshots_data = json.load(file)
            snapshots = [Snapshot(**snapshot) for snapshot in snapshots_data]
            return snapshots
    except(json.JSONDecodeError, FileNotFoundError):
        return []


def save_snapshots(snapshots, filename):
    try:
        with open(filename, "w") as file:
            snapshots_data = [snapshot.__dict__ for snapshot in snapshots]
            json.dump(snapshots_data, file, indent=4)
    except IOError as e:
        print(f"Error saving snapshots: {e}")
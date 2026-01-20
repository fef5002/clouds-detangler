"""Scaffold for building a dedupe index from manifests.

Planned behaviour (not fully implemented yet):

- Read all JSON manifest files from the manifests directory
- Normalise them into a single DuckDB table called `files`
  with columns like:
    remote, path, name, size, hash_md5, modified_time, id (fileId), mimeType

- Optionally, create summary views:
    - duplicates by hash
    - counts by extension
    - counts by remote

For now, this script only prints which manifest files it found.
"""

from pathlib import Path
from utils import get_paths_config

def main():
    paths_cfg = get_paths_config()
    manifests_dir = Path(paths_cfg.get("manifests_dir", "./manifests"))
    if not manifests_dir.exists():
        print(f"[!] Manifests directory does not exist yet: {manifests_dir}")
        print("    Run scripts/gather_metadata.py first.")
        return

    json_files = sorted(manifests_dir.glob("*.json"))
    if not json_files:
        print(f"[!] No JSON manifest files found in {manifests_dir}.")
        print("    Run scripts/gather_metadata.py first.")
        return

    print("Found the following manifest files:")
    for jf in json_files:
        print(f" - {jf.name}")

    print("\nNext steps (to be implemented):")
    print(" - Load these into DuckDB or another database")
    print(" - Build a unified `files` table")
    print(" - Compute duplicate groups by hash")

if __name__ == "__main__":
    main()

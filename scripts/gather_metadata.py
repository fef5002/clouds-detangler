"""Gather metadata from configured clouds using rclone.

This script:
- Reads config/clouds.yaml to find rclone remotes
- Reads config/paths.yaml to find the manifests directory
- Runs `rclone lsjson` for each cloud, with --recursive and --hash
- Stores the result as <remote>.json inside the manifests directory

It does NOT download file contents or change anything in your clouds.
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

from utils import (
    get_clouds_config,
    get_paths_config,
    check_prerequisites,
    ensure_directory,
)
from debug_utils import setup_logger, enable_debug_mode


def run_lsjson(remote: str, root: str, include_shared: bool, out_path: Path, log=None) -> bool:
    """Run rclone lsjson and save output to file.
    
    Args:
        remote: Name of the rclone remote
        root: Root path within the remote (empty string for root)
        include_shared: Whether to include shared files (Google Drive)
        out_path: Path to save the JSON output
        
    Returns:
        True if successful, False otherwise
    """
    if log:
        log.log_function_entry('run_lsjson', remote=remote, root=root, include_shared=include_shared)
    
    cmd = [
        "rclone", "lsjson",
        f"{remote}:{root}",
        "--recursive",
        "--hash",
    ]

    # For Google Drive, this flag includes "Shared with me" files
    if include_shared:
        cmd.append("--drive-shared-with-me")

    print(f"[{datetime.now().isoformat(timespec='seconds')}] Running: {' '.join(cmd)}")
    if log:
        log.debug(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if log:
            log.debug(f"Return code: {result.returncode}")
    except subprocess.TimeoutExpired:
        print(f"[!] TIMEOUT: rclone lsjson took longer than 5 minutes for '{remote}'")
        print(f"    This might mean you have a very large cloud.")
        print(f"    Consider using the 'root' parameter to scan specific folders.")
        return False
    except Exception as e:
        print(f"[!] ERROR running rclone lsjson: {e}")
        return False

    if result.returncode != 0:
        print(f"[!] rclone lsjson failed for remote '{remote}'.")
        print("stderr:")
        print(result.stderr)
        print("\nPossible causes:")
        print(f"  - OAuth token expired (run: rclone config reconnect {remote}:)")
        print("  - Network connectivity issue")
        print("  - Remote name doesn't exist (run: rclone listremotes)")
        return False

    out_path.write_text(result.stdout, encoding="utf-8")
    print(f"[+] Wrote manifest for {remote} to {out_path}")
    return True


def main():
    # Set up logging
    debug = enable_debug_mode()
    log = setup_logger('gather_metadata', debug=debug)
    
    print("=" * 70)
    print("Clouds Detangler - Metadata Gathering")
    print("=" * 70)
    print()
    
    log.info("Starting metadata gathering")
    
    # Check prerequisites
    if not check_prerequisites(verbose=True):
        print("\n[!] Prerequisites check failed. Fix the issues above and try again.")
        print("    Tip: Run 'python scripts/validate_setup.py' for detailed checks.")
        log.error("Prerequisites check failed")
        return 1
    
    print("[+] Prerequisites OK\n")
    log.info("Prerequisites check passed")
    
    # Load configs
    try:
        clouds_cfg = get_clouds_config()
        paths_cfg = get_paths_config()
        log.debug(f"Loaded configuration for {len(clouds_cfg.get('clouds', []))} clouds")
    except Exception as e:
        print(f"[!] ERROR loading configuration: {e}")
        log.exception("Failed to load configuration")
        return 1

    # Ensure manifests directory exists
    manifests_dir = ensure_directory(
        paths_cfg.get("manifests_dir", "./manifests"),
        "manifests"
    )
    print(f"[+] Manifests will be saved to: {manifests_dir.absolute()}\n")
    log.info(f"Manifests directory: {manifests_dir.absolute()}")

    clouds = clouds_cfg.get("clouds", [])
    if not clouds:
        print("[!] No clouds configured in config/clouds.yaml")
        print("    Edit the file and add at least one cloud.")
        log.error("No clouds configured")
        return 1
    
    print(f"[+] Found {len(clouds)} cloud(s) to scan\n")
    log.info(f"Processing {len(clouds)} clouds")

    # Process each cloud
    success_count = 0
    fail_count = 0
    
    for idx, cloud in enumerate(clouds, 1):
        remote = cloud["rclone_remote"]
        root = cloud.get("root", "")
        include_shared = bool(cloud.get("include_shared", False))
        name = cloud.get("name", remote)

        log.info(f"Processing cloud {idx}/{len(clouds)}: {name}")
        log.log_variable('remote', remote)
        log.log_variable('root', root)
        log.log_variable('include_shared', include_shared)

        out_path = manifests_dir / f"{remote}.json"
        print(f"{'=' * 70}")
        print(f"Cloud: {name}")
        print(f"{'=' * 70}")
        
        if run_lsjson(remote, root, include_shared, out_path, log=log):
            success_count += 1
            log.info(f"Successfully gathered metadata for {name}")
        else:
            fail_count += 1
            log.error(f"Failed to gather metadata for {name}")
        
        print()  # Blank line between clouds

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"✓ Successful: {success_count}")
    if fail_count > 0:
        print(f"✗ Failed: {fail_count}")
    print(f"\nManifests saved to: {manifests_dir.absolute()}")
    print("=" * 70)
    
    log.info(f"Completed: {success_count} successful, {fail_count} failed")
    log.print_log_location()
    
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

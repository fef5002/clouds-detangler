"""Validate prerequisites and configuration for Clouds Detangler.

Run this script to check that everything is set up correctly before
running gather_metadata.py or other scripts.
"""

import sys
from pathlib import Path

# Add scripts directory to path so we can import utils
sys.path.insert(0, str(Path(__file__).parent))

from utils import (
    check_prerequisites,
    validate_rclone_available,
    get_clouds_config,
    get_paths_config,
)
import subprocess


def check_rclone_remotes():
    """Verify that rclone remotes from config actually exist."""
    print("\n=== Checking rclone remotes ===")
    
    try:
        clouds_config = get_clouds_config()
    except Exception as e:
        print(f"[!] ERROR loading clouds config: {e}")
        return False
    
    clouds = clouds_config.get("clouds", [])
    if not clouds:
        print("[!] No clouds configured in config/clouds.yaml")
        return False
    
    # Get list of actual rclone remotes
    try:
        result = subprocess.run(
            ["rclone", "listremotes"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            print(f"[!] ERROR: rclone listremotes failed")
            print(f"    {result.stderr}")
            return False
        
        actual_remotes = set(
            line.strip().rstrip(':') 
            for line in result.stdout.strip().split('\n') 
            if line.strip()
        )
        
    except Exception as e:
        print(f"[!] ERROR checking rclone remotes: {e}")
        return False
    
    print(f"[+] Found {len(actual_remotes)} rclone remote(s):")
    for remote in sorted(actual_remotes):
        print(f"    - {remote}")
    
    # Check each configured cloud
    all_ok = True
    print(f"\n[+] Checking {len(clouds)} configured cloud(s):")
    
    for idx, cloud in enumerate(clouds):
        name = cloud.get("name", f"Cloud {idx}")
        remote = cloud.get("rclone_remote")
        
        if remote in actual_remotes:
            print(f"    ✓ {name} (remote: {remote})")
        else:
            print(f"    ✗ {name} (remote: {remote}) - NOT FOUND")
            print(f"      Run: rclone config")
            all_ok = False
    
    return all_ok


def test_rclone_access():
    """Test that we can actually access at least one remote."""
    print("\n=== Testing rclone access ===")
    
    try:
        clouds_config = get_clouds_config()
        clouds = clouds_config.get("clouds", [])
        
        if not clouds:
            return True  # Skip test if no clouds configured
        
        # Try the first cloud
        cloud = clouds[0]
        remote = cloud.get("rclone_remote")
        root = cloud.get("root", "")
        name = cloud.get("name", remote)
        
        print(f"[+] Testing access to: {name}")
        print(f"    Running: rclone lsf {remote}:{root} --max-depth 1")
        
        result = subprocess.run(
            ["rclone", "lsf", f"{remote}:{root}", "--max-depth", "1"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"[!] ERROR: Could not list files")
            print(f"    {result.stderr}")
            print(f"\n    This might mean:")
            print(f"    - OAuth token expired (run: rclone config reconnect {remote}:)")
            print(f"    - Network issue")
            print(f"    - Incorrect remote configuration")
            return False
        
        lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
        print(f"[+] SUCCESS: Found {len(lines)} items in {name}")
        if lines:
            print(f"    First few items:")
            for line in lines[:3]:
                print(f"      - {line}")
        
        return True
        
    except subprocess.TimeoutExpired:
        print(f"[!] ERROR: Connection timed out")
        print(f"    Check your internet connection")
        return False
    except Exception as e:
        print(f"[!] ERROR testing rclone access: {e}")
        return False


def main():
    print("=" * 60)
    print("Clouds Detangler - Configuration Validator")
    print("=" * 60)
    
    all_checks = []
    
    # Check prerequisites
    print("\n=== Checking prerequisites ===")
    prereq_ok = check_prerequisites(verbose=True)
    all_checks.append(("Prerequisites", prereq_ok))
    
    if not prereq_ok:
        print("\n" + "=" * 60)
        print("FAILED: Fix the issues above before continuing")
        print("=" * 60)
        return 1
    
    # Check remotes
    remotes_ok = check_rclone_remotes()
    all_checks.append(("Remote configuration", remotes_ok))
    
    # Test access
    if remotes_ok:
        access_ok = test_rclone_access()
        all_checks.append(("Remote access", access_ok))
    
    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    for check_name, passed in all_checks:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {check_name}")
    
    all_passed = all(passed for _, passed in all_checks)
    
    print("=" * 60)
    if all_passed:
        print("✓ ALL CHECKS PASSED")
        print("\nYou're ready to run:")
        print("  python scripts/gather_metadata.py")
    else:
        print("✗ SOME CHECKS FAILED")
        print("\nFix the issues above before running gather_metadata.py")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Simple test script to verify cloud detection without scanning files
"""

import sys
from pathlib import Path

# Import from main module
sys.path.insert(0, str(Path(__file__).parent))
from clouds_detangler import CloudDetector, CloudWarnings


def main():
    print("Cloud Detangler - Quick Test")
    print("-" * 50)
    
    # Show warnings
    CloudWarnings.display_cloud_sync_warning()
    
    # Detect cloud directories
    detector = CloudDetector()
    cloud_dirs = detector.detect_cloud_directories()
    
    if not cloud_dirs:
        print("✗ No cloud storage directories detected on this system.")
        print("\nThis tool looks for:")
        print("  - Google Drive")
        print("  - OneDrive")
        print("  - iCloud Drive")
        print("  - Dropbox")
        return
    
    print("✓ Detected cloud storage directories:\n")
    for provider, dirs in cloud_dirs.items():
        print(f"{provider.upper()}:")
        for directory in dirs:
            exists = "✓" if directory.exists() else "✗"
            print(f"  {exists} {directory}")
    
    # Test if a path is in cloud storage
    print("\n" + "-" * 50)
    print("Test: Is path in cloud storage?")
    
    test_paths = [
        Path.home() / "Documents",
        Path.home() / "Google Drive",
        Path.home() / "OneDrive",
    ]
    
    for test_path in test_paths:
        is_cloud, provider = detector.is_cloud_directory(test_path)
        if is_cloud:
            print(f"✓ {test_path} -> YES (in {provider})")
        else:
            print(f"  {test_path} -> No")


if __name__ == '__main__':
    main()

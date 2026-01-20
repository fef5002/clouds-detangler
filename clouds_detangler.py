#!/usr/bin/env python3
"""
Clouds Detangler - A tool to help manage multiple cloud storage accounts

This tool helps users who have multiple cloud accounts (Google Drive, OneDrive, iCloud)
understand that:
1. The same file existing in different clouds is NOT the same file
2. Cloud hosting sites should not be hooked up to one another
3. Locally mapped cloud directories are synchronized with the cloud
4. Deleting from a local cloud directory deletes from the cloud
"""

import os
import sys
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class CloudFile:
    """Represents a file in cloud storage"""
    path: str
    size: int
    hash: str
    cloud_provider: str
    last_modified: str
    
    
@dataclass
class DuplicateGroup:
    """Represents a group of duplicate files across cloud providers"""
    hash: str
    size: int
    files: List[CloudFile]
    total_waste: int  # Total wasted storage in bytes
    

class CloudDetector:
    """Detects cloud storage directories on the local system"""
    
    CLOUD_PATTERNS = {
        'google_drive': [
            'Google Drive',
            'GoogleDrive',
            'gdrive'
        ],
        'onedrive': [
            'OneDrive',
            'OneDrive - Personal',
            'OneDrive - Business'
        ],
        'icloud': [
            'iCloud Drive',
            'iCloudDrive',
            'Library/Mobile Documents/com~apple~CloudDocs'
        ],
        'dropbox': [
            'Dropbox'
        ]
    }
    
    def __init__(self):
        self.home = Path.home()
        
    def detect_cloud_directories(self) -> Dict[str, List[Path]]:
        """Detect all cloud storage directories on the system"""
        detected = {}
        
        for provider, patterns in self.CLOUD_PATTERNS.items():
            detected[provider] = []
            for pattern in patterns:
                # Check in home directory
                cloud_path = self.home / pattern
                if cloud_path.exists() and cloud_path.is_dir():
                    detected[provider].append(cloud_path)
                    
                # Check in common locations (macOS)
                if sys.platform == 'darwin':
                    mac_path = self.home / 'Library' / 'CloudStorage' / pattern
                    if mac_path.exists() and mac_path.is_dir():
                        detected[provider].append(mac_path)
        
        return {k: v for k, v in detected.items() if v}
    
    def is_cloud_directory(self, path: Path) -> Tuple[bool, str]:
        """Check if a path is within a cloud storage directory"""
        path = Path(path).resolve()
        
        detected = self.detect_cloud_directories()
        for provider, directories in detected.items():
            for cloud_dir in directories:
                try:
                    path.relative_to(cloud_dir)
                    return True, provider
                except ValueError:
                    continue
        
        return False, ""


class FileScanner:
    """Scans files and computes hashes for deduplication"""
    
    def __init__(self, chunk_size: int = 8192):
        self.chunk_size = chunk_size
    
    def compute_file_hash(self, file_path: Path) -> str:
        """Compute SHA256 hash of a file"""
        sha256 = hashlib.sha256()
        
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(self.chunk_size)
                while chunk:
                    sha256.update(chunk)
                    chunk = f.read(self.chunk_size)
            return sha256.hexdigest()
        except (IOError, PermissionError) as e:
            print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
            return ""
    
    def scan_directory(self, directory: Path, provider: str) -> List[CloudFile]:
        """Scan a directory and return list of CloudFile objects"""
        files = []
        
        if not directory.exists():
            return files
        
        for item in directory.rglob('*'):
            if item.is_file():
                try:
                    stat = item.stat()
                    file_hash = self.compute_file_hash(item)
                    
                    if file_hash:
                        cloud_file = CloudFile(
                            path=str(item),
                            size=stat.st_size,
                            hash=file_hash,
                            cloud_provider=provider,
                            last_modified=datetime.fromtimestamp(stat.st_mtime).isoformat()
                        )
                        files.append(cloud_file)
                except (OSError, PermissionError) as e:
                    print(f"Warning: Could not process {item}: {e}", file=sys.stderr)
        
        return files


class DuplicateFinder:
    """Finds duplicate files across cloud providers"""
    
    def find_duplicates(self, files: List[CloudFile]) -> List[DuplicateGroup]:
        """Find duplicate files based on hash"""
        hash_map: Dict[str, List[CloudFile]] = {}
        
        # Group files by hash
        for file in files:
            if file.hash not in hash_map:
                hash_map[file.hash] = []
            hash_map[file.hash].append(file)
        
        # Find duplicates (files with same hash in different providers)
        duplicates = []
        for file_hash, file_list in hash_map.items():
            if len(file_list) > 1:
                # Check if files are in different cloud providers
                providers = set(f.cloud_provider for f in file_list)
                if len(providers) > 1:
                    total_waste = file_list[0].size * (len(file_list) - 1)
                    duplicate_group = DuplicateGroup(
                        hash=file_hash,
                        size=file_list[0].size,
                        files=file_list,
                        total_waste=total_waste
                    )
                    duplicates.append(duplicate_group)
        
        return duplicates


class ManifestGenerator:
    """Generates manifest files for tracking cloud files"""
    
    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path.cwd()
    
    def generate_manifest(self, files: List[CloudFile], duplicates: List[DuplicateGroup]) -> str:
        """Generate a JSON manifest of all files and duplicates"""
        manifest = {
            'generated_at': datetime.now().isoformat(),
            'total_files': len(files),
            'total_duplicates': len(duplicates),
            'files': [asdict(f) for f in files],
            'duplicates': [
                {
                    'hash': d.hash,
                    'size': d.size,
                    'total_waste': d.total_waste,
                    'files': [asdict(f) for f in d.files]
                }
                for d in duplicates
            ],
            'summary': self._generate_summary(files, duplicates)
        }
        
        return json.dumps(manifest, indent=2)
    
    def _generate_summary(self, files: List[CloudFile], duplicates: List[DuplicateGroup]) -> Dict:
        """Generate summary statistics"""
        total_size = sum(f.size for f in files)
        total_waste = sum(d.total_waste for d in duplicates)
        
        provider_counts = {}
        for file in files:
            provider = file.cloud_provider
            if provider not in provider_counts:
                provider_counts[provider] = 0
            provider_counts[provider] += 1
        
        return {
            'total_size_bytes': total_size,
            'total_size_gb': round(total_size / (1024**3), 2),
            'total_waste_bytes': total_waste,
            'total_waste_gb': round(total_waste / (1024**3), 2),
            'files_per_provider': provider_counts,
            'duplicate_groups': len(duplicates)
        }
    
    def save_manifest(self, manifest_json: str, filename: str = 'cloud_manifest.json'):
        """Save manifest to file"""
        output_path = self.output_dir / filename
        with open(output_path, 'w') as f:
            f.write(manifest_json)
        return output_path


class CloudWarnings:
    """Provides warnings about cloud directory operations"""
    
    @staticmethod
    def display_cloud_sync_warning():
        """Display warning about cloud synchronization"""
        print("\n" + "="*80)
        print("⚠️  CRITICAL WARNING: CLOUD STORAGE SYNCHRONIZATION ⚠️")
        print("="*80)
        print("""
This tool has detected cloud storage directories on your system.

IMPORTANT THINGS TO UNDERSTAND:

1. FILES IN DIFFERENT CLOUDS ARE SEPARATE FILES
   - A file in Google Drive is NOT the same as a file in OneDrive
   - Even if they have the same name and content, they are SEPARATE files
   - Changes to one do NOT affect the other (unless you've set up sync)

2. DO NOT HOOK CLOUD SERVICES TO EACH OTHER
   - Connecting Google Drive to sync with OneDrive creates confusion
   - This often leads to duplicate files and sync conflicts
   - Each cloud service should be independent

3. LOCALLY MAPPED DIRECTORIES ARE SYNCHRONIZED
   - Files you see locally in cloud folders are YOUR ACTUAL CLOUD FILES
   - These directories are NOT just local copies
   - They are synchronized with the cloud in real-time

4. DELETING FROM LOCAL CLOUD FOLDERS DELETES FROM THE CLOUD
   - If you delete a file from your local OneDrive folder, it's deleted from OneDrive
   - If you delete from your local Google Drive folder, it's deleted from Google Drive
   - These deletions are PERMANENT (subject to cloud provider's trash policies)

5. CLOUD STORAGE IS NOT A BACKUP SERVICE
   - If you delete a file locally, it's deleted from the cloud
   - You need a separate backup solution
   - Don't rely on multiple clouds as "backups" - use proper backup tools

RECOMMENDATION:
- Choose ONE primary cloud service for each type of data
- Use this tool to identify and remove duplicates
- Set up proper backups separate from cloud sync
""")
        print("="*80 + "\n")


def main():
    """Main entry point"""
    print("Clouds Detangler - Cloud Storage Management Tool")
    print("-" * 50)
    
    # Show warnings
    CloudWarnings.display_cloud_sync_warning()
    
    # Detect cloud directories
    detector = CloudDetector()
    cloud_dirs = detector.detect_cloud_directories()
    
    if not cloud_dirs:
        print("No cloud storage directories detected on this system.")
        print("This tool looks for: Google Drive, OneDrive, iCloud Drive, Dropbox")
        return
    
    print(f"\nDetected cloud storage directories:")
    for provider, dirs in cloud_dirs.items():
        print(f"\n{provider.upper()}:")
        for directory in dirs:
            print(f"  - {directory}")
    
    # Ask user for confirmation
    print("\n" + "-" * 50)
    response = input("\nWould you like to scan these directories for duplicates? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("Scan cancelled.")
        return
    
    # Scan directories
    print("\nScanning files...")
    scanner = FileScanner()
    all_files = []
    
    for provider, dirs in cloud_dirs.items():
        for directory in dirs:
            print(f"  Scanning {provider}: {directory}")
            files = scanner.scan_directory(directory, provider)
            all_files.extend(files)
            print(f"    Found {len(files)} files")
    
    print(f"\nTotal files scanned: {len(all_files)}")
    
    # Find duplicates
    print("\nFinding duplicates across cloud providers...")
    finder = DuplicateFinder()
    duplicates = finder.find_duplicates(all_files)
    
    print(f"Found {len(duplicates)} groups of duplicate files")
    
    if duplicates:
        total_waste = sum(d.total_waste for d in duplicates)
        print(f"Total wasted storage: {total_waste / (1024**3):.2f} GB")
        
        print("\nTop 10 duplicate groups by wasted space:")
        sorted_dupes = sorted(duplicates, key=lambda d: d.total_waste, reverse=True)[:10]
        
        for i, dupe in enumerate(sorted_dupes, 1):
            print(f"\n{i}. Size: {dupe.size / (1024**2):.2f} MB, "
                  f"Copies: {len(dupe.files)}, "
                  f"Waste: {dupe.total_waste / (1024**2):.2f} MB")
            for file in dupe.files:
                print(f"   - [{file.cloud_provider}] {file.path}")
    
    # Generate manifest
    print("\nGenerating manifest...")
    manifest_gen = ManifestGenerator()
    manifest_json = manifest_gen.generate_manifest(all_files, duplicates)
    manifest_path = manifest_gen.save_manifest(manifest_json)
    print(f"Manifest saved to: {manifest_path}")
    
    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("="*80)
    print("""
1. Review the manifest file to see all duplicates
2. Decide which cloud provider should be your primary storage for each file
3. Use the manifest to identify files that can be safely deleted
4. Consider using rclone to manage cloud storage more efficiently
5. Set up a proper backup strategy separate from cloud sync

Remember: Deleting from your local cloud folder deletes from the cloud!
""")


if __name__ == '__main__':
    main()

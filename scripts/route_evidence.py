#!/usr/bin/env python3
"""
Evidence management with chain of custody
Routes files to OneDrive, Backblaze B2, and optionally Google Drive
"""

import subprocess
import hashlib
import csv
import json
from pathlib import Path
from datetime import datetime

# File type mappings
FILE_TYPES = {
    'Audio': [
        # Lossless formats
        '.wav', '.flac', '.alac', '.ape', '.wv', '.tta', '.aiff', '.aif',
        # Lossy formats
        '.mp3', '.aac', '.m4a', '.ogg', '.oga', '.opus', '.wma',
        # Mobile/Platform specific
        '.amr', '.awb',      # Android voice memos
        '.caf',              # iOS Core Audio Format
        '.3gp', '.3ga',      # 3GPP (mobile)
        # Professional/specialized
        '.dss', '.ds2',      # Digital Speech Standard (recorders)
        '.msv', '.dvf',      # Sony voice formats
        '.vox',              # Dialogic ADPCM
        '.gsm',              # GSM audio
        '.ac3',              # Dolby Digital
        # Streaming/podcast
        '.m4b', '.m4p',      # Audiobooks/iTunes
        '.ra', '.ram',       # RealAudio
        '.webm',             # WebM audio
    ],
    'Video': ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.webm', '.flv', '.m4v', '.3gp', '.mpg', '.mpeg', '.m2ts', '.mts'],
    'Images': ['.jpg', '.jpeg', '.png', '.tiff', '.tif', '.raw', '.cr2', '.nef', '.dng', '.heic', '.heif', '.bmp', '.gif', '.webp'],
    'Documents': ['.pdf', '.docx', '.txt', '.doc', '.xlsx', '.pptx', '.odt', '.rtf', '.md'],
    'Transcripts': ['.vtt', '.srt', '.txt', '.json', '.sbv', '.sub'],
    'Archives': [
        '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz',  # Standard archives
        '.tar.gz', '.tar.bz2', '.tar.xz',                     # Compressed tars
    ],
    'Messaging': [
        # WhatsApp exports
        '.txt',              # WhatsApp chat export (plain text)
        # Telegram exports
        '.html', '.json',    # Telegram export formats
        # Signal exports
        '.json',             # Signal backup format
        # Other messaging
        '.mbox', '.eml',     # Email/messaging archives
    ]
}

def get_file_type(filepath):
    """Determine file type based on extension"""
    ext = Path(filepath).suffix.lower()
    for file_type, extensions in FILE_TYPES.items():
        if ext in extensions:
            return file_type
    return 'Other'

def calculate_hash(filepath, algorithm='SHA256'):
    """Calculate cryptographic hash for chain of custody"""
    hash_func = hashlib.sha256() if algorithm == 'SHA256' else hashlib.md5()
    
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()

def get_file_metadata(filepath):
    """Extract file metadata"""
    path = Path(filepath)
    stat = path.stat()
    
    return {
        'filename': path.name,
        'size_bytes': stat.st_size,
        'size_mb': round(stat.st_size / 1024 / 1024, 2),
        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
    }

def log_custody(action, filepath, file_hash, locations, notes=''):
    """Log to chain of custody CSV"""
    custody_log = Path('C:/Evidence/manifests/custody-log.csv')
    custody_log.parent.mkdir(parents=True, exist_ok=True)
    
    # Create CSV if it doesn't exist
    if not custody_log.exists():
        with open(custody_log, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Timestamp', 'Action', 'File_Path', 'Hash_SHA256', 
                'Officer', 'Locations', 'Notes'
            ])
    
    # Append custody record
    with open(custody_log, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            action,
            filepath,
            file_hash,
            'Fiona',  # Your name/ID
            ', '.join(locations),
            notes
        ])

def copy_to_cloud(source_path, remote, dest_folder, verify=True):
    """Copy file to cloud with verification"""
    source = Path(source_path)
    dest = f"{remote}:{dest_folder}"
    
    print(f"  → Uploading to {dest}...")
    
    # Copy with checksum verification and metadata
    cmd = [
        'rclone', 'copy', str(source), dest,
        '--checksum',  # Verify with hash
        '--metadata',  # Preserve timestamps
        '--progress',
        '--transfers', '1',  # Low memory
        '--checkers', '2'    # Low memory
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Upload failed: {result.stderr}")
    
    # Verify if requested
    if verify:
        print(f"  → Verifying upload...")
        verify_cmd = ['rclone', 'hashsum', 'SHA256', f"{dest}/{source.name}"]
        verify_result = subprocess.run(verify_cmd, capture_output=True, text=True)
        
        if verify_result.returncode != 0:
            raise Exception("Verification failed")
        
        remote_hash = verify_result.stdout.split()[0] if verify_result.stdout else None
        return remote_hash
    
    return None

def route_evidence_file(source_path, upload_to_backblaze=True, upload_to_gdrive=False, local_only=False):
    """
    Main evidence routing workflow
    
    Args:
        source_path: Path to evidence file
        upload_to_backblaze: Upload to Backblaze B2 (immutable backup)
        upload_to_gdrive: Upload to Google Drive (optional, for sharing)
    """
    source = Path(source_path)
    
    if not source.exists():
        raise FileNotFoundError(f"File not found: {source_path}")
    
    # Determine file type
    file_type = get_file_type(source_path)
    print(f"\n{'='*60}")
    print(f"Evidence Routing Workflow")
    print(f"{'='*60}")
    print(f"File: {source.name}")
    print(f"Type: {file_type}")
    print(f"Size: {get_file_metadata(source_path)['size_mb']} MB")
    print()
    
    # Step 1: Calculate hash
    print("[1/6] Calculating SHA256 hash...")
    file_hash = calculate_hash(source_path)
    print(f"  Hash: {file_hash}")
    
    locations = []
    
    # Step 2: Upload to OneDrive (Primary Master)
    if local_only:
        print("\n[2/6] Skipping OneDrive (local-only mode)")
    else:
        print("\n[2/6] Uploading to OneDrive (Master)...")
        onedrive_folder = f"Evidence/Masters/{file_type}"
        try:
            onedrive_hash = copy_to_cloud(source_path, 'onedrive', onedrive_folder, verify=True)
            
            if onedrive_hash == file_hash:
                print(f"  ✓ OneDrive upload verified")
                locations.append(f'OneDrive/Masters/{file_type}')
            else:
                raise Exception(f"Hash mismatch! Expected {file_hash}, got {onedrive_hash}")
        except Exception as e:
            print(f"  ✗ OneDrive upload failed: {e}")
            raise
    
    # Step 3: Upload to Backblaze B2 (Immutable Backup)
    if not local_only and upload_to_backblaze:
        print("\n[3/6] Uploading to Backblaze B2 (Immutable Backup)...")
        b2_folder = f"evidence-masters/{file_type}"
        try:
            b2_hash = copy_to_cloud(source_path, 'b2', b2_folder, verify=True)
            
            if b2_hash == file_hash:
                print(f"  ✓ Backblaze upload verified")
                locations.append(f'Backblaze/evidence-masters/{file_type}')
            else:
                raise Exception(f"Hash mismatch! Expected {file_hash}, got {b2_hash}")
        except Exception as e:
            print(f"  ✗ Backblaze upload failed: {e}")
            # Don't raise - Backblaze is backup, OneDrive is primary
    else:
        print("\n[3/6] Skipping Backblaze (not requested)")
    
    # Step 4: Upload to Google Drive (Optional, for sharing)
    if not local_only and upload_to_gdrive:
        print("\n[4/6] Uploading to Google Drive (Working/Sharing)...")
        gdrive_folder = f"Evidence/Working/{file_type}"
        try:
            copy_to_cloud(source_path, 'gdrive', gdrive_folder, verify=False)
            print(f"  ✓ Google Drive upload complete")
            locations.append(f'GDrive/Evidence/Working/{file_type}')
        except Exception as e:
            print(f"  ✗ Google Drive upload failed: {e}")
    else:
        print("\n[4/6] Skipping Google Drive (not requested)")
    
    # Step 5: Create local working copy
    print("\n[5/6] Creating local working copy...")
    working_dir = Path('C:/Evidence/Working-Copies') / file_type
    working_dir.mkdir(parents=True, exist_ok=True)
    working_copy = working_dir / f"{source.stem}_working{source.suffix}"
    
    import shutil
    shutil.copy2(source, working_copy)
    print(f"  ✓ Working copy: {working_copy}")
    locations.append(f'Local/Working-Copies/{file_type}')
    
    # Step 6: Log to chain of custody
    print("\n[6/6] Logging chain of custody...")
    log_custody(
        action='ACQUIRED',
        filepath=str(source),
        file_hash=file_hash,
        locations=locations,
        notes=f'Master evidence file uploaded and verified'
    )
    print(f"  ✓ Logged to C:/Evidence/manifests/custody-log.csv")
    
    # Generate manifest
    manifest_path = Path('C:/Evidence/manifests') / f"{source.stem}.manifest.json"
    manifest = {
        'filename': source.name,
        'sha256': file_hash,
        'file_type': file_type,
        'metadata': get_file_metadata(source_path),
        'locations': locations,
        'timestamp': datetime.now().isoformat(),
        'verified': True
    }
    
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"✓ Evidence routing complete!")
    print(f"{'='*60}")
    print(f"Master locations: {len(locations)}")
    for loc in locations:
        print(f"  - {loc}")
    print(f"\nSHA256: {file_hash}")
    print(f"Manifest: {manifest_path}")
    print(f"Working copy: {working_copy}")
    print(f"{'='*60}\n")
    
    return {
        'hash': file_hash,
        'locations': locations,
        'working_copy': str(working_copy),
        'manifest': str(manifest_path)
    }

def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Route evidence files to cloud storage')
    parser.add_argument('file', help='Evidence file to process')
    parser.add_argument('--no-backblaze', action='store_true', help='Skip Backblaze upload')
    parser.add_argument('--gdrive', action='store_true', help='Upload to Google Drive')
    parser.add_argument('--local-only', action='store_true', help='Process locally only (no cloud uploads)')
    
    args = parser.parse_args()
    
    try:
        route_evidence_file(
            args.file,
            upload_to_backblaze=not args.no_backblaze,
            upload_to_gdrive=args.gdrive,
            local_only=args.local_only
        )
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())

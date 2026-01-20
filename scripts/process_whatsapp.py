#!/usr/bin/env python3
"""
Process WhatsApp exports for evidence management
Extracts zip files and routes media/chat files appropriately
"""

import zipfile
import shutil
from pathlib import Path
import route_evidence
import re

def is_whatsapp_export(zip_path):
    """Check if zip file is a WhatsApp export"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            files = zf.namelist()
            # WhatsApp exports contain _chat.txt or similar
            return any('chat.txt' in f.lower() for f in files)
    except:
        return False

def sanitize_filename(filename):
    """Sanitize WhatsApp export folder name"""
    # Remove special chars, spaces
    name = re.sub(r'[^\w\s-]', '', filename)
    name = re.sub(r'\s+', '_', name)
    return name

def extract_whatsapp_export(zip_path, extract_dir):
    """Extract WhatsApp export zip file"""
    zip_file = Path(zip_path)
    
    # Create extraction directory
    folder_name = sanitize_filename(zip_file.stem)
    output_dir = Path(extract_dir) / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Extracting WhatsApp export to: {output_dir}")
    
    # Extract all files
    with zipfile.ZipFile(zip_file, 'r') as zf:
        zf.extractall(output_dir)
    
    return output_dir

def categorize_whatsapp_files(extract_dir):
    """Categorize extracted WhatsApp files by type"""
    files_by_type = {
        'chat': [],
        'audio': [],
        'video': [],
        'images': [],
        'documents': []
    }
    
    for file_path in Path(extract_dir).rglob('*'):
        if not file_path.is_file():
            continue
        
        filename = file_path.name.lower()
        
        # Chat transcripts
        if 'chat.txt' in filename or filename.endswith('.txt'):
            files_by_type['chat'].append(file_path)
        
        # Voice messages and audio
        elif any(ext in filename for ext in ['.opus', '.m4a', '.mp3', '.aac', '.ogg']):
            files_by_type['audio'].append(file_path)
        
        # Videos
        elif any(ext in filename for ext in ['.mp4', '.3gp', '.mov', '.mkv']):
            files_by_type['video'].append(file_path)
        
        # Images
        elif any(ext in filename for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.heic']):
            files_by_type['images'].append(file_path)
        
        # Documents
        elif any(ext in filename for ext in ['.pdf', '.docx', '.xlsx', '.txt', '.doc']):
            files_by_type['documents'].append(file_path)
    
    return files_by_type

def process_whatsapp_export(zip_path, upload_to_backblaze=True, upload_to_gdrive=False):
    """
    Full WhatsApp export processing workflow
    
    1. Route the original zip file to Archives
    2. Extract locally to working directory
    3. Process each media file individually
    4. Route chat transcript to Messaging folder
    """
    zip_file = Path(zip_path)
    
    print(f"\n{'='*60}")
    print(f"WhatsApp Export Processing")
    print(f"{'='*60}")
    print(f"File: {zip_file.name}")
    print()
    
    # Step 1: Verify it's a WhatsApp export
    if not is_whatsapp_export(zip_path):
        print("⚠ Warning: This doesn't appear to be a WhatsApp export")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Step 2: Route the original zip to Archives
    print("\n[1/4] Routing original zip to Archives...")
    try:
        result = route_evidence.route_evidence_file(
            str(zip_path),
            upload_to_backblaze=upload_to_backblaze,
            upload_to_gdrive=upload_to_gdrive
        )
        original_hash = result['hash']
    except Exception as e:
        print(f"✗ Failed to route zip file: {e}")
        return
    
    # Step 3: Extract to working directory
    print("\n[2/4] Extracting WhatsApp export...")
    extract_base = Path('C:/Evidence/Working-Copies/Archives-Extracted')
    extract_dir = extract_whatsapp_export(zip_path, extract_base)
    
    # Step 4: Categorize files
    print("\n[3/4] Categorizing extracted files...")
    categorized = categorize_whatsapp_files(extract_dir)
    
    total_files = sum(len(files) for files in categorized.values())
    print(f"Found {total_files} files:")
    for file_type, files in categorized.items():
        if files:
            print(f"  - {file_type.title()}: {len(files)}")
    
    # Step 5: Process each file individually
    print("\n[4/4] Processing extracted files...")
    processed = 0
    failed = 0
    
    for file_type, files in categorized.items():
        for file_path in files:
            print(f"\n  Processing {file_path.name}...")
            
            try:
                # Determine target type for routing
                if file_type == 'chat':
                    # Create a renamed copy for messaging folder
                    chat_copy = extract_dir / f"WhatsApp_{zip_file.stem}_chat.txt"
                    shutil.copy2(file_path, chat_copy)
                    
                    # Route to Messaging (using Documents type with manual override)
                    # We'll manually copy to Messaging folder
                    print(f"    → Chat transcript: {chat_copy.name}")
                    # You can manually route these or add 'Messaging' type to route_evidence.py
                    
                else:
                    # Route media files normally
                    route_evidence.route_evidence_file(
                        str(file_path),
                        upload_to_backblaze=upload_to_backblaze,
                        upload_to_gdrive=False  # Don't upload every media file to gdrive
                    )
                
                processed += 1
                
            except Exception as e:
                print(f"    ✗ Failed: {e}")
                failed += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"WhatsApp Processing Complete")
    print(f"{'='*60}")
    print(f"Original zip: {original_hash[:16]}...")
    print(f"Extracted to: {extract_dir}")
    print(f"Files processed: {processed}")
    print(f"Files failed: {failed}")
    print(f"{'='*60}\n")
    
    return {
        'zip_hash': original_hash,
        'extract_dir': str(extract_dir),
        'processed': processed,
        'failed': failed
    }

def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Process WhatsApp exports')
    parser.add_argument('zipfile', help='WhatsApp export zip file')
    parser.add_argument('--no-backblaze', action='store_true', help='Skip Backblaze upload')
    parser.add_argument('--gdrive', action='store_true', help='Upload to Google Drive')
    
    args = parser.parse_args()
    
    if not Path(args.zipfile).exists():
        print(f"Error: File not found: {args.zipfile}")
        return 1
    
    try:
        process_whatsapp_export(
            args.zipfile,
            upload_to_backblaze=not args.no_backblaze,
            upload_to_gdrive=args.gdrive
        )
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())

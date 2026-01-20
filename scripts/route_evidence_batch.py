#!/usr/bin/env python3
"""
Batch process files from staging directory and route to cloud storage
"""

from pathlib import Path
import route_file
import time

def process_staging_directory(staging_dir, upload_to_backblaze=True, upload_to_gdrive=False, local_only=False, max_files=None):
    """Process all files in staging directory"""
    staging_path = Path(staging_dir)
    
    if not staging_path.exists():
        print(f"Error: Staging directory not found: {staging_dir}")
        return
    
    print(f"\n{'='*60}")
    print(f"Batch Evidence Processing")
    print(f"{'='*60}")
    print(f"Staging directory: {staging_path}")
    
    # Find all files (not in Processed subdirectory)
    files = [f for f in staging_path.rglob('*') 
             if f.is_file() and 'Processed' not in f.parts]
    if max_files is not None:
        files = files[:max_files]
    
    print(f"Found {len(files)} files to process")
    print(f"{'='*60}\n")
    
    processed_count = 0
    failed_count = 0
    
    for i, file_path in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] Processing: {file_path.name}")
        
        try:
            # Route file to clouds
            result = route_file.route_file(
                str(file_path),
                upload_to_backblaze=upload_to_backblaze,
                upload_to_gdrive=upload_to_gdrive,
                local_only=local_only
            )
            
            # Move to processed folder
            processed_dir = staging_path / 'processed'
            processed_dir.mkdir(exist_ok=True)
            new_path = processed_dir / file_path.name
            file_path.rename(new_path)
            
            print(f"✓ Moved to: {new_path}")
            processed_count += 1
            
            # Pause between files (low memory system)
            if i < len(files):
                print(f"\nPausing 5 seconds before next file...")
                time.sleep(5)
            
        except Exception as e:
            print(f"✗ Error processing {file_path.name}: {e}")
            failed_count += 1
            
            # Move to failed folder
            failed_dir = staging_path / 'failed'
            failed_dir.mkdir(exist_ok=True)
            try:
                file_path.rename(failed_dir / file_path.name)
            except:
                pass
            
            continue
    
    print(f"\n{'='*60}")
    print(f"Batch Processing Complete")
    print(f"{'='*60}")
    print(f"Processed: {processed_count}")
    print(f"Failed: {failed_count}")
    print(f"Total: {len(files)}")
    print(f"{'='*60}\n")

def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Batch process files')
    parser.add_argument('staging_dir', help='Staging directory to process')
    parser.add_argument('--no-backblaze', action='store_true', help='Skip Backblaze upload')
    parser.add_argument('--gdrive', action='store_true', help='Upload to Google Drive')
    parser.add_argument('--local-only', action='store_true', help='Process locally only (no cloud uploads)')
    parser.add_argument('--max-files', type=int, default=None, help='Limit processing to first N files')
    
    args = parser.parse_args()
    
    process_staging_directory(
        args.staging_dir,
        upload_to_backblaze=not args.no_backblaze,
        upload_to_gdrive=args.gdrive,
        local_only=args.local_only,
        max_files=args.max_files
    )

if __name__ == '__main__':
    main()

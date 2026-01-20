# Clouds Detangler

A workflow tool to help users who have multiple cloud storage accounts (Google Drive, OneDrive, iCloud) understand and manage their cloud storage properly.

## The Problem This Solves

This tool is for people who:

- Have Apple, Google, and Microsoft accounts with cloud storage
- Think hooking up cloud hosting sites to one another is no big deal
- Don't realize that the same file existing in Google Drive, OneDrive, and iCloud is **NOT the same file**
- Treat cloud hosting sites as a backup service
- Are unaware that locally mapped cloud directories are synchronized with the cloud
- Don't realize that **deleting from a locally mapped location deletes the file from the cloud**

## What This Tool Does

### 1. Educational Warnings

The tool provides clear warnings about:
- How cloud synchronization actually works
- The danger of hooking multiple cloud services together
- That files in different clouds are separate, independent files
- That local cloud folders are NOT local copies - they're synchronized
- That deleting locally deletes from the cloud

### 2. Cloud Directory Detection

Automatically detects cloud storage directories on your system:
- Google Drive
- OneDrive (Personal and Business)
- iCloud Drive
- Dropbox

### 3. Duplicate File Detection

Scans your cloud directories and identifies:
- Files that exist in multiple cloud providers (duplicates)
- How much storage space is wasted on duplicates
- Which files are consuming the most duplicate storage

### 4. Manifest Generation

Creates a detailed JSON manifest containing:
- All files found in cloud directories
- File hashes, sizes, and locations
- Duplicate file groups
- Summary statistics
- Storage waste analysis

### 5. Workflow Guidance

Helps you:
- Unhook cloud hosting sites from one another
- Deduplicate files across clouds
- Create a single source of truth for each file
- Stop paying to host the same file in multiple clouds

## Installation

### Requirements

- Python 3.6 or higher
- No external dependencies required (uses Python standard library)

### Setup

1. Clone this repository:
```bash
git clone https://github.com/fef5002/clouds-detangler.git
cd clouds-detangler
```

2. Make the script executable:
```bash
chmod +x clouds_detangler.py
```

## Usage

### Basic Usage

Run the tool:

```bash
python3 clouds_detangler.py
```

The tool will:
1. Display important warnings about cloud storage
2. Detect cloud directories on your system
3. Ask for confirmation before scanning
4. Scan all detected cloud directories
5. Find duplicate files across different cloud providers
6. Generate a manifest file with detailed information
7. Show you the top duplicate groups wasting storage

### Understanding the Output

The tool will show:
- Which cloud directories were detected
- How many files were scanned in each
- How many duplicate groups were found
- Total wasted storage in GB
- Top 10 duplicate groups by wasted space
- Location of the generated manifest file

### Example Output

```
⚠️  CRITICAL WARNING: CLOUD STORAGE SYNCHRONIZATION ⚠️

IMPORTANT THINGS TO UNDERSTAND:

1. FILES IN DIFFERENT CLOUDS ARE SEPARATE FILES
   - A file in Google Drive is NOT the same as a file in OneDrive
   ...

Detected cloud storage directories:

GOOGLE_DRIVE:
  - /Users/yourname/Google Drive

ONEDRIVE:
  - /Users/yourname/OneDrive

Total files scanned: 1,234
Found 45 groups of duplicate files
Total wasted storage: 2.34 GB

Top 10 duplicate groups by wasted space:

1. Size: 150.00 MB, Copies: 3, Waste: 300.00 MB
   - [google_drive] /Users/yourname/Google Drive/Photos/vacation.jpg
   - [onedrive] /Users/yourname/OneDrive/Photos/vacation.jpg
   - [icloud] /Users/yourname/iCloud Drive/Photos/vacation.jpg

Manifest saved to: /current/directory/cloud_manifest.json
```

## The Manifest File

The generated `cloud_manifest.json` contains:

```json
{
  "generated_at": "2026-01-20T10:00:00",
  "total_files": 1234,
  "total_duplicates": 45,
  "files": [...],
  "duplicates": [...],
  "summary": {
    "total_size_gb": 50.5,
    "total_waste_gb": 2.34,
    "files_per_provider": {
      "google_drive": 456,
      "onedrive": 678,
      "icloud": 100
    }
  }
}
```

## Workflow to Detangle Your Clouds

### Step 1: Understand the Situation

Run this tool to:
- Get educated about how cloud sync really works
- See which cloud directories you have
- Identify all duplicate files

### Step 2: Plan Your Strategy

Decide:
- Which cloud provider should be your primary for each type of file
- Which duplicates can be safely removed
- How to organize your files going forward

### Step 3: Unhook Services

If you've connected cloud services to sync with each other:
1. Disconnect those integrations
2. Stop any third-party sync tools
3. Let each cloud service be independent

### Step 4: Deduplicate

Using the manifest:
1. Review duplicate groups
2. Choose one copy to keep (in your primary cloud)
3. **Carefully** delete duplicates from other clouds
4. Remember: Deleting from local folders deletes from the cloud!

### Step 5: Reorganize (Optional)

Consider using `rclone` for advanced cloud management:
```bash
# Install rclone
# Configure your cloud providers
rclone config

# Copy files between clouds (doesn't delete originals)
rclone copy source:path dest:path

# Dedupe within a single cloud
rclone dedupe source:path
```

### Step 6: Set Up Proper Backups

- Cloud sync is NOT backup
- Use proper backup tools (Time Machine, Backblaze, etc.)
- Keep backups separate from cloud sync

## Important Reminders

### ⚠️ Before Deleting Anything

1. **Verify the manifest** - Make sure you understand what files are duplicates
2. **Choose carefully** - Decide which copy to keep
3. **Backup first** - Make a backup before deleting duplicates
4. **Delete one at a time** - Don't bulk delete until you're confident
5. **Check the trash** - Most cloud services have a trash/recycle bin

### ⚠️ About Local Cloud Folders

- They are NOT local copies
- They ARE synchronized with the cloud
- Changes propagate to the cloud immediately
- Deletions are permanent (subject to trash policies)

### ⚠️ About Multiple Clouds

- Each cloud is independent
- Files with the same name are different files
- Syncing clouds together creates problems
- Use ONE cloud per file type/category

## Advanced Configuration

Copy the example configuration:
```bash
cp config.example.json config.json
```

Edit `config.json` to customize:
- Specific paths to scan
- File patterns to exclude
- Minimum file size
- Output directory
- Warning preferences

## Troubleshooting

### No Cloud Directories Detected

Make sure:
- Cloud storage apps are installed
- Cloud folders are set up on your system
- You're running the tool with proper permissions

### Permission Errors

Some cloud directories may have restricted permissions. Run with:
```bash
sudo python3 clouds_detangler.py
```

### Large Number of Files

For systems with many files:
- The scan may take several minutes
- Hash computation is the slowest part
- Consider scanning one cloud at a time

## Integration with rclone

This tool identifies duplicates. For advanced cloud management, use `rclone`:

```bash
# List configured remotes
rclone listremotes

# Check differences between clouds
rclone check gdrive: onedrive:

# Dedupe within a cloud
rclone dedupe --dedupe-mode newest gdrive:

# Move files between clouds
rclone move gdrive:source onedrive:dest
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Disclaimer

This tool is provided as-is. Always backup your data before making changes. The authors are not responsible for data loss resulting from use of this tool.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Remember**: Cloud storage is convenient, but it's not a backup solution. Always maintain proper backups of important data!

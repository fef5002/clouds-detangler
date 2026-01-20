# Workflow Guide: Detangling Your Cloud Storage

This guide walks you through the complete process of organizing your cloud storage and eliminating duplicates.

## Prerequisites

Before you start:
- ✅ You have multiple cloud storage accounts (Google Drive, OneDrive, iCloud, etc.)
- ✅ You have local sync folders set up for these services
- ✅ You've backed up important data (just in case)
- ✅ You understand that this process will involve deleting files

## Step-by-Step Workflow

### Phase 1: Discovery and Understanding

#### 1. Run the Detangler Tool

```bash
python3 clouds_detangler.py
```

**What happens:**
- You'll see critical warnings about cloud storage
- The tool will detect your cloud directories
- You'll be asked to confirm the scan

#### 2. Review the Scan Results

Pay attention to:
- How many files are in each cloud
- How many duplicate groups exist
- Total wasted storage

Example output:
```
Total files scanned: 2,500
Found 150 groups of duplicate files
Total wasted storage: 5.67 GB
```

#### 3. Study the Manifest

Open `cloud_manifest.json` and review:
- The duplicates section
- Files that appear in multiple clouds
- Which clouds have the most duplicates

### Phase 2: Planning

#### 4. Decide Your Primary Cloud for Each Category

Make a decision table:

| File Category | Primary Cloud | Reason |
|--------------|---------------|---------|
| Work Documents | OneDrive | Work account integration |
| Personal Photos | Google Drive | Google Photos integration |
| Important Files | iCloud | Apple ecosystem |
| Archives | Dropbox | Long-term storage |

#### 5. Create a Deletion Plan

For each duplicate group in the manifest:
1. Identify which copy to KEEP
2. Mark which copies to DELETE
3. Note any special considerations

Example:
```
Duplicate: family-photo.jpg
- KEEP: Google Drive (primary for photos)
- DELETE: OneDrive copy
- DELETE: iCloud copy
```

#### 6. Identify Risky Deletions

Flag files where you're uncertain:
- Files with different modification dates
- Files in multiple versions
- Critical files (test with a copy first)

### Phase 3: Preparation

#### 7. Unhook Any Cloud-to-Cloud Sync

If you've set up services to sync with each other:

**Google Drive ↔ OneDrive sync:**
- Disconnect third-party sync tools
- Turn off any automation

**Cloud Backup Services:**
- Pause services like Backblaze during cleanup
- They'll re-scan after you're done

#### 8. Make Final Backups

Before deleting anything:
```bash
# Create a timestamp
DATE=$(date +%Y%m%d)

# Backup your cloud folders
tar -czf backup-clouds-$DATE.tar.gz \
  ~/Google\ Drive \
  ~/OneDrive \
  ~/iCloud\ Drive
```

Or use a backup tool:
- Time Machine (Mac)
- Windows Backup
- Carbon Copy Cloner
- Backblaze

### Phase 4: Deduplication

#### 9. Start with Low-Risk Deletions

Begin with duplicates you're confident about:
- Exact copies with same size and date
- Non-critical files
- Recent files you remember duplicating

#### 10. Delete Files Carefully

**IMPORTANT:** Remember that deleting from local folders deletes from the cloud!

For each duplicate to delete:

```bash
# Option 1: Move to a temporary folder first (safer)
mkdir ~/temp-cloud-cleanup
mv "path/to/duplicate/file" ~/temp-cloud-cleanup/

# Wait 24 hours to ensure no issues
# Then permanently delete
rm -rf ~/temp-cloud-cleanup/
```

**OR**

Delete directly (if you're confident):
```bash
# On Mac/Linux
rm "path/to/duplicate/file"

# On Windows
del "path\to\duplicate\file"
```

#### 11. Verify Deletions

After each batch of deletions:
1. Check that the primary copy still exists
2. Verify it's accessible in the cloud web interface
3. Confirm the size/content is correct

### Phase 5: Reorganization (Optional)

#### 12. Use rclone for Advanced Management

If you need to move files between clouds:

```bash
# Install rclone
# Visit: https://rclone.org/install/

# Configure your cloud providers
rclone config

# Example: Move files from OneDrive to Google Drive
rclone move onedrive:Photos gdrive:Photos --progress

# Copy instead of move (keeps original)
rclone copy onedrive:Photos gdrive:Photos --progress

# Sync folders (makes destination match source)
rclone sync onedrive:Photos gdrive:Photos --progress
```

**rclone Commands for This Project:**

```bash
# List all configured cloud remotes
rclone listremotes

# Compare two cloud directories
rclone check gdrive:Documents onedrive:Documents

# Find duplicates within a single cloud
rclone dedupe --dedupe-mode interactive gdrive:

# Size of each cloud
rclone size gdrive:
rclone size onedrive:
rclone size icloud:
```

#### 13. Consolidate by Category

Based on your plan from Step 4:

```bash
# Move all photos to Google Drive
rclone move onedrive:Photos gdrive:Photos
rclone move icloud:Photos gdrive:Photos

# Move all work docs to OneDrive
rclone move gdrive:Work onedrive:Work
rclone move icloud:Work onedrive:Work
```

### Phase 6: Verification

#### 14. Run Detangler Again

```bash
python3 clouds_detangler.py
```

Compare results:
- Duplicate groups should be reduced
- Wasted storage should be less
- Files should be in their designated clouds

#### 15. Verify Critical Files

Check that all important files:
- Are in your chosen primary cloud
- Are accessible
- Have correct content
- Have recent backups

#### 16. Empty Cloud Trash

Most cloud services keep deleted files for 30 days:

**Google Drive:**
- Visit drive.google.com
- Click "Trash" in sidebar
- "Empty trash"

**OneDrive:**
- Visit onedrive.com
- Click "Recycle bin"
- "Empty recycle bin"

**iCloud:**
- Visit icloud.com
- Click "Recently Deleted"
- "Delete All"

### Phase 7: Ongoing Maintenance

#### 17. Establish New Habits

Going forward:
- ✅ Save files to only ONE cloud
- ✅ Know which cloud is for which category
- ✅ Don't hook clouds together
- ✅ Run detangler monthly to catch new duplicates

#### 18. Set Up Proper Backups

Cloud sync ≠ Backup. Use:
- **Time Machine** (Mac)
- **Windows Backup** (Windows)
- **Backblaze** (Online backup)
- **External drives** (Physical backup)

#### 19. Document Your System

Create a file: `~/cloud-organization.txt`

```
MY CLOUD ORGANIZATION SYSTEM
============================

Google Drive:
- Personal photos and videos
- Family documents
- Creative projects

OneDrive:
- Work documents
- School materials
- Shared team files

iCloud:
- iOS/Mac backups
- Keychain sync
- Notes and reminders

Backups:
- Time Machine to external drive (daily)
- Backblaze (continuous)
- Monthly archive to separate drive
```

## Troubleshooting

### "I can't find a file I deleted!"

1. Check the cloud's trash/recycle bin
2. Check your backup from Step 8
3. Check the manifest file for the file's last known location

### "Files reappeared after deletion"

Possible causes:
- Another device still syncing
- Cloud-to-cloud sync still active
- Shared folders with other users

Solution:
- Ensure all devices are synced
- Disconnect any automation
- Check sharing settings

### "Different clouds have different versions"

When files have different modification dates:
1. Compare content manually
2. Keep the newest version
3. Or keep copies in a "Review" folder

### "I'm nervous about deleting"

Start small:
1. Pick 5 obvious duplicates
2. Delete just those
3. Wait 24 hours
4. Verify everything is fine
5. Continue with more

## Safety Checklist

Before deleting each batch:
- [ ] I have a backup
- [ ] I know which copy I'm keeping
- [ ] I've verified the keeper exists
- [ ] I understand this deletes from the cloud
- [ ] I'm not deleting the last copy

## Time Estimates

For a typical user with 3 clouds and 10GB of duplicates:

| Phase | Time Required |
|-------|---------------|
| Discovery (scan) | 15-30 minutes |
| Planning | 1-2 hours |
| Preparation | 30 minutes |
| Deduplication | 2-4 hours |
| Verification | 30 minutes |
| **Total** | **~5-8 hours** |

Spread this over several days for safety.

## Success Metrics

You'll know you're done when:
- ✅ Duplicate groups < 10
- ✅ Wasted storage < 1GB
- ✅ Each file category has a primary cloud
- ✅ You understand where each file lives
- ✅ You have a backup strategy

## Additional Resources

- [rclone Documentation](https://rclone.org/docs/)
- [Google Drive Help](https://support.google.com/drive)
- [OneDrive Help](https://support.microsoft.com/onedrive)
- [iCloud Help](https://support.apple.com/icloud)

---

Remember: Take your time, verify everything, and when in doubt, don't delete!

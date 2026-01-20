# Quick Start Guide

Get started with Clouds Detangler in 5 minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/fef5002/clouds-detangler.git
cd clouds-detangler

# Run setup (optional)
bash setup.sh
```

## Quick Test

Test if cloud directories are detected:

```bash
python3 test_detection.py
```

## Full Scan

Run a complete scan of your cloud storage:

```bash
python3 clouds_detangler.py
```

Follow the prompts to:
1. Read the warnings
2. Confirm the scan
3. Review duplicate files
4. Check the generated manifest

## What You Get

After running, you'll have:
- `cloud_manifest.json` - Complete analysis of your files
- Console output showing top duplicates
- Understanding of your cloud storage situation

## Next Steps

1. Read the full [README.md](README.md) for detailed information
2. Follow the [WORKFLOW.md](WORKFLOW.md) for step-by-step cleanup
3. Review your `cloud_manifest.json` to plan deletions

## Key Warnings

⚠️ **Remember:**
- Local cloud folders sync with the cloud
- Deleting locally = deleting from the cloud
- Files in different clouds are separate files
- Cloud sync is NOT a backup

## Need Help?

- Read the [README.md](README.md) for full documentation
- Check [WORKFLOW.md](WORKFLOW.md) for detailed workflows
- Open an issue on GitHub for support

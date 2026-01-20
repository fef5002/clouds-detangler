# Quick Start Guide

Get started with Clouds Detangler in 5 steps.

## Step 1: Prerequisites

Install the required tools:

1. **Python 3.10+**: https://www.python.org/downloads/
2. **rclone**: https://rclone.org/downloads/

Verify installations:

```bash
python --version
rclone version
```

## Step 2: Install Dependencies

Clone or download this repository, then:

```bash
cd clouds-detangler
pip install -r requirements.txt
```

## Step 3: Configure rclone

You need at least one rclone remote configured. See detailed instructions in `docs/RCLONE_SETUP.md`.

Quick start for Google Drive:

```bash
rclone config
```

Follow the wizard to add a remote named `gdrive_main`.

Verify it works:

```bash
rclone lsf gdrive_main: --max-depth 1
```

## Step 4: Create Config Files

Copy the templates and customize:

```bash
cp config/template_clouds.yaml config/clouds.yaml
cp config/template_paths.yaml config/paths.yaml
```

Edit `config/clouds.yaml` to match your rclone remotes:

```yaml
clouds:
  - name: "Google Drive Main"
    rclone_remote: "gdrive_main"  # Must match your rclone remote name
    root: ""
    include_shared: false
```

## Step 5: Validate and Scan

Validate your setup:

```bash
python scripts/validate_setup.py
```

If all checks pass, gather metadata:

```bash
python scripts/gather_metadata.py
```

This will create JSON manifest files in the `manifests/` directory.

## What's Next?

After gathering metadata, you can:

1. **Build an index** to find duplicates (coming soon):
   ```bash
   python scripts/build_index.py
   ```

2. **Route evidence files** to multiple locations:
   ```bash
   python scripts/route_evidence.py myfile.jpg
   ```

3. **Process WhatsApp exports**:
   ```bash
   python scripts/process_whatsapp.py --chat "WhatsApp Chat.txt"
   ```

## Common Issues

### "Config file not found"

Make sure you copied the templates:
```bash
cp config/template_clouds.yaml config/clouds.yaml
cp config/template_paths.yaml config/paths.yaml
```

### "rclone not found"

Make sure rclone is installed and in your PATH:
```bash
rclone version
```

On Windows, you may need to add the rclone folder to your PATH.

### "OAuth token expired"

Reconnect your rclone remote:
```bash
rclone config reconnect gdrive_main:
```

### "Remote not found"

Check your remote names:
```bash
rclone listremotes
```

Make sure the `rclone_remote` value in `config/clouds.yaml` matches exactly.

## Getting Help

- Read the full documentation in `README.md`
- Check `docs/RCLONE_SETUP.md` for rclone configuration help
- Run validation to diagnose issues: `python scripts/validate_setup.py`
- Open an issue on GitHub if you encounter problems

## Example Workflow

Here's a complete example workflow:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure rclone (interactive)
rclone config

# 3. Copy config templates
cp config/template_clouds.yaml config/clouds.yaml
cp config/template_paths.yaml config/paths.yaml

# 4. Edit config/clouds.yaml to add your remotes
# (use your text editor)

# 5. Validate setup
python scripts/validate_setup.py

# 6. Gather metadata
python scripts/gather_metadata.py

# 7. Check the manifests
ls -lh manifests/
```

You should now have JSON manifest files showing all your cloud files!

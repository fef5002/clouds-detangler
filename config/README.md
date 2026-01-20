# Example Configuration for Clouds Detangler

This directory contains example configurations to help you get started.

## Files in this directory

- `example_clouds.yaml` - Example cloud provider configuration
- `example_paths.yaml` - Example output paths configuration

## How to use

1. Copy these files to the parent config directory and rename them:

```bash
cp config/example_clouds.yaml config/clouds.yaml
cp config/example_paths.yaml config/paths.yaml
```

2. Edit the files to match your setup:
   - Update remote names to match your `rclone listremotes` output
   - Adjust paths as needed

3. Run validation:

```bash
python scripts/validate_setup.py
```

## Security Note

⚠️ **NEVER commit your actual config files to version control!**

The actual config files (`clouds.yaml` and `paths.yaml`) are in `.gitignore` to prevent accidentally committing them. They may contain sensitive information about your cloud storage structure.

## Getting Help

See the main documentation:
- `../docs/RCLONE_SETUP.md` - How to configure rclone
- `../docs/QUICKSTART.md` - Quick start guide
- `../README.md` - Full documentation

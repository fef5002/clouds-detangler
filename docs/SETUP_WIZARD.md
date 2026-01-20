# Setup Wizard Guide

The Clouds Detangler Setup Wizard provides an interactive, typeform-style interface to configure your cloud storage setup.

## Overview

The setup wizard (`setup_wizard.py`) guides you through the entire setup process with a series of interactive screens:

1. **Prerequisites Check** - Verifies Python, rclone, and dependencies
2. **Configure Cloud Remotes** - Guides you through rclone OAuth setup
3. **Create Configuration** - Creates your config files
4. **Validate Setup** - Runs validation to ensure everything works

## Running the Wizard

```bash
python setup_wizard.py
```

## Features

### Interactive UI

- **Color-coded output**: Success (green), errors (red), warnings (yellow), info (blue)
- **Step-by-step progression**: Clear indication of where you are in the process
- **Smart defaults**: Suggested values you can accept or override
- **Yes/No prompts**: Simple confirmation questions
- **Multiple choice**: Select from predefined options
- **Text input**: Enter custom values with validation

### Cloud Provider Support

The wizard has built-in support for:

- **Google Drive** - Personal and Workspace accounts
- **OneDrive** - Personal and Business accounts
- **Dropbox** - Personal and Business accounts
- **Backblaze B2** - Backup storage
- **Other providers** - Manual configuration option

### OAuth Authentication

For cloud providers like Google Drive and OneDrive:

1. Wizard launches `rclone config`
2. rclone opens your web browser
3. You authenticate with your cloud provider
4. Grant permissions to rclone
5. rclone saves the credentials
6. Wizard verifies the remote was created

### Configuration Creation

The wizard creates two configuration files:

**`config/clouds.yaml`**:
```yaml
clouds:
  - name: "Google Drive Main"
    rclone_remote: "gdrive_main"
    root: ""
    include_shared: false
```

**`config/paths.yaml`**:
```yaml
manifests_dir: "./manifests"
logs_dir: "./logs"
database_path: "./clouds.duckdb"
```

## Workflow Example

### Step 1: Welcome Screen

```
======================================================================
                  Clouds Detangler Setup Wizard
======================================================================

Welcome!
This wizard will help you set up Clouds Detangler.

We'll guide you through:
  1. Checking prerequisites
  2. Configuring cloud storage remotes
  3. Creating configuration files
  4. Validating your setup

Ready to begin? [Y/n]:
```

### Step 2: Prerequisites

```
======================================================================
                        Prerequisites Check
======================================================================

Step 1/4: Checking Prerequisites

✓ Python 3.12 installed
✓ rclone is installed
✓ Python dependencies installed

Press Enter to continue...
```

### Step 3: Configure Remotes

```
======================================================================
                      Configure Cloud Storage
======================================================================

Step 2/4: Configure Cloud Remotes

ℹ Found 2 existing remote(s):
  - gdrive_main
  - onedrive

Use existing remotes? [Y/n]: y

Include 'gdrive_main' in configuration? [Y/n]: y
Display name for 'gdrive_main' [Gdrive_Main]: Google Drive
Root folder (leave blank for entire remote) []:
Include 'Shared with me' files? [y/N]: n

Include 'onedrive' in configuration? [Y/n]: y
Display name for 'onedrive' [Onedrive]: OneDrive Personal
Root folder (leave blank for entire remote) []:

Add new cloud remote? [Y/n]: n
```

### Step 4: Create Configuration

```
======================================================================
                    Create Configuration Files
======================================================================

Step 3/4: Create Configuration

Creating clouds.yaml...
✓ Created config/clouds.yaml

Creating paths.yaml...
Where should manifests be saved? [./manifests]:
Where should logs be saved? [./logs]:
Where should the database be saved? [./clouds.duckdb]:

✓ Created config/paths.yaml

✓ Configuration files created!

Press Enter to continue...
```

### Step 5: Validation

```
======================================================================
                          Validate Setup
======================================================================

Step 4/4: Validate Configuration

Running validation...

=== Checking prerequisites ===
[+] Prerequisites OK

=== Checking rclone remotes ===
[+] Found 2 rclone remote(s):
    - gdrive_main
    - onedrive

[+] Checking 2 configured cloud(s):
    ✓ Google Drive (remote: gdrive_main)
    ✓ OneDrive Personal (remote: onedrive)

=== Testing rclone access ===
[+] Testing access to: Google Drive
    Running: rclone lsf gdrive_main: --max-depth 1
[+] SUCCESS: Found 15 items in Google Drive

✓ Setup validation passed!
```

### Step 6: Summary

```
======================================================================
                         Setup Complete!
======================================================================

Next Steps:

1. Review your configuration in config/clouds.yaml
2. Run: python scripts/validate_setup.py
3. Gather metadata: python scripts/gather_metadata.py
4. Check manifests in the manifests/ directory

Documentation:

  - README.md - Full documentation
  - docs/QUICKSTART.md - Quick start guide
  - docs/RCLONE_SETUP.md - rclone configuration help

Thank you for using Clouds Detangler!
```

## Advanced Usage

### Using Existing Remotes

If you already have rclone configured, the wizard will detect your remotes and let you choose which ones to include.

### Adding New Remotes

The wizard can launch rclone config for you to add new remotes, or you can configure them manually and return to the wizard.

### Multiple Accounts

You can configure multiple accounts from the same provider:
- Multiple Google Drive accounts (personal + work)
- Multiple OneDrive accounts
- Mix and match different providers

### Partial Scans

You can configure remotes to scan only specific folders:
- Set `root` to `"Photos"` to scan only Photos folder
- Set `root` to `"Documents/Work"` for a specific subfolder

### Shared Files

For Google Drive, you can choose to include "Shared with me" files:
- Useful for work accounts with team folders
- Can be enabled per-remote

## Troubleshooting

### "rclone is not installed"

Download and install rclone from https://rclone.org/downloads/

### OAuth Browser Doesn't Open

If the browser doesn't open automatically:
1. Look for the URL in the terminal output
2. Copy and paste it into your browser manually
3. Complete the authentication
4. Copy the code back to the terminal if prompted

### "Remote not found"

Make sure you completed the rclone configuration:
1. Don't cancel the rclone config process
2. Follow all prompts until it says "Configuration complete"
3. Verify with: `rclone listremotes`

### Permission Denied

Make sure you grant the necessary permissions when authenticating:
- Google Drive: Grant file access
- OneDrive: Grant file access
- Some providers have read-only vs. full-access options

## Security Notes

- The wizard never stores passwords directly
- OAuth tokens are stored by rclone in its config file
- Your cloud credentials never pass through this tool
- rclone handles all authentication securely

## Next Steps

After completing the wizard:

1. **Validate**: Run `python scripts/validate_setup.py`
2. **Gather metadata**: Run `python scripts/gather_metadata.py`
3. **Review manifests**: Check the `manifests/` directory
4. **Explore tools**: Try other scripts like `route_evidence.py`

## Getting Help

- For rclone issues: See `docs/RCLONE_SETUP.md`
- For general help: See `README.md` and `docs/QUICKSTART.md`
- For bugs: Open an issue on GitHub

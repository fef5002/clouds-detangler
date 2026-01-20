# Setting Up rclone for Clouds Detangler

This guide will help you configure rclone to work with your cloud storage providers.

## What is rclone?

rclone is a command-line program that syncs files and directories to and from cloud storage. Think of it as rsync for cloud storage.

Website: https://rclone.org/

## Installation

### Windows

1. Download the latest rclone from: https://rclone.org/downloads/
2. Extract the ZIP file
3. Move `rclone.exe` to a folder in your PATH (e.g., `C:\Windows\System32`)
4. Or add the rclone folder to your PATH

### macOS

```bash
brew install rclone
```

Or download from: https://rclone.org/downloads/

### Linux

```bash
sudo apt install rclone  # Ubuntu/Debian
sudo dnf install rclone  # Fedora
```

Or download from: https://rclone.org/downloads/

## Verify Installation

```bash
rclone version
```

You should see version information.

## Configuring Cloud Remotes

### Google Drive

1. Run the configuration wizard:

```bash
rclone config
```

2. Choose `n` for new remote
3. Enter a name (e.g., `gdrive_main`)
4. Choose `drive` from the list (Google Drive)
5. Leave client_id and client_secret blank (press Enter) unless you have your own OAuth app
6. Choose scope `1` (full access) or `2` (read-only if you only want to scan)
7. Leave root_folder_id blank (press Enter)
8. Leave service_account_file blank (press Enter)
9. Choose `n` for advanced config
10. Choose `y` to auto config (opens browser for OAuth)
11. Log in with your Google account and grant permissions
12. Choose whether this is a Shared Drive (usually `n`)
13. Confirm the configuration

### OneDrive

1. Run the configuration wizard:

```bash
rclone config
```

2. Choose `n` for new remote
3. Enter a name (e.g., `onedrive`)
4. Choose `onedrive` from the list
5. Leave client_id and client_secret blank (press Enter)
6. Choose `n` for advanced config
7. Choose `y` to auto config (opens browser for OAuth)
8. Log in with your Microsoft account
9. Choose the type of OneDrive:
   - `1` for OneDrive Personal
   - `2` for OneDrive for Business
   - `3` for SharePoint
10. If prompted, choose your drive
11. Confirm the configuration

### Dropbox

1. Run the configuration wizard:

```bash
rclone config
```

2. Choose `n` for new remote
3. Enter a name (e.g., `dropbox`)
4. Choose `dropbox` from the list
5. Leave client_id and client_secret blank (press Enter)
6. Choose `n` for advanced config
7. Choose `y` to auto config (opens browser for OAuth)
8. Log in with your Dropbox account
9. Confirm the configuration

### Backblaze B2 (for backups)

1. Create a B2 account at https://www.backblaze.com/b2
2. Create an application key:
   - Go to "App Keys" in B2 web console
   - Click "Add a New Application Key"
   - Give it a name and appropriate permissions
   - Save the keyID and applicationKey
3. Run the configuration wizard:

```bash
rclone config
```

4. Choose `n` for new remote
5. Enter a name (e.g., `b2`)
6. Choose `b2` from the list
7. Enter your account ID (keyID)
8. Enter your application key
9. Leave endpoint blank (press Enter)
10. Choose `n` for advanced config
11. Confirm the configuration

## Testing Your Configuration

List your configured remotes:

```bash
rclone listremotes
```

You should see:
```
gdrive_main:
onedrive:
dropbox:
b2:
```

Test accessing a remote:

```bash
rclone lsf gdrive_main: --max-depth 1
```

This should list the top-level folders in your Google Drive.

## Troubleshooting

### "OAuth token expired"

If you get this error, reconnect the remote:

```bash
rclone config reconnect gdrive_main:
```

This will open your browser to re-authenticate.

### "Remote not found"

Make sure the remote name matches exactly what you configured:

```bash
rclone listremotes
```

The name must include the colon (`:`) when used in commands but not when specified in config.

### Permission Denied

Make sure you granted the necessary permissions when authenticating. You may need to delete and recreate the remote with the correct scope.

## Next Steps

Once you have at least one remote configured:

1. Copy the template configs:
```bash
cp config/template_clouds.yaml config/clouds.yaml
cp config/template_paths.yaml config/paths.yaml
```

2. Edit `config/clouds.yaml` to add your remotes

3. Run the validation script:
```bash
python scripts/validate_setup.py
```

4. Gather metadata:
```bash
python scripts/gather_metadata.py
```

## Security Notes

- rclone stores your OAuth tokens in `~/.config/rclone/rclone.conf` (Linux/Mac) or `%APPDATA%\rclone\rclone.conf` (Windows)
- These tokens give access to your cloud storage
- Keep this file secure - don't share it or commit it to git
- For sensitive environments, consider using rclone's built-in encryption or `rclone config password` to encrypt the config file

## More Information

- Full rclone documentation: https://rclone.org/docs/
- Google Drive setup: https://rclone.org/drive/
- OneDrive setup: https://rclone.org/onedrive/
- Dropbox setup: https://rclone.org/dropbox/
- Backblaze B2 setup: https://rclone.org/b2/

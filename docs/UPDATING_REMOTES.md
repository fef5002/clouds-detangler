# Updating Existing Remotes

If you set up rclone months or years ago, your OAuth tokens or passwords might be expired. This guide explains how to update them.

## Why Remotes Need Updating

Common reasons:
- **OAuth tokens expired** - Google Drive, OneDrive tokens expire after ~60 days of inactivity
- **Password changed** - You changed your cloud account password
- **Permissions revoked** - You or your organization revoked rclone's access
- **Account migrated** - Moved from personal to business account

## Using the Setup Wizard (Easiest)

The setup wizard now includes a **Review & Update Existing Remotes** step:

```bash
python setup_wizard.py
```

### What the Wizard Does

**Step 1: Lists all your remotes**
```
Found 3 existing remote(s):

gdrive_main
  Type: drive
  Testing access... ✓ Working

onedrive_old
  Type: onedrive  
  Testing access... ✗ Failed (may need reconnecting)

dropbox_2020
  Type: dropbox
  Testing access... ✗ Failed (may need reconnecting)
```

**Step 2: Offers update options**

For each broken remote, you can:

1. **Reconnect** - Re-authenticate with OAuth (refreshes tokens)
2. **Reconfigure** - Edit all settings (passwords, paths, etc.)
3. **Delete and recreate** - Start fresh with same name
4. **Skip** - Leave it for now
5. **Update from Bitwarden CLI** - Retrieve password from Bitwarden

## Using Bitwarden CLI for Passwords

If you use Bitwarden to manage passwords:

### 1. Install Bitwarden CLI

```bash
# npm (Node.js required)
npm install -g @bitwarden/cli

# Or download from:
# https://bitwarden.com/help/cli/
```

### 2. Log in to Bitwarden

```bash
bw login
# Enter your email and master password

bw unlock
# Enter master password, save the session key
```

### 3. Run the Setup Wizard

When asked "Are you using Bitwarden CLI?", say **yes**.

The wizard will show option 5: "Update password from Bitwarden CLI"

### 4. Provide the Bitwarden Item Name

```
Bitwarden item name for onedrive_old: Microsoft OneDrive
```

The wizard will run:
```bash
bw get password "Microsoft OneDrive"
```

And use that password to update your rclone config.

## Manual Update (Without Wizard)

### Reconnect (OAuth Remotes)

For Google Drive, OneDrive, Dropbox:

```bash
rclone config reconnect gdrive_main:
```

This opens your browser to re-authenticate.

### Update Configuration

For any remote:

```bash
rclone config update onedrive_old
```

This lets you edit settings including passwords.

### Test a Remote

```bash
rclone lsf gdrive_main: --max-depth 1
```

If this works, the remote is good!

## Bitwarden CLI Examples

### List All Items

```bash
bw list items
```

### Get a Specific Password

```bash
# By name
bw get password "Google Drive"

# By ID
bw get password a1b2c3d4-e5f6-7890-abcd-ef1234567890

# Store in variable (for scripts)
PASSWORD=$(bw get password "OneDrive")
```

### Search for Items

```bash
bw list items --search drive
```

### Use with rclone

```bash
# Get password from Bitwarden
PASSWORD=$(bw get password "Dropbox")

# Update rclone config (you'll need to enter it when prompted)
rclone config update dropbox
```

## Common Issues

### "OAuth token expired"

**Solution:** Use `rclone config reconnect remote:`

```bash
rclone config reconnect gdrive_main:
```

### "Bitwarden CLI not found"

**Solution:** Install Bitwarden CLI

```bash
npm install -g @bitwarden/cli
```

Or download from: https://bitwarden.com/help/cli/

### "Bitwarden is locked"

**Solution:** Unlock your vault

```bash
bw unlock
# Save the BW_SESSION variable it gives you
export BW_SESSION="your_session_key"
```

### "Password incorrect"

**Solution:** 
1. Check the password in Bitwarden web vault
2. Make sure you're getting the right item
3. Try updating the password in Bitwarden first

## Best Practices

### For OAuth Remotes (Google Drive, OneDrive, Dropbox)

- Use "Reconnect" option - fastest and safest
- Keep your browser logged in to make it easier
- Grant necessary permissions when asked

### For Password-Based Remotes

- Store passwords in Bitwarden (or another password manager)
- Never store passwords in plain text files
- Use the Bitwarden CLI integration in the wizard

### Security Tips

- Keep Bitwarden master password secure
- Use `bw lock` when done
- Don't commit rclone.conf to version control
- Use `rclone config password` to encrypt the rclone config

## Example Workflow

### Scenario: You have 3 old remotes with expired tokens

**Step 1:** Run the wizard
```bash
python setup_wizard.py
```

**Step 2:** When it finds broken remotes
```
Remotes that need updating:
  ✗ gdrive_2020
  ✗ onedrive_work
  ✗ dropbox_old

Would you like to update these remotes now? [Y/n]: y
```

**Step 3:** Update each one

For `gdrive_2020`:
- Choose option 1: Reconnect
- Browser opens → Log in to Google → Allow access
- ✓ Success!

For `onedrive_work`:
- Using Bitwarden? Yes
- Choose option 5: Update from Bitwarden CLI
- Item name: "Microsoft Work Account"
- ✓ Password retrieved and updated!

For `dropbox_old`:
- Choose option 3: Delete and recreate
- Confirm deletion
- Create new remote with same name
- ✓ Fresh configuration!

**Step 4:** Continue with wizard

All remotes now working! Proceed to configure clouds.yaml.

## Troubleshooting

### Remote Still Broken After Update

1. Delete the remote: `rclone config delete remote_name`
2. Create it fresh: `rclone config`
3. Test it: `rclone lsf remote_name: --max-depth 1`

### Too Many Remotes

Delete unused ones:
```bash
rclone config delete old_remote_name
```

### Want to Start Fresh

Backup your config:
```bash
# Linux/Mac
cp ~/.config/rclone/rclone.conf ~/.config/rclone/rclone.conf.backup

# Windows
copy %APPDATA%\rclone\rclone.conf %APPDATA%\rclone\rclone.conf.backup
```

Then delete all and start over:
```bash
rm ~/.config/rclone/rclone.conf  # Linux/Mac
del %APPDATA%\rclone\rclone.conf # Windows
```

## More Information

- rclone config commands: https://rclone.org/commands/rclone_config/
- Bitwarden CLI: https://bitwarden.com/help/cli/
- OAuth tokens: https://rclone.org/docs/#oauth
- Encrypted configs: https://rclone.org/docs/#configuration-encryption

---

*Updated remotes mean reliable cloud access!* ✨

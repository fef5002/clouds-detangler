# Remote Update Feature Demo

This shows the new "Review & Update Existing Remotes" step in action.

## Scenario: User has 3 old remotes, 1 works, 2 are broken

### Step 2: Review & Update Existing Remotes

```
======================================================================
                 Review & Update Existing Remotes
======================================================================

Step 2/5: Review Existing Remotes

Found 3 existing remote(s):

gdrive_main
  Type: drive
  Testing access... ✓ Working ✓

onedrive_old
  Type: onedrive
  Testing access... ✗ Failed ✗ (may need reconnecting)

dropbox_2020
  Type: dropbox
  Testing access... ✗ Failed ✗ (may need reconnecting)

======================================================================
Remotes that need updating:
======================================================================

  ✗ onedrive_old
  ✗ dropbox_2020

======================================================================

Why remotes fail:
  • OAuth tokens expired (need to log in again)
  • Passwords changed
  • Account permissions changed
  • Remote was deleted from cloud provider

Would you like to update these remotes now? [Y/n]: y
```

## User Chooses to Update

### Bitwarden CLI Question

```
Let's update your remotes.

Are you using Bitwarden CLI for password management? [y/N]: y

ℹ Great! Make sure you're logged into Bitwarden CLI:
  bw login
  bw unlock

ℹ You can retrieve passwords with:
  bw get password <item-name>

Are you logged into Bitwarden CLI? [y/N]: y
```

## Updating First Remote: onedrive_old

```
======================================================================
Updating: onedrive_old
======================================================================

Remote type: onedrive

Update options:

1. Reconnect (re-authenticate with OAuth)
2. Reconfigure (edit all settings)
3. Delete and recreate
4. Skip this remote
5. Update password from Bitwarden CLI

Choose an option (1-5) [1]: 5

ℹ Retrieving password from Bitwarden CLI...

Bitwarden item name for onedrive_old: Microsoft OneDrive

Running: bw get password "Microsoft OneDrive"

✓ Password retrieved from Bitwarden!

ℹ Now updating rclone config with new password...
ℹ You'll need to enter this password when prompted.

[rclone config update onedrive_old runs interactively]
```

## Updating Second Remote: dropbox_2020

```
======================================================================
Updating: dropbox_2020
======================================================================

Remote type: dropbox

Update options:

1. Reconnect (re-authenticate with OAuth)
2. Reconfigure (edit all settings)
3. Delete and recreate
4. Skip this remote
5. Update password from Bitwarden CLI

Choose an option (1-5) [1]: 1

ℹ Reconnecting dropbox_2020...
ℹ Your browser will open for authentication.

[Browser opens, user logs in to Dropbox, grants permission]

✓ Successfully reconnected dropbox_2020!
```

## Update Summary

```
======================================================================
Remote Update Summary
======================================================================

Updated 2 remote(s)

Successfully updated:
  ✓ onedrive_old
  ✓ dropbox_2020


Press Enter to continue...
```

## Alternative Scenario: User Not Using Bitwarden

```
Are you using Bitwarden CLI for password management? [y/N]: n

======================================================================
Updating: onedrive_old
======================================================================

Remote type: onedrive

Update options:

1. Reconnect (re-authenticate with OAuth)
2. Reconfigure (edit all settings)
3. Delete and recreate
4. Skip this remote

Choose an option (1-4) [1]: 1

ℹ Reconnecting onedrive_old...
ℹ Your browser will open for authentication.

[Browser opens to Microsoft login]

✓ Successfully reconnected onedrive_old!
```

## What Each Option Does

### Option 1: Reconnect (OAuth)
- Best for: Google Drive, OneDrive, Dropbox
- Opens browser for re-authentication
- Refreshes OAuth tokens
- Fastest option for OAuth remotes

### Option 2: Reconfigure
- Best for: Changing settings, paths, or non-OAuth passwords
- Opens interactive rclone config
- Can edit any setting
- More thorough than reconnect

### Option 3: Delete & Recreate
- Best for: Completely broken configs
- Deletes the remote entirely
- Walks through creating it again
- Fresh start with same name

### Option 4: Skip
- Best for: Remotes you'll fix later
- Doesn't update anything
- Can return to wizard anytime
- Good for low-priority remotes

### Option 5: Bitwarden CLI (when enabled)
- Best for: Password-based remotes
- Retrieves password from Bitwarden
- No typing passwords
- Secure and convenient

## Real-World Use Cases

### Case 1: OAuth Token Expired

**Problem:** Set up Google Drive 3 months ago, token expired

**Solution:**
```
Choose option (1-5): 1
[Browser opens]
[Log in to Google]
[Allow access]
✓ Success!
```

**Time:** 30 seconds

### Case 2: Password Changed in Bitwarden

**Problem:** Updated OneDrive password in Bitwarden, rclone still has old one

**Solution:**
```
Choose option (1-5): 5
Item name: Microsoft OneDrive
✓ Password retrieved and updated!
```

**Time:** 15 seconds

### Case 3: Don't Remember What's Wrong

**Problem:** Remote broken, not sure why

**Solution:**
```
Choose option (1-5): 1  (try reconnect first)
If that doesn't work, try option 2 (reconfigure)
If still broken, option 3 (delete & recreate)
```

**Time:** 1-2 minutes with trial and error

### Case 4: Multiple Remotes Need Updates

**Problem:** Haven't used rclone in a year, everything's broken

**Solution:**
```
Update each remote one by one:
- OAuth remotes: option 1 (reconnect)
- Password remotes: option 5 (Bitwarden) or 2 (reconfigure)
- Totally broken: option 3 (delete & recreate)

Summary: Updated 5 remotes in 10 minutes!
```

## Error Handling

### Bitwarden Not Logged In

```
Running: bw get password "Microsoft OneDrive"

✗ Failed to retrieve password from Bitwarden
ℹ Make sure you're logged in: bw login && bw unlock
```

### Reconnect Failed

```
✗ Reconnect failed for gdrive_old
ℹ Try option 2 (Reconfigure) or option 3 (Delete & recreate)
```

### Item Not Found in Bitwarden

```
✗ Failed to retrieve password from Bitwarden

[Check the item name in Bitwarden]
[Try again with correct name]
```

## Benefits

✅ **Saves Time** - No manual config file editing  
✅ **Secure** - Passwords from Bitwarden, not typed  
✅ **Smart** - Tests remotes to find problems  
✅ **Flexible** - Multiple fix options per remote  
✅ **Safe** - Can skip and return later  
✅ **Educational** - Explains what each option does  

## Perfect For

- **People with old rclone configs** (like you!)
- **Bitwarden users** who want secure password management
- **OAuth users** whose tokens expired
- **Anyone** who hasn't used rclone in months/years

The remote update feature turns a frustrating manual task into a guided, 
secure, and quick process! 🎉

# PATH Helper Demo

This shows what the new PATH helper looks like when you run the setup wizard.

## Scenario: rclone is downloaded but not in PATH

When the wizard runs the prerequisites check and finds rclone on your computer but not in PATH:

```
======================================================================
                        Prerequisites Check
======================================================================

Step 1/4: Checking Prerequisites

✓ Python 3.12 installed
✗ rclone is not found in PATH

ℹ Found rclone at: C:\Users\YourName\Downloads\rclone-v1.65.0-windows-amd64\rclone.exe
ℹ But it's not in your PATH, so we need to add it.

Would you like help adding rclone to PATH? [Y/n]: y

Press Enter to see instructions...
```

## Then it shows the PATH helper screen:

```
======================================================================
                      Add rclone to PATH
======================================================================

Let's find rclone and add it to your PATH.

✓ Found rclone at: C:\Users\YourName\Downloads\rclone-v1.65.0-windows-amd64\rclone.exe

======================================================================
What is PATH?
======================================================================

PATH is a list of folders where your computer looks for programs.
When you type 'rclone' in the terminal, your computer searches
these folders to find the rclone program.

We need to add rclone to PATH so you can run it from anywhere.
======================================================================

Option 1: Quick Method (This Session Only)

Copy and paste this command in your terminal:

set PATH=%PATH%;C:\Users\YourName\Downloads\rclone-v1.65.0-windows-amd64

⚠ Note: This only works until you close the terminal.

Option 2: Permanent Method (Recommended)

1. Press Windows Key and search for 'Environment Variables'
2. Click 'Edit the system environment variables'
3. Click 'Environment Variables...' button
4. Under 'User variables', find and select 'Path'
5. Click 'Edit...'
6. Click 'New'
7. Paste this folder path: C:\Users\YourName\Downloads\rclone-v1.65.0-windows-amd64
8. Click 'OK' on all windows
9. Close and reopen your terminal

Option 3: PowerShell Command (Permanent)

⚠ Run PowerShell as Administrator, then paste this:

[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Users\YourName\Downloads\rclone-v1.65.0-windows-amd64", "User")

======================================================================

After adding to PATH:
1. Close and reopen your terminal (or reload shell)
2. Test by typing: rclone version
3. You should see the rclone version information

Have you added rclone to PATH? [y/N]: 
```

## For Mac/Linux users, it looks like this:

```
Option 1: Quick Method (This Session Only)

Copy and paste this command in your terminal:

export PATH="$PATH:/Users/yourname/Downloads/rclone-v1.65.0-osx-amd64"

⚠ Note: This only works until you close the terminal.

Option 2: Permanent Method (Recommended)

Copy and paste this command in your terminal:

echo 'export PATH="$PATH:/Users/yourname/Downloads/rclone-v1.65.0-osx-amd64"' >> ~/.zshrc

Then reload your shell with: source ~/.zshrc

Option 3: Move to System Folder

Copy and paste this command (may need to enter your password):

sudo mv /Users/yourname/Downloads/rclone-v1.65.0-osx-amd64/rclone /usr/local/bin/
```

## Key Features

✅ **Auto-detects rclone** - Searches common download locations  
✅ **Multiple options** - Quick, permanent, PowerShell/shell, move to system folder  
✅ **Copy-paste ready** - All commands are ready to copy and paste  
✅ **Platform-specific** - Different instructions for Windows/Mac/Linux  
✅ **Educational** - Explains what PATH is in simple terms  
✅ **Safe** - Shows exactly what each command does before running  

## Perfect For

- **Teens learning to code** (like your 13-year-old boys!)
- **Parents helping their kids** (middle-age moms three decades post-DOS!)
- **Anyone comfortable with CLI** but doesn't know environment variables
- **Users who want guidance** without being patronized

The setup wizard makes the complex task of PATH configuration into a simple, guided experience with copy-paste commands. No need to understand Windows registry, shell profiles, or environment variables - just follow the steps!

# Getting Started - For Beginners

This guide is written for people who are new to command-line tools but want to learn. If you're 13 or a parent helping your kids, this is for you!

## What You Need

1. **A computer** - Windows, Mac, or Linux
2. **Internet connection** - To download rclone and authenticate with your cloud accounts
3. **Basic typing skills** - You'll be typing commands, but we'll tell you exactly what to type

## What is a Terminal?

A **terminal** (also called command prompt or command line) is where you type text commands to tell your computer what to do. Don't worry - we'll give you the exact commands to copy and paste!

### Opening the Terminal

**Windows:**
- Press `Windows Key` + type `cmd` or `powershell`
- Click on "Command Prompt" or "PowerShell"

**Mac:**
- Press `Command` + `Space`
- Type `terminal`
- Press Enter

**Linux:**
- Press `Ctrl` + `Alt` + `T`

## Step 1: Install Python

Python is a programming language. This tool is written in Python.

1. Go to: https://www.python.org/downloads/
2. Click the big yellow "Download Python" button
3. Run the installer
4. **IMPORTANT**: Check the box that says "Add Python to PATH"
5. Click "Install Now"

### Test if Python is installed:

Open your terminal and type:
```bash
python --version
```

You should see something like `Python 3.12.3`. If you do, you're good! 🎉

## Step 2: Download rclone

rclone is the program that talks to your cloud storage (Google Drive, OneDrive, etc.)

1. Go to: https://rclone.org/downloads/
2. Click on your operating system (Windows, Mac, or Linux)
3. Download the file (it's a ZIP file)
4. Extract the ZIP file to your Downloads folder

**Windows users:** Right-click the ZIP → "Extract All"  
**Mac users:** Double-click the ZIP file  

## Step 3: Get Clouds Detangler

### Option A: Download ZIP (Easier)
1. Go to: https://github.com/fef5002/clouds-detangler
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP to a folder you'll remember (like Documents)

### Option B: Use Git (If you know how)
```bash
git clone https://github.com/fef5002/clouds-detangler.git
cd clouds-detangler
```

## Step 4: Open Terminal in the Project Folder

You need to "be inside" the clouds-detangler folder in your terminal.

**Windows:**
1. Open File Explorer
2. Go to where you extracted clouds-detangler
3. Click in the address bar at the top
4. Type `cmd` and press Enter
   - This opens a terminal already in that folder!

**Mac/Linux:**
1. Open Terminal
2. Type `cd ` (with a space after it)
3. Drag the clouds-detangler folder onto the terminal window
4. Press Enter

## Step 5: Install Dependencies

Dependencies are other programs this tool needs. Type this command:

```bash
pip install -r requirements.txt
```

Wait for it to finish (you'll see green text). This might take a minute.

## Step 6: Run the Setup Wizard

Now for the fun part! Type:

```bash
python setup_wizard.py
```

The wizard will:
1. Check if everything is installed correctly
2. Help you add rclone to PATH (so you can use it anywhere)
3. Guide you through connecting to your cloud accounts
4. Set up your configuration files
5. Test that everything works

### Following the Wizard

The wizard will ask you questions. Read each question carefully.

**When you see `[Y/n]`:**
- Capital `Y` means "yes" is the default
- Just press Enter for "yes"
- Type `n` and Enter for "no"

**When you see `[y/N]`:**
- Capital `N` means "no" is the default
- Type `y` and Enter for "yes"
- Just press Enter for "no"

**Copy-paste commands:**
- When the wizard shows a command in blue/cyan text
- Select it with your mouse
- Right-click → Copy (or Ctrl+C / Cmd+C)
- Right-click in the terminal → Paste (or Ctrl+V / Cmd+V)
- Press Enter

## Step 7: Connecting Your Cloud Accounts

When the wizard asks which cloud you want to connect:

1. Choose your cloud provider (like Google Drive)
2. The wizard will open your web browser
3. Log in to your cloud account
4. Click "Allow" to let rclone access your files
5. The browser will say "Success!" and you can close it
6. Go back to the terminal

**Don't worry:** rclone is safe and trusted by millions of people. It only gets permission to see your files - it doesn't steal them!

## Common Questions

### "What is PATH?"

PATH is a list of folders where your computer looks for programs. When you type `rclone` in the terminal, your computer searches these folders to find it.

The wizard will help you add rclone to PATH so it works from anywhere.

### "The browser didn't open!"

Sometimes the browser doesn't open automatically. Look in the terminal for a long URL (web address) starting with `https://`. Copy it and paste it into your web browser.

### "I got an error!"

Don't panic! Read the error message - it usually tells you what's wrong:

- **"rclone not found"** → Need to add rclone to PATH (wizard will help)
- **"Permission denied"** → Try running as administrator (Windows) or with `sudo` (Mac/Linux)
- **"Module not found"** → Need to run `pip install -r requirements.txt` again

### "Can I mess up my files?"

No! The first time you run it, the tool only **reads** your cloud storage - it doesn't change, move, or delete anything. It just makes a list of what files you have.

Later features let you organize files, but they'll always ask for confirmation first.

## After Setup: What Can You Do?

### See what files you have in all your clouds:

```bash
python scripts/gather_metadata.py
```

This creates a list (manifest) of every file in each cloud.

### Check if files are duplicated:

```bash
python scripts/build_index.py
```

This will tell you if the same file exists in multiple places.

### Process WhatsApp chats:

```bash
python scripts/process_whatsapp.py --chat "WhatsApp Chat.txt"
```

This organizes WhatsApp exports.

## Getting Help

- **README.md** - Full documentation
- **docs/QUICKSTART.md** - Quick start guide
- **docs/RCLONE_SETUP.md** - Help with rclone
- **docs/SETUP_WIZARD.md** - Wizard walkthrough

## Tips for Parents

Teaching your kids to use command-line tools:

1. **Start simple** - Run the wizard together the first time
2. **Explain what's happening** - Show them the files being created
3. **Let them type** - Don't do it for them (they learn by doing)
4. **Mistakes are OK** - Nothing will break! They can always re-run the wizard
5. **Celebrate success** - When it works, that's real programming!

## Safety Reminders

✅ **Do:**
- Read what the wizard asks before answering
- Keep your passwords private
- Ask an adult if you're unsure about giving permissions

❌ **Don't:**
- Share your rclone config file (it has your login tokens)
- Run commands you don't understand from strangers
- Give rclone access to accounts you don't own

## You Did It! 🎉

If you made it through the setup wizard, congratulations! You just:

1. Installed Python
2. Downloaded and configured rclone
3. Connected to cloud storage using OAuth
4. Ran a Python program

These are real programming and IT skills. Pretty cool, right?

Now you can explore the other features and maybe even look at the Python code to see how it works!

---

*Made with ❤️ by Fiona for her boys and anyone learning to code*

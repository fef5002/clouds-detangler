# Debugging Guide

This guide explains how to use the debugging and logging features in Clouds Detangler.

## Quick Start

### Enable Debug Mode

**Method 1: Command Line Flag**
```bash
python scripts/gather_metadata.py --debug
```

**Method 2: Environment Variable**
```bash
# Linux/Mac
export CLOUDS_DETANGLER_DEBUG=1
python scripts/gather_metadata.py

# Windows (CMD)
set CLOUDS_DETANGLER_DEBUG=1
python scripts/gather_metadata.py

# Windows (PowerShell)
$env:CLOUDS_DETANGLER_DEBUG="1"
python scripts/gather_metadata.py
```

### View Logs

All logs are automatically written to:
- **Windows**: `C:\Users\YourName\logs\clouds-detangler\`
- **Mac/Linux**: `~/logs/clouds-detangler/`

Each run creates a timestamped log file:
```
gather_metadata_20260120_143052.log
validate_setup_20260120_143105.log
```

## Log Levels

### INFO (Default)
Shows important operational messages:
```
INFO: Starting gather_metadata
INFO: Prerequisites check passed
INFO: Processing cloud 1/3: Google Drive
INFO: Successfully gathered metadata for Google Drive
```

### DEBUG (When --debug flag is used)
Shows detailed diagnostic information:
```
DEBUG: Log file: /home/user/logs/clouds-detangler/gather_metadata_20260120_143052.log
DEBUG: Debug mode: True
DEBUG: Loaded configuration for 3 clouds
DEBUG: Command: rclone lsjson gdrive_main: --recursive --hash
DEBUG: Return code: 0
DEBUG: ENTER run_lsjson(remote=gdrive_main, root=, include_shared=False)
DEBUG: VAR remote = gdrive_main
DEBUG: EXIT run_lsjson -> True
```

## Log File Format

Each log entry includes:
- **Timestamp**: When the event occurred
- **Logger name**: Script and module
- **Level**: INFO, DEBUG, WARNING, ERROR
- **Location**: Function name and line number
- **Message**: What happened

Example:
```
2026-01-20 14:30:52 - clouds_detangler.gather_metadata - INFO - main:89 - Starting metadata gathering
2026-01-20 14:30:52 - clouds_detangler.gather_metadata - DEBUG - main:95 - Loaded configuration for 3 clouds
2026-01-20 14:30:53 - clouds_detangler.gather_metadata - DEBUG - run_lsjson:31 - Command: rclone lsjson gdrive_main: --recursive --hash
```

## Using Breakpoints

When debug mode is enabled, you can set breakpoints in the code:

### Built-in Breakpoints

Some scripts have built-in breakpoints at critical points. When hit, they:
1. Log the breakpoint location
2. Show the call stack
3. Drop you into an interactive debugger (pdb)

### Interactive Debugger Commands

When you hit a breakpoint:
```
(Pdb) l          # List code around current position
(Pdb) n          # Next line
(Pdb) s          # Step into function
(Pdb) c          # Continue execution
(Pdb) p var      # Print variable value
(Pdb) pp var     # Pretty-print variable
(Pdb) w          # Show stack trace
(Pdb) h          # Help
(Pdb) q          # Quit debugger
```

Example session:
```bash
$ python scripts/gather_metadata.py --debug

Starting gather_metadata...
DEBUG: BREAKPOINT: Before processing clouds
DEBUG: Stack trace:
  File "gather_metadata.py", line 120, in main
    log.breakpoint("Before processing clouds")

> /path/to/gather_metadata.py(121)main()
-> for idx, cloud in enumerate(clouds, 1):
(Pdb) p clouds
[{'name': 'Google Drive', 'rclone_remote': 'gdrive_main', ...}]
(Pdb) c
Continuing...
```

## Logging Variables

Debug mode logs important variables:

```python
log.log_variable('remote', remote)           # VAR remote = gdrive_main
log.log_variable('file_count', len(files))   # VAR file_count = 1523
```

## Function Entry/Exit Tracking

Debug mode tracks function calls:

```python
log.log_function_entry('process_file', filename='test.txt')
# DEBUG: ENTER process_file(filename=test.txt)

result = process_file('test.txt')

log.log_function_exit('process_file', result=result)
# DEBUG: EXIT process_file -> True
```

## Error Logging

Errors are logged with full stack traces:

```python
try:
    risky_operation()
except Exception as e:
    log.exception("Operation failed")
    raise
```

Log output:
```
ERROR: Operation failed
Traceback (most recent call last):
  File "script.py", line 42, in main
    risky_operation()
  File "script.py", line 67, in risky_operation
    1 / 0
ZeroDivisionError: division by zero
```

## Finding Log Files

At the end of each script run, the log location is printed:

```
📝 Logs written to: /home/user/logs/clouds-detangler/gather_metadata_20260120_143052.log
   View logs with: cat /home/user/logs/clouds-detangler/gather_metadata_20260120_143052.log
   Or open with: less /home/user/logs/clouds-detangler/gather_metadata_20260120_143052.log
```

### View Recent Logs

**Linux/Mac:**
```bash
# View latest log
ls -t ~/logs/clouds-detangler/*.log | head -1 | xargs cat

# View with pager
ls -t ~/logs/clouds-detangler/*.log | head -1 | xargs less

# Follow log in real-time (in another terminal)
tail -f ~/logs/clouds-detangler/gather_metadata_20260120_143052.log
```

**Windows (PowerShell):**
```powershell
# View latest log
Get-ChildItem "$env:USERPROFILE\logs\clouds-detangler\*.log" | 
    Sort-Object LastWriteTime -Descending | 
    Select-Object -First 1 | 
    Get-Content

# Open in Notepad
Get-ChildItem "$env:USERPROFILE\logs\clouds-detangler\*.log" | 
    Sort-Object LastWriteTime -Descending | 
    Select-Object -First 1 | 
    ForEach-Object { notepad $_.FullName }
```

## Debugging Specific Issues

### Issue: Script hangs or runs slowly

**Solution:** Enable debug mode and check what command is running:

```bash
python scripts/gather_metadata.py --debug

# In the log, look for:
DEBUG: Command: rclone lsjson gdrive_main: --recursive --hash
# This shows exactly what's being executed
```

### Issue: rclone command fails

**Solution:** The full command and output are in the debug log:

```
DEBUG: Command: rclone lsjson gdrive_main: --recursive --hash
DEBUG: Return code: 1
ERROR: rclone lsjson failed for remote 'gdrive_main'
```

### Issue: Configuration not loading

**Solution:** Debug log shows the exact path and error:

```
DEBUG: Loading config from: /path/to/config/clouds.yaml
ERROR: Config file not found: /path/to/config/clouds.yaml
```

### Issue: Unknown error

**Solution:** Full stack trace in the log:

```
EXCEPTION: Operation failed
Traceback (most recent call last):
  [full stack trace here]
```

## Log Management

### Clean Old Logs

**Linux/Mac:**
```bash
# Delete logs older than 30 days
find ~/logs/clouds-detangler -name "*.log" -mtime +30 -delete

# Keep only last 10 logs
ls -t ~/logs/clouds-detangler/*.log | tail -n +11 | xargs rm
```

**Windows (PowerShell):**
```powershell
# Delete logs older than 30 days
Get-ChildItem "$env:USERPROFILE\logs\clouds-detangler\*.log" | 
    Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} | 
    Remove-Item

# Keep only last 10 logs
Get-ChildItem "$env:USERPROFILE\logs\clouds-detangler\*.log" | 
    Sort-Object LastWriteTime -Descending | 
    Select-Object -Skip 10 | 
    Remove-Item
```

### Archive Logs

```bash
# Linux/Mac
tar -czf ~/logs/clouds-detangler-archive-$(date +%Y%m%d).tar.gz \
    ~/logs/clouds-detangler/*.log

# Windows (PowerShell)
Compress-Archive -Path "$env:USERPROFILE\logs\clouds-detangler\*.log" `
    -DestinationPath "$env:USERPROFILE\logs\clouds-detangler-archive-$(Get-Date -Format 'yyyyMMdd').zip"
```

## Tips for Your Boys

### Learning to Debug

Debugging is a crucial programming skill! Here's what to do:

1. **Run with --debug first** when something doesn't work
2. **Read the log file** - it tells you what happened
3. **Look for ERROR or EXCEPTION** lines
4. **Check the stack trace** - it shows where the error occurred
5. **Use breakpoints** to pause and inspect

### Practice Exercise

Try this to learn debugging:

```bash
# 1. Run with debug mode
python scripts/gather_metadata.py --debug

# 2. Find the log file (it will print the location)
# 3. Open it in a text editor
# 4. Find these things:
#    - When did the script start? (look for "Starting")
#    - What commands were run? (look for "Command:")
#    - Were there any errors? (look for "ERROR")
#    - How long did it take? (check timestamps)

# 5. Extra credit: Set a breakpoint in the code
#    Edit gather_metadata.py and add:
#    if debug:
#        log.breakpoint("My first breakpoint!")
```

### Understanding Logs = Understanding Code

When you read logs, you're seeing:
- What the program is doing
- What decisions it's making
- What data it's working with

This helps you:
- Fix bugs
- Understand how programs work
- Become a better programmer!

## Getting Help

If you're stuck:

1. **Check the log file** - most answers are there
2. **Look for the ERROR message** - it usually explains the problem
3. **Check the documentation** - README.md, QUICKSTART.md, etc.
4. **Share the log file** - when asking for help, include the relevant log entries

---

*Happy debugging!* 🐛🔍

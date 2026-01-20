# Debugging Features Demo

This shows the new debugging and logging features in action.

## Example 1: Running with Debug Mode

```bash
$ python scripts/gather_metadata.py --debug
```

**Console Output:**
```
======================================================================
                  Clouds Detangler - Metadata Gathering
======================================================================

INFO: Starting gather_metadata
DEBUG: Log file: /home/user/logs/clouds-detangler/gather_metadata_20260120_143052.log
DEBUG: Debug mode: True

=== Checking prerequisites ===
[+] Prerequisites OK

INFO: Prerequisites check passed
DEBUG: Loaded configuration for 3 clouds

[+] Manifests will be saved to: /home/user/clouds-detangler/manifests

[+] Found 3 cloud(s) to scan

======================================================================
Cloud: Google Drive Main
======================================================================
INFO: Processing cloud 1/3: Google Drive Main
DEBUG: VAR remote = gdrive_main
DEBUG: VAR root = 
DEBUG: VAR include_shared = False
DEBUG: ENTER run_lsjson(remote=gdrive_main, root=, include_shared=False)
[2026-01-20T14:30:52] Running: rclone lsjson gdrive_main: --recursive --hash
DEBUG: Command: rclone lsjson gdrive_main: --recursive --hash
DEBUG: Return code: 0
[+] Wrote manifest for gdrive_main to /home/user/clouds-detangler/manifests/gdrive_main.json
DEBUG: EXIT run_lsjson -> True
INFO: Successfully gathered metadata for Google Drive Main

======================================================================
SUMMARY
======================================================================
✓ Successful: 3
✗ Failed: 0

Manifests saved to: /home/user/clouds-detangler/manifests
======================================================================
INFO: Completed: 3 successful, 0 failed

📝 Logs written to: /home/user/logs/clouds-detangler/gather_metadata_20260120_143052.log
   View logs with: cat /home/user/logs/clouds-detangler/gather_metadata_20260120_143052.log
   Or open with: less /home/user/logs/clouds-detangler/gather_metadata_20260120_143052.log
```

## Example 2: Log File Contents

**File:** `/home/user/logs/clouds-detangler/gather_metadata_20260120_143052.log`

```
2026-01-20 14:30:52 - clouds_detangler.gather_metadata - INFO - main:82 - Starting metadata gathering
2026-01-20 14:30:52 - clouds_detangler.gather_metadata - DEBUG - _setup_logging:82 - Log file: /home/user/logs/clouds-detangler/gather_metadata_20260120_143052.log
2026-01-20 14:30:52 - clouds_detangler.gather_metadata - DEBUG - _setup_logging:83 - Debug mode: True
2026-01-20 14:30:52 - clouds_detangler.gather_metadata - INFO - main:89 - Prerequisites check passed
2026-01-20 14:30:52 - clouds_detangler.gather_metadata - DEBUG - main:95 - Loaded configuration for 3 clouds
2026-01-20 14:30:52 - clouds_detangler.gather_metadata - INFO - main:110 - Processing {len(clouds)} clouds
2026-01-20 14:30:52 - clouds_detangler.gather_metadata - INFO - main:120 - Processing cloud 1/3: Google Drive Main
2026-01-20 14:30:52 - clouds_detangler.gather_metadata - DEBUG - main:121 - VAR remote = gdrive_main
2026-01-20 14:30:52 - clouds_detangler.gather_metadata - DEBUG - main:122 - VAR root = 
2026-01-20 14:30:52 - clouds_detangler.gather_metadata - DEBUG - main:123 - VAR include_shared = False
2026-01-20 14:30:52 - clouds_detangler.gather_metadata - DEBUG - run_lsjson:31 - ENTER run_lsjson(remote=gdrive_main, root=, include_shared=False)
2026-01-20 14:30:52 - clouds_detangler.gather_metadata - DEBUG - run_lsjson:42 - Command: rclone lsjson gdrive_main: --recursive --hash
2026-01-20 14:30:58 - clouds_detangler.gather_metadata - DEBUG - run_lsjson:47 - Return code: 0
2026-01-20 14:30:58 - clouds_detangler.gather_metadata - DEBUG - run_lsjson:74 - EXIT run_lsjson -> True
2026-01-20 14:30:58 - clouds_detangler.gather_metadata - INFO - main:133 - Successfully gathered metadata for Google Drive Main
2026-01-20 14:31:15 - clouds_detangler.gather_metadata - INFO - main:147 - Completed: 3 successful, 0 failed
```

## Example 3: Using Breakpoints

**Code with breakpoint:**
```python
# In gather_metadata.py
for idx, cloud in enumerate(clouds, 1):
    remote = cloud["rclone_remote"]
    
    if debug and remote == "gdrive_main":
        log.breakpoint("About to process Google Drive")
    
    # ... rest of processing
```

**What happens when breakpoint is hit:**
```
DEBUG: BREAKPOINT: About to process Google Drive
DEBUG: Stack trace:
  File "gather_metadata.py", line 120, in main
    log.breakpoint("About to process Google Drive")

> /path/to/gather_metadata.py(123)main()
-> root = cloud.get("root", "")
(Pdb) 
```

**Interactive debugger session:**
```
(Pdb) l
118     for idx, cloud in enumerate(clouds, 1):
119         remote = cloud["rclone_remote"]
120         
121         if debug and remote == "gdrive_main":
122             log.breakpoint("About to process Google Drive")
123  -> 
124         root = cloud.get("root", "")
125         include_shared = bool(cloud.get("include_shared", False))
126         name = cloud.get("name", remote)

(Pdb) p cloud
{'name': 'Google Drive Main', 'rclone_remote': 'gdrive_main', 'root': '', 'include_shared': False}

(Pdb) p remote
'gdrive_main'

(Pdb) p clouds
[{'name': 'Google Drive Main', ...}, {'name': 'OneDrive', ...}, {'name': 'Dropbox', ...}]

(Pdb) c
Continuing...
```

## Example 4: Error Logging

**When an error occurs:**
```python
try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
except Exception as e:
    log.exception("Failed to run rclone command")
    raise
```

**Log output:**
```
2026-01-20 14:35:22 - clouds_detangler.gather_metadata - ERROR - run_lsjson:50 - Failed to run rclone command
Traceback (most recent call last):
  File "/path/to/gather_metadata.py", line 46, in run_lsjson
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
  File "/usr/lib/python3.10/subprocess.py", line 505, in run
    with Popen(*popenargs, **kwargs) as process:
  File "/usr/lib/python3.10/subprocess.py", line 951, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
FileNotFoundError: [Errno 2] No such file or directory: 'rclone'
```

## Example 5: Finding and Reading Logs

**On Linux/Mac:**
```bash
# View the latest log
ls -t ~/logs/clouds-detangler/*.log | head -1 | xargs cat

# View in pager
ls -t ~/logs/clouds-detangler/*.log | head -1 | xargs less

# Search for errors
grep ERROR ~/logs/clouds-detangler/*.log

# Follow in real-time (in another terminal while script runs)
tail -f ~/logs/clouds-detangler/gather_metadata_20260120_143052.log
```

**On Windows (PowerShell):**
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

# Search for errors
Select-String -Path "$env:USERPROFILE\logs\clouds-detangler\*.log" -Pattern "ERROR"
```

## Example 6: Comparing Regular vs Debug Mode

**Regular mode (default):**
```
======================================================================
                  Clouds Detangler - Metadata Gathering
======================================================================

=== Checking prerequisites ===
[+] Prerequisites OK

[+] Manifests will be saved to: /home/user/clouds-detangler/manifests
[+] Found 3 cloud(s) to scan

======================================================================
Cloud: Google Drive Main
======================================================================
[2026-01-20T14:30:52] Running: rclone lsjson gdrive_main: --recursive --hash
[+] Wrote manifest for gdrive_main to /home/user/clouds-detangler/manifests/gdrive_main.json

======================================================================
SUMMARY
======================================================================
✓ Successful: 3
======================================================================
```

**Debug mode (--debug):**
```
======================================================================
                  Clouds Detangler - Metadata Gathering
======================================================================

INFO: Starting gather_metadata
DEBUG: Log file: /home/user/logs/clouds-detangler/gather_metadata_20260120_143052.log
DEBUG: Debug mode: True

=== Checking prerequisites ===
[+] Prerequisites OK

INFO: Prerequisites check passed
DEBUG: Loaded configuration for 3 clouds

[+] Manifests will be saved to: /home/user/clouds-detangler/manifests
INFO: Manifests directory: /home/user/clouds-detangler/manifests

[+] Found 3 cloud(s) to scan
INFO: Processing 3 clouds

======================================================================
Cloud: Google Drive Main
======================================================================
INFO: Processing cloud 1/3: Google Drive Main
DEBUG: VAR remote = gdrive_main
DEBUG: VAR root = 
DEBUG: VAR include_shared = False
DEBUG: ENTER run_lsjson(remote=gdrive_main, root=, include_shared=False)
[2026-01-20T14:30:52] Running: rclone lsjson gdrive_main: --recursive --hash
DEBUG: Command: rclone lsjson gdrive_main: --recursive --hash
DEBUG: Return code: 0
[+] Wrote manifest for gdrive_main to /home/user/clouds-detangler/manifests/gdrive_main.json
DEBUG: EXIT run_lsjson -> True
INFO: Successfully gathered metadata for Google Drive Main

======================================================================
SUMMARY
======================================================================
✓ Successful: 3
======================================================================
INFO: Completed: 3 successful, 0 failed

📝 Logs written to: /home/user/logs/clouds-detangler/gather_metadata_20260120_143052.log
   View logs with: cat /home/user/logs/clouds-detangler/gather_metadata_20260120_143052.log
```

## Key Differences

**Regular Mode:**
- Shows user-friendly messages
- Hides technical details
- No log file location shown
- Minimal output

**Debug Mode:**
- Shows all INFO and DEBUG messages
- Logs every operation
- Shows log file location at end
- Variable values
- Function calls
- Command details
- Return codes
- Much more verbose!

## When to Use Each

**Use Regular Mode When:**
- Everything is working fine
- You just want to get the job done
- You don't need technical details

**Use Debug Mode When:**
- Something is not working
- You want to understand what's happening
- You're learning how the code works
- You need to report a bug
- You're developing/testing new features

---

*With debugging enabled, you can see exactly what the program is doing at every step!* 🔍

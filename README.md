# Clouds Detangler

A toolkit to help you **untangle messy cloud storage** across multiple accounts.

This repo is designed for users who:
- Have files scattered across Google Drive / OneDrive / other cloud services
- Keep running out of storage space
- Know there are duplicate files everywhere but don't know where to start
- Want a safe, systematic way to see what they have and start organizing

The core workflow:

> **Look → Plan → Approve → Tidy → Log**

Clouds Detangler does **metadata-only** scanning first (no downloads, no changes), then helps you plan safe, server-side moves using `rclone`.

---

## Key Concepts

- Your files (photos, videos, docs) are stored as **binary data** – just 0s and 1s – on disks in data centers
- Cloud providers store **copies** of data across different servers for reliability
- Over time, you might upload the *same* file multiple times; the provider doesn't always detect this, and you pay for duplicate storage
- A **hash** (like MD5) is a short fingerprint of a file – if two files have identical hashes, they're almost certainly the exact same file
- Clouds Detangler groups files by hash to identify **real duplicates** across folders and even across different accounts
- A **WORM-style archive** (Write Once, Read Many) is a safe storage location for important files that won't be accidentally edited or deleted

You don't need deep technical knowledge to use this – but the code is open if you want to understand how it works.

---

## What This Tool Does

This version focuses on **Step 1: seeing what you have**.

- Reads a config file (`config/clouds.yaml`) listing your cloud accounts (as rclone remotes)
- Reads `config/paths.yaml` to know where to save outputs
- Uses `rclone lsjson` to fetch file metadata from each cloud (no downloads)
- Saves one JSON manifest per cloud in the `manifests/` folder

Future versions will:
- Build a deduplication index (grouping files by hash)
- Propose an action plan (keep / move / delete)
- Execute server-side moves into organized folders like `ref/pdf`, `ref/aac`, etc.

Right now, you get a safe, inspectable **snapshot** of your cloud storage.

---

## Quick Start

### Option 1: Interactive Setup Wizard (Recommended)

The easiest way to get started is using the interactive setup wizard:

```bash
python setup_wizard.py
```

This will guide you through:
1. Checking prerequisites
2. Configuring cloud storage remotes (with OAuth)
3. Creating configuration files
4. Validating your setup

### Option 2: Manual Setup

### 1. Prerequisites

- **Python 3.10+** installed
- **rclone** installed and on your PATH  
  Download from: https://rclone.org/downloads/

- At least one rclone remote configured, e.g.:
  - `gdrive_main` (Google Drive)
  - `gdrive_second` (second Google Drive)
  - `onedrive_main` (OneDrive)

Check your remotes with:

```bash
rclone listremotes
```

**New to rclone?** See `docs/RCLONE_SETUP.md` for a detailed walkthrough.

**New to command-line tools?** See `docs/FOR_BEGINNERS.md` - written for teens and parents!

### 2. Create Your Config

Copy the template config files and customize them:

```bash
cp config/template_clouds.yaml config/clouds.yaml
cp config/template_paths.yaml config/paths.yaml
```

Edit `config/clouds.yaml` to point to your rclone remotes.

### 3. Install Python Dependencies

From the repo folder:

```bash
pip install -r requirements.txt
```

### 4. Validate Your Setup

Run the validation script to check everything is configured correctly:

```bash
python scripts/validate_setup.py
```

### 5. Gather Metadata

Run:

```bash
python scripts/gather_metadata.py
```

If successful, JSON manifest files will appear in `manifests/`, e.g.:

- `manifests/gdrive_main.json`
- `manifests/gdrive_second.json`
- `manifests/onedrive_main.json`

Each file contains metadata for files in that cloud: path, size, hash, modified time, etc.

### 6. Debugging (Optional)

If something goes wrong, enable debug mode:

```bash
python scripts/gather_metadata.py --debug
```

This will:
- Show detailed diagnostic information
- Write logs to `~/logs/clouds-detangler/` (or `C:\Users\YourName\logs\clouds-detangler\` on Windows)
- Enable breakpoints for interactive debugging

See `docs/DEBUGGING.md` for full debugging guide.

---

## Advanced Features

### Evidence Routing

For users managing evidence files (photos, videos, documents), the toolkit includes:

- **`route_evidence.py`**: Routes files to multiple cloud locations with chain of custody logging
- **`route_evidence_batch.py`**: Batch processing for multiple files
- **`process_whatsapp.py`**: Specialized handling for WhatsApp exports

### Chain of Custody

The evidence routing scripts maintain a detailed chain of custody log with:
- SHA256 hashes for file verification
- Timestamp tracking
- Location history
- Verification of uploads

---

## For Students & Curious Learners

If you're studying Computer Science or just interested in how things work, this project demonstrates several concepts:

- **Binary data**: All files are ultimately streams of bits – 0s and 1s
- **Cloud storage**: Just means renting disk space on someone else's servers
- **Hashing**: A checksum technique to detect whether two files are identical
- **Abstraction**: Separating *what* we want (organized storage) from *how* tools achieve it (APIs, hashes, JSON)

Clouds Detangler is a practical example of using these concepts to solve a real-world problem: preventing your digital life from becoming chaos.

---

## Project Structure

```
clouds-detangler/
├── config/
│   ├── template_clouds.yaml    # Template for cloud configuration
│   └── template_paths.yaml     # Template for path configuration
├── scripts/
│   ├── utils.py                # Utility functions
│   ├── validate_setup.py       # Validate prerequisites and config
│   ├── gather_metadata.py      # Gather metadata from clouds
│   ├── build_index.py          # Build deduplication index
│   ├── plan_actions.py         # Plan deduplication actions
│   ├── execute_plan.py         # Execute planned actions
│   ├── route_evidence.py       # Route evidence files to clouds
│   ├── route_evidence_batch.py # Batch evidence routing
│   └── process_whatsapp.py     # Process WhatsApp exports
├── manifests/                  # Output directory for manifests
├── docs/                       # Documentation
└── requirements.txt            # Python dependencies
```

---

## Contributing

This is an open-source project. Contributions, bug reports, and suggestions are welcome!

---

## License

MIT License - see LICENSE file for details

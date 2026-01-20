#!/usr/bin/env python3
"""
Interactive setup wizard for Clouds Detangler

Provides a typeform-style guided interface to:
- Configure rclone remotes
- Set up cloud provider authentication
- Create configuration files
- Validate the setup
"""

import sys
import subprocess
import os
from pathlib import Path
from typing import Optional, List, Dict


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(text: str):
    """Print a styled header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.ENDC}\n")


def print_step(step: int, total: int, title: str):
    """Print a step indicator"""
    print(f"{Colors.BOLD}Step {step}/{total}: {title}{Colors.ENDC}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.ENDC}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")


def ask_yes_no(question: str, default: bool = True) -> bool:
    """Ask a yes/no question"""
    default_str = "Y/n" if default else "y/N"
    while True:
        response = input(f"{question} [{default_str}]: ").strip().lower()
        if not response:
            return default
        if response in ['y', 'yes']:
            return True
        if response in ['n', 'no']:
            return False
        print_error("Please answer 'y' or 'n'")


def ask_choice(question: str, choices: List[str], descriptions: Optional[List[str]] = None) -> str:
    """Ask user to choose from a list of options"""
    print(f"\n{question}")
    print()
    for i, choice in enumerate(choices, 1):
        desc = f" - {descriptions[i-1]}" if descriptions and i-1 < len(descriptions) else ""
        print(f"  {i}. {choice}{desc}")
    print()
    
    while True:
        try:
            response = input(f"Choose (1-{len(choices)}): ").strip()
            if not response:
                continue
            choice_num = int(response)
            if 1 <= choice_num <= len(choices):
                return choices[choice_num - 1]
            print_error(f"Please enter a number between 1 and {len(choices)}")
        except ValueError:
            print_error("Please enter a valid number")


def ask_text(question: str, default: str = "", required: bool = True) -> str:
    """Ask for text input"""
    default_str = f" [{default}]" if default else ""
    while True:
        response = input(f"{question}{default_str}: ").strip()
        if not response and default:
            return default
        if response or not required:
            return response
        print_error("This field is required")


def check_rclone_installed() -> bool:
    """Check if rclone is installed"""
    try:
        result = subprocess.run(['rclone', 'version'], capture_output=True, timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def find_rclone_executable() -> Optional[Path]:
    """Try to find rclone executable in common locations"""
    import shutil
    
    # First check if it's already in PATH
    rclone_path = shutil.which('rclone')
    if rclone_path:
        return Path(rclone_path)
    
    # Common download/install locations
    common_locations = []
    
    if os.name == 'nt':  # Windows
        common_locations = [
            Path.home() / 'Downloads' / 'rclone.exe',
            Path.home() / 'Downloads' / 'rclone-*' / 'rclone.exe',
            Path('C:/Program Files/rclone/rclone.exe'),
            Path('C:/rclone/rclone.exe'),
        ]
    else:  # macOS/Linux
        common_locations = [
            Path.home() / 'Downloads' / 'rclone',
            Path('/usr/local/bin/rclone'),
            Path('/usr/bin/rclone'),
            Path('/opt/rclone/rclone'),
        ]
    
    # Check each location
    for loc in common_locations:
        if '*' in str(loc):
            # Handle wildcards
            parent = loc.parent
            pattern = loc.name
            if parent.exists():
                matches = list(parent.glob(pattern))
                if matches:
                    return matches[0]
        elif loc.exists():
            return loc
    
    return None


def explain_path():
    """Explain what PATH is in simple terms"""
    print("\n" + "=" * 70)
    print(f"{Colors.BOLD}What is PATH?{Colors.ENDC}\n")
    print("PATH is a list of folders where your computer looks for programs.")
    print("When you type 'rclone' in the terminal, your computer searches")
    print("these folders to find the rclone program.\n")
    print("We need to add rclone to PATH so you can run it from anywhere.")
    print("=" * 70 + "\n")


def help_add_to_path():
    """Guide user through adding rclone to PATH"""
    print_header("Add rclone to PATH")
    
    print("Let's find rclone and add it to your PATH.\n")
    
    # Try to find rclone
    rclone_path = find_rclone_executable()
    
    if rclone_path:
        print_success(f"Found rclone at: {rclone_path}")
        rclone_dir = rclone_path.parent
    else:
        print_warning("Could not find rclone automatically.")
        print("\nDo you know where you downloaded/installed rclone?")
        
        while True:
            user_path = ask_text("Enter the full path to rclone (or 'skip' to skip)", required=False)
            if user_path.lower() == 'skip':
                return False
            
            check_path = Path(user_path)
            if check_path.exists():
                rclone_path = check_path
                rclone_dir = check_path.parent if check_path.is_file() else check_path
                print_success(f"Found rclone at: {rclone_path}")
                break
            else:
                print_error(f"File not found: {user_path}")
                if not ask_yes_no("Try again?"):
                    return False
    
    print()
    explain_path()
    
    # Platform-specific instructions
    if os.name == 'nt':  # Windows
        print(f"{Colors.BOLD}Option 1: Quick Method (This Session Only){Colors.ENDC}\n")
        print("Copy and paste this command in your terminal:\n")
        cmd = f'set PATH=%PATH%;{rclone_dir}'
        print(f"{Colors.CYAN}{cmd}{Colors.ENDC}\n")
        print(f"{Colors.YELLOW}Note: This only works until you close the terminal.{Colors.ENDC}\n")
        
        print(f"{Colors.BOLD}Option 2: Permanent Method (Recommended){Colors.ENDC}\n")
        print("1. Press Windows Key and search for 'Environment Variables'")
        print("2. Click 'Edit the system environment variables'")
        print("3. Click 'Environment Variables...' button")
        print("4. Under 'User variables', find and select 'Path'")
        print("5. Click 'Edit...'")
        print("6. Click 'New'")
        print(f"7. Paste this folder path: {Colors.CYAN}{rclone_dir}{Colors.ENDC}")
        print("8. Click 'OK' on all windows")
        print("9. Close and reopen your terminal\n")
        
        print(f"{Colors.BOLD}Option 3: PowerShell Command (Permanent){Colors.ENDC}\n")
        print(f"{Colors.YELLOW}⚠ Run PowerShell as Administrator, then paste this:{Colors.ENDC}\n")
        ps_cmd = f'[Environment]::SetEnvironmentVariable("Path", $env:Path + ";{rclone_dir}", "User")'
        print(f"{Colors.CYAN}{ps_cmd}{Colors.ENDC}\n")
        
    else:  # macOS/Linux
        shell = os.environ.get('SHELL', '/bin/bash')
        
        if 'zsh' in shell:
            rc_file = Path.home() / '.zshrc'
        elif 'bash' in shell:
            rc_file = Path.home() / '.bashrc'
        else:
            rc_file = Path.home() / '.profile'
        
        print(f"{Colors.BOLD}Option 1: Quick Method (This Session Only){Colors.ENDC}\n")
        print("Copy and paste this command in your terminal:\n")
        cmd = f'export PATH="$PATH:{rclone_dir}"'
        print(f"{Colors.CYAN}{cmd}{Colors.ENDC}\n")
        print(f"{Colors.YELLOW}Note: This only works until you close the terminal.{Colors.ENDC}\n")
        
        print(f"{Colors.BOLD}Option 2: Permanent Method (Recommended){Colors.ENDC}\n")
        print("Copy and paste this command in your terminal:\n")
        perm_cmd = f'echo \'export PATH="$PATH:{rclone_dir}"\' >> {rc_file}'
        print(f"{Colors.CYAN}{perm_cmd}{Colors.ENDC}\n")
        print(f"Then reload your shell with: {Colors.CYAN}source {rc_file}{Colors.ENDC}\n")
        
        print(f"{Colors.BOLD}Option 3: Move to System Folder{Colors.ENDC}\n")
        print("Copy and paste this command (may need to enter your password):\n")
        move_cmd = f'sudo mv {rclone_path} /usr/local/bin/'
        print(f"{Colors.CYAN}{move_cmd}{Colors.ENDC}\n")
    
    print("=" * 70)
    print(f"\n{Colors.BOLD}After adding to PATH:{Colors.ENDC}")
    print("1. Close and reopen your terminal (or reload shell)")
    print("2. Test by typing: rclone version")
    print("3. You should see the rclone version information\n")
    
    return ask_yes_no("Have you added rclone to PATH?", default=False)


def get_rclone_remotes() -> List[str]:
    """Get list of configured rclone remotes"""
    try:
        result = subprocess.run(
            ['rclone', 'listremotes'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return [line.strip().rstrip(':') for line in result.stdout.strip().split('\n') if line.strip()]
        return []
    except Exception:
        return []


def get_remote_info(remote: str) -> Dict[str, str]:
    """Get configuration info for a specific remote"""
    try:
        result = subprocess.run(
            ['rclone', 'config', 'show', remote],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            info = {}
            for line in result.stdout.split('\n'):
                if '=' in line and not line.startswith('['):
                    key, value = line.split('=', 1)
                    info[key.strip()] = value.strip()
            return info
        return {}
    except Exception:
        return {}


def test_remote_access(remote: str) -> bool:
    """Test if a remote is accessible (OAuth token still valid)"""
    try:
        result = subprocess.run(
            ['rclone', 'lsf', f'{remote}:', '--max-depth', '1'],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0
    except Exception:
        return False


def review_and_update_remotes() -> List[str]:
    """Review existing remotes and update if needed"""
    print_header("Review Existing rclone Remotes")
    
    remotes = get_rclone_remotes()
    
    if not remotes:
        print_info("No existing rclone remotes found.")
        print_info("You'll configure new remotes in the next step.\n")
        return []
    
    print(f"Found {len(remotes)} existing remote(s):\n")
    
    # Show all remotes with their status
    remote_status = {}
    
    for remote in remotes:
        info = get_remote_info(remote)
        remote_type = info.get('type', 'unknown')
        
        print(f"{Colors.BOLD}{remote}{Colors.ENDC}")
        print(f"  Type: {remote_type}")
        
        # Test access
        print(f"  Testing access...", end=' ', flush=True)
        is_accessible = test_remote_access(remote)
        
        if is_accessible:
            print_success("Working ✓")
            remote_status[remote] = 'working'
        else:
            print_error("Failed ✗ (may need reconnecting)")
            remote_status[remote] = 'needs_update'
        
        print()
    
    # Check if any need updating
    needs_update = [r for r, s in remote_status.items() if s == 'needs_update']
    
    if needs_update:
        print(f"{Colors.YELLOW}{'=' * 70}{Colors.ENDC}")
        print(f"{Colors.BOLD}Remotes that need updating:{Colors.ENDC}\n")
        for remote in needs_update:
            print(f"  ✗ {remote}")
        print(f"\n{Colors.YELLOW}{'=' * 70}{Colors.ENDC}\n")
        
        print(f"{Colors.BOLD}Why remotes fail:{Colors.ENDC}")
        print("  • OAuth tokens expired (need to log in again)")
        print("  • Passwords changed")
        print("  • Account permissions changed")
        print("  • Remote was deleted from cloud provider\n")
        
        if ask_yes_no("Would you like to update these remotes now?"):
            return update_remotes_interactive(needs_update, remotes)
    else:
        print_success("All remotes are working! ✓\n")
        
        if ask_yes_no("Would you like to update any remotes anyway?", default=False):
            return update_remotes_interactive(remotes, remotes)
    
    return remotes


def update_remotes_interactive(remotes_to_update: List[str], all_remotes: List[str]) -> List[str]:
    """Interactively update remotes with various methods"""
    print()
    print_info("Let's update your remotes.\n")
    
    # Ask about Bitwarden CLI
    use_bitwarden = False
    if ask_yes_no("Are you using Bitwarden CLI for password management?", default=False):
        use_bitwarden = True
        print()
        print_info("Great! Make sure you're logged into Bitwarden CLI:")
        print(f"  {Colors.CYAN}bw login{Colors.ENDC}")
        print(f"  {Colors.CYAN}bw unlock{Colors.ENDC}")
        print()
        print_info("You can retrieve passwords with:")
        print(f"  {Colors.CYAN}bw get password <item-name>{Colors.ENDC}\n")
        
        if not ask_yes_no("Are you logged into Bitwarden CLI?", default=False):
            print_warning("Please log in to Bitwarden CLI first, then run this wizard again.")
            use_bitwarden = False
    
    updated_remotes = []
    
    for remote in remotes_to_update:
        print(f"\n{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
        print(f"{Colors.BOLD}Updating: {remote}{Colors.ENDC}")
        print(f"{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")
        
        info = get_remote_info(remote)
        remote_type = info.get('type', 'unknown')
        
        print(f"Remote type: {remote_type}")
        
        # Show update options
        print(f"\n{Colors.BOLD}Update options:{Colors.ENDC}\n")
        print("1. Reconnect (re-authenticate with OAuth)")
        print("2. Reconfigure (edit all settings)")
        print("3. Delete and recreate")
        print("4. Skip this remote")
        
        if use_bitwarden:
            print("5. Update password from Bitwarden CLI")
        
        print()
        
        choice = ask_text("Choose an option (1-5)" if use_bitwarden else "Choose an option (1-4)", default="1")
        
        if choice == '1':
            # Reconnect (OAuth refresh)
            print()
            print_info(f"Reconnecting {remote}...")
            print_info("Your browser will open for authentication.\n")
            
            try:
                result = subprocess.run(['rclone', 'config', 'reconnect', f'{remote}:'])
                
                if result.returncode == 0:
                    # Test if it worked
                    if test_remote_access(remote):
                        print_success(f"Successfully reconnected {remote}!")
                        updated_remotes.append(remote)
                    else:
                        print_warning(f"Reconnect completed but access test failed.")
                        print_info(f"You may need to try 'Reconfigure' instead.")
                else:
                    print_error(f"Reconnect failed for {remote}")
            except Exception as e:
                print_error(f"Error reconnecting: {e}")
        
        elif choice == '2':
            # Reconfigure
            print()
            print_info(f"Opening configuration for {remote}...")
            print_info("You'll be guided through updating all settings.\n")
            
            try:
                subprocess.run(['rclone', 'config', 'update', remote])
                updated_remotes.append(remote)
            except Exception as e:
                print_error(f"Error reconfiguring: {e}")
        
        elif choice == '3':
            # Delete and recreate
            print()
            print_warning(f"This will DELETE the remote '{remote}' and let you create a new one.")
            
            if ask_yes_no(f"Are you sure you want to delete '{remote}'?", default=False):
                try:
                    # Delete
                    subprocess.run(['rclone', 'config', 'delete', remote])
                    print_success(f"Deleted {remote}")
                    
                    print()
                    print_info("Now let's create a new remote with the same name...")
                    subprocess.run(['rclone', 'config'])
                    
                    # Check if it was recreated
                    if remote in get_rclone_remotes():
                        updated_remotes.append(remote)
                except Exception as e:
                    print_error(f"Error during delete/recreate: {e}")
        
        elif choice == '4':
            # Skip
            print_info(f"Skipping {remote}")
        
        elif choice == '5' and use_bitwarden:
            # Update password from Bitwarden
            print()
            print_info("Retrieving password from Bitwarden CLI...\n")
            
            item_name = ask_text(f"Bitwarden item name for {remote}")
            
            print(f"\n{Colors.CYAN}Running: bw get password {item_name}{Colors.ENDC}\n")
            
            try:
                bw_result = subprocess.run(
                    ['bw', 'get', 'password', item_name],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if bw_result.returncode == 0:
                    password = bw_result.stdout.strip()
                    print_success("Password retrieved from Bitwarden!")
                    
                    print()
                    print_info("Now updating rclone config with new password...")
                    print_info("You'll need to enter this password when prompted.")
                    print()
                    
                    # Run config update
                    subprocess.run(['rclone', 'config', 'update', remote])
                    updated_remotes.append(remote)
                else:
                    print_error("Failed to retrieve password from Bitwarden")
                    print_info("Make sure you're logged in: bw login && bw unlock")
            except FileNotFoundError:
                print_error("Bitwarden CLI not found!")
                print_info("Install from: https://bitwarden.com/help/cli/")
            except Exception as e:
                print_error(f"Error retrieving from Bitwarden: {e}")
    
    print(f"\n{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.BOLD}Remote Update Summary{Colors.ENDC}")
    print(f"{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")
    print(f"Updated {len(updated_remotes)} remote(s)")
    
    if updated_remotes:
        print(f"\n{Colors.GREEN}Successfully updated:{Colors.ENDC}")
        for r in updated_remotes:
            print(f"  ✓ {r}")
    
    skipped = set(remotes_to_update) - set(updated_remotes)
    if skipped:
        print(f"\n{Colors.YELLOW}Skipped:{Colors.ENDC}")
        for r in skipped:
            print(f"  - {r}")
    
    print()
    
    return all_remotes


def configure_rclone_remote(provider: str) -> Optional[str]:
    """Guide user through rclone configuration"""
    print_info(f"Opening rclone configuration for {provider}...")
    print_info("Follow the prompts in your terminal to authenticate.")
    print_info("Your browser may open for OAuth authentication.\n")
    
    remote_name = ask_text("What would you like to name this remote?", 
                          default=provider.lower().replace(' ', '_'))
    
    print()
    
    # Run rclone config with interactive mode
    try:
        # We'll use rclone config in non-interactive mode for better control
        result = subprocess.run(['rclone', 'config'], text=True)
        
        if result.returncode == 0:
            # Verify the remote was created
            remotes = get_rclone_remotes()
            if remote_name in remotes:
                print_success(f"Remote '{remote_name}' configured successfully!")
                return remote_name
            else:
                print_warning(f"Remote '{remote_name}' not found. Did you complete the setup?")
                return None
        else:
            print_error("rclone configuration failed")
            return None
    except Exception as e:
        print_error(f"Error running rclone config: {e}")
        return None


def create_clouds_config(remotes: List[Dict[str, str]]):
    """Create clouds.yaml configuration"""
    config_path = Path('config/clouds.yaml')
    
    with open(config_path, 'w') as f:
        f.write("# Cloud storage configuration\n")
        f.write("# Generated by setup wizard\n\n")
        f.write("clouds:\n")
        
        for remote in remotes:
            f.write(f"  - name: \"{remote['name']}\"\n")
            f.write(f"    rclone_remote: \"{remote['remote']}\"\n")
            f.write(f"    root: \"{remote.get('root', '')}\"\n")
            f.write(f"    include_shared: {str(remote.get('include_shared', False)).lower()}\n")
            f.write("\n")
    
    print_success(f"Created {config_path}")


def create_paths_config():
    """Create paths.yaml configuration"""
    config_path = Path('config/paths.yaml')
    
    manifests_dir = ask_text("Where should manifests be saved?", default="./manifests")
    logs_dir = ask_text("Where should logs be saved?", default="./logs")
    db_path = ask_text("Where should the database be saved?", default="./clouds.duckdb")
    
    with open(config_path, 'w') as f:
        f.write("# Path configuration\n")
        f.write("# Generated by setup wizard\n\n")
        f.write(f"manifests_dir: \"{manifests_dir}\"\n")
        f.write(f"logs_dir: \"{logs_dir}\"\n")
        f.write(f"database_path: \"{db_path}\"\n")
    
    print_success(f"Created {config_path}")


def main():
    """Main setup wizard"""
    clear_screen()
    print_header("Clouds Detangler Setup Wizard")
    
    print(f"{Colors.BOLD}Welcome!{Colors.ENDC}")
    print("This wizard will help you set up Clouds Detangler.\n")
    print("We'll guide you through:")
    print("  1. Checking prerequisites")
    print("  2. Reviewing & updating existing remotes")
    print("  3. Configuring cloud storage remotes")
    print("  4. Creating configuration files")
    print("  5. Validating your setup\n")
    
    if not ask_yes_no("Ready to begin?"):
        print("\nSetup cancelled.")
        return 1
    
    # Step 1: Check prerequisites
    clear_screen()
    print_header("Prerequisites Check")
    print_step(1, 4, "Checking Prerequisites")
    
    # Check Python
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    if sys.version_info >= (3, 10):
        print_success(f"Python {python_version} installed")
    else:
        print_error(f"Python {python_version} is too old. Python 3.10+ required.")
        return 1
    
    # Check rclone
    if check_rclone_installed():
        print_success("rclone is installed and in PATH")
    else:
        print_error("rclone is not found in PATH")
        print()
        
        # Check if rclone exists but not in PATH
        rclone_path = find_rclone_executable()
        if rclone_path:
            print_info(f"Found rclone at: {rclone_path}")
            print_info("But it's not in your PATH, so we need to add it.\n")
            
            if ask_yes_no("Would you like help adding rclone to PATH?"):
                input("\nPress Enter to see instructions...")
                clear_screen()
                if help_add_to_path():
                    # Test again
                    if check_rclone_installed():
                        print_success("Great! rclone is now working!")
                    else:
                        print_warning("rclone still not found. You may need to restart your terminal.")
                        print_info("After restarting, run this wizard again: python setup_wizard.py")
                        if not ask_yes_no("Continue setup anyway?", default=False):
                            return 1
                else:
                    print_warning("Skipping PATH setup.")
                    if not ask_yes_no("Continue anyway?", default=False):
                        return 1
            else:
                if not ask_yes_no("Continue anyway?", default=False):
                    return 1
        else:
            print_info("rclone not found on your computer.")
            print_info("Download from: https://rclone.org/downloads/\n")
            
            print(f"{Colors.BOLD}Download Instructions:{Colors.ENDC}\n")
            print("1. Go to: https://rclone.org/downloads/")
            print("2. Download the version for your operating system")
            print("3. Extract the ZIP file")
            print("4. Note where you extracted it (like Downloads folder)")
            print("5. Run this wizard again after downloading\n")
            
            if not ask_yes_no("Continue anyway?", default=False):
                return 1
    
    # Check dependencies
    try:
        import yaml
        import dateutil
        print_success("Python dependencies installed")
    except ImportError as e:
        print_warning(f"Missing dependency: {e}")
        print_info("Run: pip install -r requirements.txt")
        if not ask_yes_no("Continue anyway?", default=False):
            return 1
    
    input("\nPress Enter to continue...")
    
    # Step 2: Review and update existing remotes
    clear_screen()
    print_header("Review & Update Existing Remotes")
    print_step(2, 5, "Review Existing Remotes")
    
    existing_remotes = review_and_update_remotes()
    
    input("\nPress Enter to continue...")
    
    # Step 3: Configure cloud remotes
    clear_screen()
    print_header("Configure Cloud Storage")
    print_step(3, 5, "Configure Cloud Remotes")
    
    existing_remotes = get_rclone_remotes()
    
    # Note: We already reviewed these in the previous step
    if existing_remotes:
        print_info(f"You have {len(existing_remotes)} existing remote(s) from the review step.\n")
    else:
        print_info("No existing remotes. Let's add some!\n")
    
    # Choose what to configure
    providers = {
        "Google Drive": "drive",
        "OneDrive": "onedrive",
        "Dropbox": "dropbox",
        "Backblaze B2": "b2",
        "Other / Manual": "manual"
    }
    
    configured_remotes = []
    
    if existing_remotes and ask_yes_no("Use existing remotes?"):
        # Let user select from existing remotes
        for remote in existing_remotes:
            if ask_yes_no(f"Include '{remote}' in configuration?"):
                name = ask_text(f"Display name for '{remote}'", default=remote.title())
                root = ask_text("Root folder (leave blank for entire remote)", default="", required=False)
                include_shared = False
                
                if 'drive' in remote.lower() or 'google' in remote.lower():
                    include_shared = ask_yes_no("Include 'Shared with me' files?", default=False)
                
                configured_remotes.append({
                    'name': name,
                    'remote': remote,
                    'root': root,
                    'include_shared': include_shared
                })
    
    # Option to add new remotes
    if ask_yes_no("Add new cloud remote?"):
        while True:
            provider = ask_choice(
                "Which cloud provider?",
                list(providers.keys()),
                [
                    "Google Drive, Google Workspace",
                    "OneDrive Personal, OneDrive for Business",
                    "Dropbox",
                    "Backblaze B2 (backup storage)",
                    "I'll configure it manually"
                ]
            )
            
            if provider == "Other / Manual":
                print_info("\nOpening rclone config...")
                print_info("Complete the configuration, then return here.\n")
                subprocess.run(['rclone', 'config'])
                
                # Ask for the remote name they created
                remote_name = ask_text("What did you name the remote?")
                remotes = get_rclone_remotes()
                
                if remote_name in remotes:
                    print_success(f"Found remote '{remote_name}'")
                    name = ask_text(f"Display name", default=remote_name.title())
                    root = ask_text("Root folder (leave blank for entire remote)", default="", required=False)
                    
                    configured_remotes.append({
                        'name': name,
                        'remote': remote_name,
                        'root': root,
                        'include_shared': False
                    })
                else:
                    print_error(f"Remote '{remote_name}' not found")
            else:
                # Guide through provider-specific setup
                remote_name = configure_rclone_remote(provider)
                if remote_name:
                    root = ask_text("Root folder (leave blank for entire remote)", default="", required=False)
                    include_shared = False
                    
                    if 'Google Drive' in provider:
                        include_shared = ask_yes_no("Include 'Shared with me' files?", default=False)
                    
                    configured_remotes.append({
                        'name': provider,
                        'remote': remote_name,
                        'root': root,
                        'include_shared': include_shared
                    })
            
            if not ask_yes_no("Add another cloud remote?", default=False):
                break
    
    if not configured_remotes:
        print_error("No remotes configured. Setup incomplete.")
        return 1
    
    input("\nPress Enter to continue...")
    
    # Step 4: Create configuration files
    clear_screen()
    print_header("Create Configuration Files")
    print_step(4, 5, "Create Configuration")
    
    # Ensure config directory exists
    Path('config').mkdir(exist_ok=True)
    
    # Create clouds.yaml
    print("\nCreating clouds.yaml...")
    create_clouds_config(configured_remotes)
    
    # Create paths.yaml
    print("\nCreating paths.yaml...")
    create_paths_config()
    
    print()
    print_success("Configuration files created!")
    
    input("\nPress Enter to continue...")
    
    # Step 5: Validate setup
    clear_screen()
    print_header("Validate Setup")
    print_step(5, 5, "Validate Configuration")
    
    print("Running validation...\n")
    
    try:
        result = subprocess.run([sys.executable, 'scripts/validate_setup.py'])
        
        if result.returncode == 0:
            print()
            print_success("Setup validation passed!")
        else:
            print()
            print_warning("Setup validation found some issues.")
            print_info("Review the output above and fix any problems.")
    except Exception as e:
        print_error(f"Could not run validation: {e}")
    
    # Final summary
    print()
    print_header("Setup Complete!")
    
    print(f"{Colors.BOLD}Next Steps:{Colors.ENDC}\n")
    print("1. Review your configuration in config/clouds.yaml")
    print("2. Run: python scripts/validate_setup.py")
    print("3. Gather metadata: python scripts/gather_metadata.py")
    print("4. Check manifests in the manifests/ directory\n")
    
    print(f"{Colors.BOLD}Documentation:{Colors.ENDC}\n")
    print("  - README.md - Full documentation")
    print("  - docs/QUICKSTART.md - Quick start guide")
    print("  - docs/RCLONE_SETUP.md - rclone configuration help\n")
    
    print(f"{Colors.GREEN}Thank you for using Clouds Detangler!{Colors.ENDC}\n")
    
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)

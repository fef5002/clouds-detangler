"""Utility functions for configuration management and validation."""

import sys
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional


def load_yaml(path: str | Path) -> Dict[str, Any]:
    """Load and parse a YAML configuration file.
    
    Args:
        path: Path to the YAML file (string or Path object)
        
    Returns:
        Parsed YAML content as a dictionary
        
    Raises:
        FileNotFoundError: If the config file doesn't exist
        yaml.YAMLError: If the YAML syntax is invalid
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Config file not found: {path}\n"
            f"Expected location: {path.absolute()}"
        )
    
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if data is None:
                return {}
            return data
    except yaml.YAMLError as e:
        raise yaml.YAMLError(
            f"Invalid YAML syntax in {path}:\n{e}"
        ) from e


def get_paths_config() -> Dict[str, str]:
    """Load paths configuration from config/paths.yaml.
    
    Returns:
        Dictionary with path configurations (manifests_dir, logs_dir, etc.)
    """
    config = load_yaml("config/paths.yaml")
    
    # Validate expected keys
    if "manifests_dir" not in config:
        print("[!] Warning: 'manifests_dir' not found in paths.yaml, using default './manifests'")
        config["manifests_dir"] = "./manifests"
    
    return config


def get_clouds_config() -> Dict[str, List[Dict[str, Any]]]:
    """Load clouds configuration from config/clouds.yaml.
    
    Returns:
        Dictionary containing list of cloud configurations
        
    Raises:
        ValueError: If the configuration is invalid or missing required fields
    """
    config = load_yaml("config/clouds.yaml")
    
    if "clouds" not in config:
        raise ValueError(
            "Invalid clouds.yaml: missing 'clouds' key.\n"
            "See config/template_clouds.yaml for an example."
        )
    
    clouds = config.get("clouds", [])
    if not clouds:
        print("[!] Warning: No clouds configured in clouds.yaml")
        return config
    
    # Validate each cloud entry
    for idx, cloud in enumerate(clouds):
        if not isinstance(cloud, dict):
            raise ValueError(f"Cloud entry {idx} is not a dictionary")
        
        if "rclone_remote" not in cloud:
            raise ValueError(
                f"Cloud entry {idx} ('{cloud.get('name', 'unnamed')}') "
                f"is missing required field 'rclone_remote'"
            )
    
    return config


def validate_rclone_available() -> bool:
    """Check if rclone is installed and available on PATH.
    
    Returns:
        True if rclone is available, False otherwise
    """
    import subprocess
    
    try:
        result = subprocess.run(
            ["rclone", "version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def check_prerequisites(verbose: bool = True) -> bool:
    """Verify that all prerequisites are met before running operations.
    
    Args:
        verbose: If True, print detailed messages about what's missing
        
    Returns:
        True if all prerequisites are met, False otherwise
    """
    all_ok = True
    
    # Check if rclone is available
    if not validate_rclone_available():
        if verbose:
            print("[!] ERROR: rclone is not installed or not on PATH")
            print("    Install from: https://rclone.org/downloads/")
        all_ok = False
    
    # Check config files exist
    config_dir = Path("config")
    required_configs = ["clouds.yaml", "paths.yaml"]
    
    for config_file in required_configs:
        config_path = config_dir / config_file
        if not config_path.exists():
            if verbose:
                template = config_dir / f"template_{config_file}"
                print(f"[!] ERROR: Missing {config_path}")
                if template.exists():
                    print(f"    Copy from template: cp {template} {config_path}")
            all_ok = False
    
    return all_ok


def ensure_directory(path: str | Path, description: str = "directory") -> Path:
    """Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path to ensure exists
        description: Human-readable description for error messages
        
    Returns:
        Path object for the directory
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

from .exceptions import ConfigurationError

# Default configuration file locations
DEFAULT_CONFIG_FILE = os.path.join(os.environ.get("HOME", ""), ".tkio_config.json")
DEFAULT_API_URL = "https://api.terrak.io"

def read_config_file(config_file: str = DEFAULT_CONFIG_FILE) -> Dict[str, Any]:
    """
    Read and parse the configuration file.
    
    Args:
        config_file: Path to the configuration file
        
    Returns:
        Dict[str, Any]: Configuration parameters
        
    Raises:
        ConfigurationError: If the configuration file can't be read or parsed
    """
    config_path = Path(os.path.expanduser(config_file))
    
    if not config_path.exists():
        raise ConfigurationError(
            f"Configuration file not found: {config_file}\n"
            f"Please create a file at {config_file} with the following format:\n"
            '{\n  "EMAIL": "your-email@example.com",\n  "TERRAKIO_API_KEY": "your-api-key-here"\n}'
        )
    
    try:
        with open(config_path, 'r') as f:
            config_data = json.load(f)
            
        # Convert the JSON config to our expected format
        config = {
            # Allow config to override default URL if provided
            'url': config_data.get('TERRAKIO_API_URL', DEFAULT_API_URL),
            'key': config_data.get('TERRAKIO_API_KEY')
        }
        return config
            
    except Exception as e:
        raise ConfigurationError(f"Failed to parse configuration file: {e}")

def create_default_config(email: str, api_key: str, api_url: Optional[str] = None, config_file: str = DEFAULT_CONFIG_FILE) -> None:
    """
    Create a default configuration file in JSON format.
    
    Args:
        email: User email
        api_key: Terrakio API key
        api_url: Optional API URL (if different from default)
        config_file: Path to configuration file
        
    Raises:
        ConfigurationError: If the configuration file can't be created
    """
    config_path = Path(os.path.expanduser(config_file))
    
    # Ensure directory exists
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        config_data = {
            "EMAIL": email,
            "TERRAKIO_API_KEY": api_key
        }
        
        # Add API URL if provided
        if api_url:
            config_data["TERRAKIO_API_URL"] = api_url
        
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=2)
            
    except Exception as e:
        raise ConfigurationError(f"Failed to create configuration file: {e}")
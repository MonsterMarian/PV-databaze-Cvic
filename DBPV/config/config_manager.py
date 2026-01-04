"""
Configuration Management for E-commerce Application
"""
import json
import os
from typing import Dict, Any


class Config:
    """Configuration class to manage application settings"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.settings = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file, create default if not exists"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Create default configuration
            default_config = {
                "database": {
                    "server": "PC000",
                    "database": "app1",
                    "username": "app1user",
                    "password": "student",
                    "driver": "ODBC Driver 17 for SQL Server"
                },
                "application": {
                    "name": "E-commerce Application",
                    "version": "1.0.0",
                    "debug": True,
                    "log_level": "INFO"
                },
                "paths": {
                    "data_import_dir": "./data/import",
                    "reports_dir": "./reports",
                    "logs_dir": "./logs"
                }
            }
            self.save_config(default_config)
            return default_config
    
    def save_config(self, config: Dict[str, Any] = None) -> None:
        """Save configuration to file"""
        config_to_save = config if config is not None else self.settings
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config_to_save, f, indent=4, ensure_ascii=False)
    
    def get_database_connection_string(self) -> str:
        """Generate database connection string from config"""
        db_config = self.settings["database"]
        return (
            f"DRIVER={{{db_config['driver']}}};"
            f"SERVER={db_config['server']};"
            f"DATABASE={db_config['database']};"
            f"UID={db_config['username']};"
            f"PWD={db_config['password']}"
        )
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation (e.g., 'database.server')"""
        keys = key.split('.')
        value = self.settings
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value using dot notation"""
        keys = key.split('.')
        config_ref = self.settings
        
        for k in keys[:-1]:
            if k not in config_ref:
                config_ref[k] = {}
            config_ref = config_ref[k]
        
        config_ref[keys[-1]] = value
        self.save_config()


# Example usage
if __name__ == "__main__":
    # Create config instance
    config = Config()
    
    # Print database connection string
    print("Database Connection String:")
    print(config.get_database_connection_string())
    
    # Print all settings
    print("\nAll Settings:")
    print(json.dumps(config.settings, indent=2, ensure_ascii=False))
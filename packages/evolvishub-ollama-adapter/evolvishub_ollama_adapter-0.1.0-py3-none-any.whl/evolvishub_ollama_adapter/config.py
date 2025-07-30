"""
Configuration management for the Ollama adapter.
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from configparser import ConfigParser

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

class Config:
    """Configuration manager for Ollama adapter."""
    
    YAML_AVAILABLE = YAML_AVAILABLE
    
    def __init__(self, config_path: Optional[str] = None, config_type: str = "ini"):
        """Initialize configuration.
        
        Args:
            config_path: Path to configuration file
            config_type: Type of configuration file ("ini" or "yaml")
        """
        self.config_type = config_type
        self.config_path = config_path or os.getenv("OLLAMA_CONFIG", os.path.expanduser("~/.ollama/config.ini"))
        
        if config_type == "ini":
            self.config = ConfigParser()
        else:
            self.config = {}
            
        self.load()
        
    def load(self) -> None:
        """Load configuration from file."""
        if os.path.exists(self.config_path):
            if self.config_type == "ini":
                self.config.read(self.config_path)
            else:
                with open(self.config_path, "r") as f:
                    self.config = yaml.safe_load(f)
        else:
            self._create_default_config()
            
    def save(self, path: Optional[str] = None) -> None:
        """Save configuration to file.
        
        Args:
            path: Optional path to save configuration to
        """
        save_path = path or self.config_path
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        if self.config_type == "ini":
            with open(save_path, "w") as f:
                self.config.write(f)
        else:
            with open(save_path, "w") as f:
                yaml.dump(self.config, f)
                
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        if self.config_type == "ini":
            if not self.config.has_section(section):
                return default
            if not self.config.has_option(section, key):
                return default
            value = self.config.get(section, key, fallback=default)
            return value if value is not None else default
        else:
            if section not in self.config or key not in self.config[section]:
                return default
            value = self.config.get(section, {}).get(key, default)
            return value if value is not None else default
            
    def set(self, section: str, key: str, value: Any) -> None:
        """Set configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            value: Configuration value
        """
        if self.config_type == "ini":
            if not self.config.has_section(section):
                self.config.add_section(section)
            self.config.set(section, key, str(value))
        else:
            if section not in self.config:
                self.config[section] = {}
            self.config[section][key] = value
            
    def get_int(self, section: str, key: str, default: Optional[int] = None) -> Optional[int]:
        """Get integer configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Integer configuration value
        """
        value = self.get(section, key, default)
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
            
    def get_float(self, section: str, key: str, default: Optional[float] = None) -> Optional[float]:
        """Get float configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Float configuration value
        """
        value = self.get(section, key, default)
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
            
    def get_bool(self, section: str, key: str, default: Optional[bool] = None) -> Optional[bool]:
        """Get boolean configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Boolean configuration value
        """
        value = self.get(section, key, default)
        if value is None:
            return None
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "yes", "1", "on")
        return bool(value)
        
    def get_list(self, section: str, key: str, default: Optional[List[Any]] = None) -> Optional[List[Any]]:
        """Get list configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            List configuration value
        """
        value = self.get(section, key, default)
        if value is None:
            return None
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [x.strip() for x in value.split(",")]
        return [value]
        
    def _create_default_config(self) -> None:
        """Create default configuration."""
        if self.config_type == "ini":
            self.config["Ollama"] = {
                "base_url": "http://localhost:11434",
                "timeout": "120",
                "retries": "3"
            }
            self.config["Model"] = {
                "name": "llama2",
                "temperature": "0.7",
                "top_p": "0.9",
                "top_k": "40",
                "repeat_penalty": "1.1"
            }
            self.config["Data"] = {
                "chunk_size": "1000",
                "overlap": "100",
                "max_tokens": "2048"
            }
            self.config["File"] = {
                "formats": ".txt,.md,.rst,.py,.js,.html,.css,.json,.xml,.yaml,.yml",
                "max_size": "10485760"
            }
            self.config["Logging"] = {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": "ollama.log"
            }
        else:
            self.config = {
                "Ollama": {
                    "base_url": "http://localhost:11434",
                    "timeout": 120,
                    "retries": 3
                },
                "Model": {
                    "name": "llama2",
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 40,
                    "repeat_penalty": 1.1
                },
                "Data": {
                    "chunk_size": 1000,
                    "overlap": 100,
                    "max_tokens": 2048
                },
                "File": {
                    "formats": [".txt", ".md", ".rst", ".py", ".js", ".html", ".css", ".json", ".xml", ".yaml", ".yml"],
                    "max_size": 10485760
                },
                "Logging": {
                    "level": "INFO",
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    "file": "ollama.log"
                }
            }
            
    # Backward compatibility aliases
    getint = get_int
    getfloat = get_float
    getboolean = get_bool
    getlist = get_list
    
    def get_model_options(self) -> Dict[str, Any]:
        """Get model options as dictionary.
        
        Returns:
            Dictionary of model options
        """
        return {
            "temperature": self.get_float("Model", "temperature", 0.7),
            "top_p": self.get_float("Model", "top_p", 0.9),
            "top_k": self.get_int("Model", "top_k", 40),
            "repeat_penalty": self.get_float("Model", "repeat_penalty", 1.1),
            "num_ctx": self.get_int("Data", "max_tokens", 2048),
            "num_thread": self.get_int("Model", "num_thread", 4),
            "num_gpu": self.get_int("Model", "num_gpu", 1),
            "repeat_last_n": self.get_int("Model", "repeat_last_n", 64),
            "seed": self.get_int("Model", "seed", 42),
            "stop": self.get_list("Model", "stop", ["\n", "Human:"]),
            "tfs_z": self.get_float("Model", "tfs_z", 1.0),
            "num_predict": self.get_int("Model", "num_predict", 128),
            "typical_p": self.get_float("Model", "typical_p", 0.9),
            "mirostat": self.get_int("Model", "mirostat", 0),
            "mirostat_eta": self.get_float("Model", "mirostat_eta", 0.1),
            "mirostat_tau": self.get_float("Model", "mirostat_tau", 5.0),
            "presence_penalty": self.get_float("Model", "presence_penalty", 0.0),
            "frequency_penalty": self.get_float("Model", "frequency_penalty", 0.0)
        }
        
    def get_file_patterns(self) -> Dict[str, List[str]]:
        """Get file patterns for different file types.
        
        Returns:
            Dictionary of file patterns
        """
        return {
            "text": [".txt", ".md", ".rst"],
            "code": [".py", ".js", ".ts", ".java", ".cpp", ".c", ".cs", ".go", ".rb", ".php", ".swift", ".kt", ".rs", ".scala", ".pl", ".sh", ".bat", ".ps1", ".lua", ".r", ".m", ".jl", ".dart", ".sql"],
            "web": [".html", ".css", ".js", ".ts"],
            "data": [".json", ".xml", ".yaml", ".yml"],
            "binary": ["bin", "dat", "model", "weights"]
        }
        
    def get_storage_paths(self) -> Dict[str, Path]:
        """Get storage paths for different data types.
        
        Returns:
            Dictionary of storage paths
        """
        base_path = Path(os.path.expanduser("~/.ollama"))
        return {
            "models": base_path / "models",
            "data": base_path / "data",
            "cache": base_path / "cache",
            "logs": base_path / "logs",
            "temp": base_path / "temp"
        }
        
    def get_base_url(self) -> str:
        """Get base URL for Ollama API.
        
        Returns:
            Base URL string
        """
        return self.get("Ollama", "base_url", "http://localhost:11434").rstrip("/")
        
    def get_timeout(self) -> int:
        """Get timeout for API requests.
        
        Returns:
            Timeout in seconds
        """
        return self.get_int("Ollama", "timeout", 120)
        
    def get_retries(self) -> int:
        """Get number of retries for API requests.
        
        Returns:
            Number of retries
        """
        return self.get_int("Ollama", "retries", 3)
        
    def get_model_name(self) -> str:
        """Get default model name.
        
        Returns:
            Model name
        """
        return self.get("Model", "name", "llama2")
        
    def get_chunk_size(self) -> int:
        """Get chunk size for data processing.
        
        Returns:
            Chunk size in tokens
        """
        return self.get_int("Data", "chunk_size", 1000)
        
    def get_overlap(self) -> int:
        """Get overlap size for data processing.
        
        Returns:
            Overlap size in tokens
        """
        return self.get_int("Data", "overlap", 100)
        
    def get_max_tokens(self) -> int:
        """Get maximum number of tokens.
        
        Returns:
            Maximum number of tokens
        """
        return self.get_int("Data", "max_tokens", 2048)
        
    def get_file_formats(self) -> List[str]:
        """Get supported file formats.
        
        Returns:
            List of file formats
        """
        return self.get_list("File", "formats", [".txt", ".md", ".rst", ".py", ".js", ".html", ".css", ".json", ".xml", ".yaml", ".yml"])
        
    def get_max_file_size(self) -> int:
        """Get maximum file size.
        
        Returns:
            Maximum file size in bytes
        """
        return self.get_int("File", "max_size", 10485760)
        
    def get_log_level(self) -> str:
        """Get logging level.
        
        Returns:
            Logging level
        """
        return self.get("Logging", "level", "INFO")
        
    def get_log_format(self) -> str:
        """Get logging format.
        
        Returns:
            Logging format
        """
        return self.get("Logging", "format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        
    def get_log_file(self) -> str:
        """Get log file path.
        
        Returns:
            Log file path
        """
        return self.get("Logging", "file", "ollama.log") 
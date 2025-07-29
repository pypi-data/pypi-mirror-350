"""
Core functionality for the konfigure package.

This module provides the main classes and functions for working with YAML configuration files.
"""

import copy
import os
import yaml
import jinja2
from typing import Any, Dict, List, Optional, Union


class StringTemplate(str):
    """A string class that can be parsed as a Jinja template."""
    
    def __init__(self, content):
        """Initialize with the raw string content."""
        self.raw_string = str(content)
    
    def render(self, **kwargs):
        """Render the string as a Jinja template."""
        template = jinja2.Template(self.raw_string)
        return template.render(**kwargs)
    
    def __str__(self):
        return self.raw_string
    
    def __repr__(self):
        return f"StringTemplate({repr(self.raw_string)})"
    
    def __eq__(self, other):
        if isinstance(other, StringTemplate):
            return self.raw_string == other.raw_string
        return self.raw_string == other


class Config(dict):
    """Enhanced dictionary with dot notation access and Jinja2 template rendering."""

    def __init__(self, dict_value=None, yaml_path=None, parent=None, parent_key=None):
        """Initialize a Config object.
        
        Args:
            dict_value: Dictionary to initialize with
            yaml_path: Path to the YAML file this config is associated with
            parent: Parent Config object if this is a nested config
            parent_key: Key in the parent that this config is stored under
        """
        dict_value = dict_value or {}
        super().__init__(dict_value)
        self._yaml_path = yaml_path
        self._parent = parent
        self._parent_key = parent_key
        self._convert_to_config()

    def _convert_to_config(self):
        """Recursively convert nested dictionaries to Config objects."""
        for key, value in list(self.items()):  # Use list to avoid modifying during iteration
            self[key] = self._convert_value(value, key)

    def _convert_value(self, value, key=None):
        """Recursively convert a value to its appropriate type."""
        if isinstance(value, dict) and not isinstance(value, Config):
            return Config(value, yaml_path=None, parent=self, parent_key=key)
        elif isinstance(value, list):
            return [self._convert_value(item) for item in value]
        elif isinstance(value, (int, float, bool, type(None))):
            return value
        elif isinstance(value, str):
            return StringTemplate(value)
        elif isinstance(value, Config):
            # Update parent reference if it's a Config
            value._parent = self
            value._parent_key = key
            return value
        else:
            return value

    def __getattr__(self, key):
        """Get an attribute from the Config using dot notation."""
        # Ignore special methods
        if key.startswith('__') and key.endswith('__'):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")
        try:
            return self[key]
        except KeyError:
            return None

    def _process_value(self, value, key=None):
        """Process a value to ensure it's in the correct format for Config storage."""
        if isinstance(value, str) and not isinstance(value, StringTemplate):
            return StringTemplate(value)
        elif isinstance(value, dict) and not isinstance(value, Config):
            return Config(value, yaml_path=None, parent=self, parent_key=key)
        elif isinstance(value, list):
            return [self._process_value(item) for item in value]
        return value

    def __setitem__(self, key, value):
        """Set an item in the Config."""
        if key in ('_yaml_path', '_parent', '_parent_key'):
            super().__setitem__(key, value)
            return
        processed_value = self._process_value(value, key)
        super().__setitem__(key, processed_value)

    def __setattr__(self, key, value):
        """Set an attribute in the Config using dot notation."""
        if key in ('_yaml_path', '_parent', '_parent_key'):
            super().__setattr__(key, value)
            return
        if key.startswith('__') and key.endswith('__'):
            super().__setattr__(key, value)
        else:
            self[key] = value

    def __delattr__(self, key):
        """Delete an attribute from the Config."""
        if key.startswith('__') and key.endswith('__'):
            super().__delattr__(key)
        else:
            try:
                del self[key]
            except KeyError:
                # Silently ignore if the key doesn't exist
                pass

    def __deepcopy__(self, memo):
        """Create a deep copy of the Config."""
        return Config(copy.deepcopy(dict(self), memo))

    def _to_serializable(self):
        """Convert the Config to a serializable dictionary."""
        def _serialize(v):
            if isinstance(v, Config):
                return v._to_serializable()
            elif isinstance(v, StringTemplate):
                return v.raw_string
            elif isinstance(v, list):
                return [_serialize(item) for item in v]
            elif isinstance(v, dict):
                return {k: _serialize(val) for k, val in v.items()}
            elif isinstance(v, (str, int, float, bool, type(None))):
                return v
            else:
                return str(v)
        
        # Create a new dictionary with converted values
        result = {}
        
        # Process each key-value pair in the Config
        for k, v in list(self.items()):
            if k.startswith('_'):
                continue
            # Convert all other values to serializable format
            result[k] = _serialize(v)
            
        return result


def load(file_path) -> Config:
    """Load a YAML file into a Config object.
    
    Args:
        file_path: Path to the YAML file to load
        
    Returns:
        Config object with the loaded data
    """
    # Make file_path absolute if it's not already
    full_path = os.path.abspath(file_path)
    
    # If file doesn't exist, create a new empty Config
    if not os.path.exists(full_path):
        config = Config({})
        config._yaml_path = full_path
        return config
    
    try:
        with open(full_path, 'r') as f:
            data = yaml.safe_load(f) or {}
            config = Config(data)
            config._yaml_path = full_path
            return config
    except Exception as e:
        print(f"Warning: Failed to load config from {file_path}: {str(e)}")
        # Create new config if loading fails
        config = Config({})
        config._yaml_path = full_path
        return config


def dump(config, file_path=None):
    """Save a Config object to a YAML file.
    
    Args:
        config: Config object to save
        file_path: Path to save the YAML file to. If None, uses the path the Config was loaded from.
        
    Returns:
        True if successful, False otherwise
    """
    if not isinstance(config, Config):
        raise TypeError("Can only dump Config objects")
    
    # Use the provided file_path or the one from the Config
    yaml_path = file_path or config._yaml_path
    if not yaml_path:
        raise ValueError("No file path provided and Config has no associated file path")
    
    # Make yaml_path absolute if it's not already
    full_path = os.path.abspath(yaml_path)
    
    try:
        # Ensure directory exists
        directory = os.path.dirname(full_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        # Convert to serializable format
        serializable_data = config._to_serializable()
        
        # Write to file
        with open(full_path, 'w') as f:
            yaml.dump(
                serializable_data,
                f,
                default_flow_style=False,
                sort_keys=False,
                indent=2,
                width=100,
                allow_unicode=True
            )
        return True
    except Exception as e:
        print(f"Warning: Failed to save config to {full_path}: {str(e)}")
        return False

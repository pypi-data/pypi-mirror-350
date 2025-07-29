"""
Konfigure - A YAML-based configuration management tool for separating code from prompts in LLMs.

This package provides a simple way to load, manipulate, and save YAML configuration files
with dot notation access and Jinja2 template rendering capabilities.
"""

from .core import load, dump, Config

__all__ = ['load', 'dump', 'Config']

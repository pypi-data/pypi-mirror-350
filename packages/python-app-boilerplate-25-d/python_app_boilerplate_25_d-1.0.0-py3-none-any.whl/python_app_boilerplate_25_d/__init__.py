# src/python_app_boilerplate_25_d/__init__.py

"""Boilerplate package."""

import importlib.metadata

try:
  __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
  __version__ = "0.0.0"

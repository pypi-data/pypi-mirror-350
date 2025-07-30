"""Viruses

This subpackage provides access to classes useful for modeling
viral systems.
"""
from . import virus

from .virus import Virus


__all__ = [
    # ─── modules ─────────────────────────────────────────────────────────────
    "virus",

    # ─── classes ─────────────────────────────────────────────────────────────
    "Virus"
]
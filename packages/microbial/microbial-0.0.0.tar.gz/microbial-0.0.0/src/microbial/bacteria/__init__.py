"""Bacteria

This subpackage provides access to classes useful for modeling
bacterial systems.
"""

from . import bacterium

from .bacterium import Bacterium


__all__ = [
    # ─── modules ─────────────────────────────────────────────────────────────
    "bacterium",

    # ─── classes ─────────────────────────────────────────────────────────────
    "Bacterium"
]
"""Microbial

Utilities for modeling various microbiological systems.
"""
# ─── import statements ────────────────────────────────────────────────── ✦✦ ─
from . import bacteria, fungi, genomics, phylogeny, viruses

from .phylogeny import Phylogeny

from .bacteria import Bacterium
from .fungi import Fungus
from .genomics import Genome, BacterialGenome, FungalGenome, ViralGenome
from .viruses import Virus


__all__ = [
    # ─── modules ─────────────────────────────────────────────────────────────
    "bacteria",
    "fungi",
    "genomics",
    "phylogeny",
    "viruses",

    # ─── classes ─────────────────────────────────────────────────────────────
    "BacterialGenome",
    "Bacterium",
    "FungalGenome",
    "Fungus",
    "Genome",
    "Phylogeny",
    "ViralGenome",
    "Virus"
]
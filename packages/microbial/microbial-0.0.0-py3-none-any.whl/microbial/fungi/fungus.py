"""Fungus

Utilities for modeling various fungal systems.
"""
# ─── import statements ────────────────────────────────────────────────── ✦✦ ─
import logging

from typing import Optional

from platformdirs import user_log_dir

from ..genomics import FungalGenome
from ..phylogeny import Phylogeny

# ─── helpers ──────────────────────────────────────────────────────────── ✦✦ ─
#
# Initialize the logger.
logging.basicConfig(filename=user_log_dir("microbial", "C. W. Rice"), level=logging.INFO)
logger = logging.getLogger(__name__)


# ─── model ────────────────────────────────────────────────────────────── ✦✦ ─
#
# Define the fungal model.
class Fungus:
    def __init__(
        self,
        genome: Optional[FungalGenome] = None,
        phylogeny: Optional[Phylogeny] = None
    ) -> None:
        self.phylogeny = phylogeny
        if self.phylogeny:
            self.genus = phylogeny.genus
            self.species = phylogeny.species
        else:
            logger.warning("Fungus initialized without a phylogeny.")
    
    # ─── instance methods ────────────────────────────────────────────────────
        
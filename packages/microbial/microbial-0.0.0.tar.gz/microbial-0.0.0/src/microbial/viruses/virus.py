"""Virus

Utilities for modeling various viral systems.
"""
# ─── import statements ────────────────────────────────────────────────── ✦✦ ─
import logging

from typing import Optional

from platformdirs import user_log_dir

from ..genomics import ViralGenome
from ..phylogeny import Phylogeny

# ─── helpers ──────────────────────────────────────────────────────────── ✦✦ ─
#
# Initialize the logger.
logging.basicConfig(filename=user_log_dir("microbial", "C. W. Rice"), level=logging.INFO)
logger = logging.getLogger(__name__)


# ─── model ────────────────────────────────────────────────────────────── ✦✦ ─
#
# Define the viral model.
class Virus:
    def __init__(
        self,
        genome: Optional[ViralGenome] = None,
        phylogeny: Optional[Phylogeny] = None
    ) -> None:
        self.phylogeny = phylogeny
        if self.phylogeny:
            self.genus = phylogeny.genus
            self.species = phylogeny.species
        else:
            logger.warning("Virus initialized without a phylogeny.")
    
    # ─── instance methods ────────────────────────────────────────────────────
        
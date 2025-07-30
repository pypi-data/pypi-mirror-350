"""Bacterium

Utilities for modeling various bacterial systems.
"""
# ─── import statements ────────────────────────────────────────────────── ✦✦ ─
import logging

from typing import Optional

from platformdirs import user_log_dir

from ..genomics import BacterialGenome
from ..phylogeny import Phylogeny

# ─── helpers ──────────────────────────────────────────────────────────── ✦✦ ─
#
# Initialize the logger.
logging.basicConfig(filename=user_log_dir("microbial", "C. W. Rice"), level=logging.INFO)
logger = logging.getLogger(__name__)


# ─── model ────────────────────────────────────────────────────────────── ✦✦ ─
#
# Define the bacterial model.
class Bacterium:
    def __init__(
        self,
        genome: Optional[BacterialGenome] = None,
        phylogeny: Optional[Phylogeny] = None
    ) -> None:
        self.phylogeny = phylogeny
        if self.phylogeny:
            self.genus = phylogeny.genus
            self.species = phylogeny.species
        else:
            logger.warning("Bacterium initialized without a phylogeny.")
    
    # ─── instance methods ────────────────────────────────────────────────────
        
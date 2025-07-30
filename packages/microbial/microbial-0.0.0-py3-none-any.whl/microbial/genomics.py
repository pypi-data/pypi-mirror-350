"""Genomics

This module defines the package's microbial genome models.
"""
# ─── import statements ────────────────────────────────────────────────── ✦✦ ─
from enum import Enum
from typing import Optional, Protocol

from Bio.Seq import Seq

class Domain(Enum):
    BACTERIA = "bacteria"
    FUNGI = "fungi"
    VIRUSES = "viruses"

class Genomic(Protocol):
    domain: Domain
    sequence: Optional[Seq]

    @property
    def sequence(self) -> str: ...

    @sequence.setter
    def sequence(self, value) -> None: ...

    @sequence.deleter
    def sequence(self) -> None: ...


# ─── models ───────────────────────────────────────────────────────────── ✦✦ ─
class Genome:
    domain: Domain

    def __init__(self, sequence: Optional[Seq] = None) -> None:
        self._sequence = sequence

    @property
    def sequence(self) -> str:
        return self._sequence
    
    @sequence.setter
    def sequence(self, value) -> None:
        self._sequence = value
    
    @sequence.deleter
    def sequence(self) -> None:
        del self._sequence


class BacterialGenome(Genome):
    domain = Domain.BACTERIA


class FungalGenome(Genome):
    domain = Domain.FUNGI


class ViralGenome(Genome):
    domain = Domain.VIRUSES

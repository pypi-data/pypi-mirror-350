"""Phylogeny

This module defines the package's phylogenetic analysis interface.
"""
# ─── import statements ────────────────────────────────────────────────── ✦✦ ─
from typing import Optional


# ─── data containers ──────────────────────────────────────────────────── ✦✦ ─
class Phylogeny:
    """
    A data container for representing an organism's phylogeny.
    """
    def __init__(
        self,
        kingdom: Optional[str] = None,
        phylum: Optional[str] = None,
        rclass: Optional[str] = None,
        order: Optional[str] = None,
        family: Optional[str] = None,
        genus: Optional[str] = None,
        species: Optional[str] = None
    ) -> None:
        """Constructor

        Initializes an instance of the `Phylogeny` class.

        Args:
            kingdom: A string representing the organism's taxonomic kingdom.
            phylum: A string representing the organism's taxonomic phylum.
            rclass: A string representing the organism's taxonomic class.
            order: A string representing the organism's taxonomic order.
            family: A string representing the organism's taxonomic family.
            genus: A string representing the organism's taxonomic genus.
            species: A string representing the organism's taxonomic species.
        
        Returns:
            None.
        """
        self._kingdom = kingdom
        self._phylum = phylum
        self._rclass = rclass
        self._subclass = None
        self._order = order
        self._suborder = None
        self._family = family
        self._subfamily = None
        self._genus = genus
        self._species = species
        self._subspecies = None

    
    # ─── properties ──────────────────────────────────────────────────────────
    # Kingdom
    @property
    def kingdom(self) -> str:
        return self._kingdom
    
    @kingdom.setter
    def kingdom(self, value) -> None:
        self._kingdom = value
    
    @kingdom.deleter
    def kingdom(self) -> None:
        del self._kingdom
    
    # Phylum
    @property
    def phylum(self) -> str:
        return self._phylum
    
    @phylum.setter
    def phylum(self, value) -> None:
        self._phylum = value
    
    @phylum.deleter
    def phylum(self) -> None:
        del self._phylum
    
    # Class
    @property
    def rclass(self) -> str:
        return self._rclass
    
    @rclass.setter
    def rclass(self, value) -> None:
        self._rclass = value
    
    @rclass.deleter
    def rclass(self) -> None:
        del self._rclass

    # Subclass
    @property
    def subclass(self) -> str:
        return self._subclass
    
    @subclass.setter
    def subclass(self, value) -> None:
        self._subclass = value
    
    # Order
    @property
    def order(self) -> str:
        return self._order
    
    @order.setter
    def order(self, value) -> None:
        self._order = value
    
    @order.deleter
    def order(self) -> None:
        del self._order

    # Suborder
    @property
    def suborder(self) -> str:
        return self._suborder
    
    @suborder.setter
    def suborder(self, value) -> None:
        self._suborder = value
    
    @suborder.deleter
    def suborder(self) -> None:
        del self._suborder
    
    # Family
    @property
    def family(self) -> str:
        return self._family
    
    @family.setter
    def family(self, value) -> None:
        self._family = value
    
    @family.deleter
    def family(self) -> None:
        del self._family
    
    # Subfamily
    @property
    def subfamily(self) -> str:
        return self._subfamily
    
    @subfamily.setter
    def subfamily(self, value) -> None:
        self._subfamily = value
    
    @subfamily.deleter
    def subfamily(self) -> None:
        del self._subfamily
    
    # Genus
    @property
    def genus(self) -> str:
        return self._genus
    
    @genus.setter
    def genus(self, value) -> None:
        self._genus = value
    
    @genus.deleter
    def genus(self) -> None:
        del self._genus
    
    # Species
    @property
    def species(self) -> str:
        return self._species
    
    @species.setter
    def species(self, value) -> None:
        self._species = value

    @species.deleter
    def species(self) -> None:
        del self._species

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyOptik.material.base_class import BaseMaterial

from PyMieSim.units import Quantity
from PyMieSim.single.scatterer.base import BaseScatterer
from PyMieSim.binary.interface_scatterer import CORESHELL
from PyMieSim.single.source.base import BaseSource


class CoreShell(CORESHELL, BaseScatterer):
    """
    Class representing a core/shell spherical scatterer.

    Parameters
    ----------
    core_diameter : Quantity
        Diameter of the core of the scatterer.
    shell_thickness : Quantity
        Thickness of the shell surrounding the core.
    core_property : Quantity | BaseMaterial
        Defines either the refractive index (`Quantity`) or material (`BaseMaterial`) of the scatterer's core. Only one can be provided.
    shell_property : Quantity | BaseMaterial
        Defines either the refractive index (`Quantity`) or material (`BaseMaterial`) of the scatterer's shell. Only one can be provided.

    """

    core_diameter: Quantity
    shell_thickness: Quantity
    core_property: Quantity | BaseMaterial
    shell_property: Quantity | BaseMaterial
    medium_property: Quantity | BaseMaterial
    source: BaseSource

    property_names = [
        "size_parameter", "cross_section", "g",
        "Qsca", "Qext", "Qabs", "Qback", "Qratio", "Qpr",
        "Csca", "Cext", "Cabs", "Cback", "Cratio", "Cpr"
    ]

    def __init__(self,
        core_diameter: Quantity,
        shell_thickness: Quantity,
        core_property: Quantity | BaseMaterial,
        shell_property: Quantity | BaseMaterial,
        medium_property: Quantity | BaseMaterial,
        source: BaseSource):
        """
        Initialize the CoreShell scatterer with its core and shell properties.

        Parameters
        ----------
        core_diameter : Quantity
            Diameter of the core in meters.
        shell_thickness : Quantity
            Thickness of the shell in meters.
        core_property : Quantity or BaseMaterial
            Refractive index or material of the core.
        shell_property : Quantity or BaseMaterial
            Refractive index or material of the shell.
        medium_property : Quantity or BaseMaterial
            Refractive index or material of the surrounding medium.
        source : BaseSource
            Source object associated with the scatterer.
        """
        self.core_diameter = self._validate_length(core_diameter)
        self.shell_thickness = self._validate_length(shell_thickness)
        self.core_property = self._validate_property(core_property)
        self.shell_property = self._validate_property(shell_property)
        self.medium_property = self._validate_property(medium_property)

        self.source = source
        self.core_index, self.core_material = self._assign_index_or_material(self.core_property)
        self.shell_index, self.shell_material = self._assign_index_or_material(self.shell_property)
        self.medium_index, self.medium_material = self._assign_index_or_material(self.medium_property)

        super().__init__(
            core_diameter=core_diameter.to_base_units().magnitude,
            shell_thickness=shell_thickness.to_base_units().magnitude,
            core_refractive_index=self.core_index.to_base_units().magnitude,
            shell_refractive_index=self.shell_index.to_base_units().magnitude,
            medium_refractive_index=self.medium_index.to_base_units().magnitude,
            source=self.source.binding
        )

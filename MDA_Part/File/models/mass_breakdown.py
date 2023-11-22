"""Main components for mass breakdown."""
#  This file is part of FAST-OAD_CS25
#  Copyright (C) 2022 ONERA & ISAE-SUPAERO
#  FAST is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import openmdao.api as om
from fastoad.module_management.service_registry import RegisterSubmodel

from fastoad_cs25.models.weight.mass_breakdown.constants import (
    SERVICE_AIRFRAME_MASS,
    SERVICE_CREW_MASS,
    SERVICE_FURNITURE_MASS,
    SERVICE_OWE,
    SERVICE_PAYLOAD_MASS,
    SERVICE_PROPULSION_MASS,
    SERVICE_SYSTEMS_MASS,
)
from fastoad_cs25.models.weight.mass_breakdown.update_mlw_and_mzfw import (
    UpdateMLWandMZFW,
)
from fastoad_cs25.models.weight.constants import SERVICE_MASS_BREAKDOWN
from fastoad_cs25.models.constants import PAYLOAD_FROM_NPAX


@RegisterSubmodel(
    SERVICE_MASS_BREAKDOWN, "fastoad.submodel.weight.mass.with_k_factor_owe"
)
class MassBreakdown(om.Group):
    """ """

    def initialize(self):
        self.options.declare(PAYLOAD_FROM_NPAX, types=bool, default=True)

    def setup(self):
        if self.options[PAYLOAD_FROM_NPAX]:
            self.add_subsystem(
                "payload",
                RegisterSubmodel.get_submodel(SERVICE_PAYLOAD_MASS),
                promotes=["*"],
            )
        self.add_subsystem("owe", OperatingWeightEmpty(), promotes=["*"])
        self.add_subsystem("update_mzfw_and_mlw", UpdateMLWandMZFW(), promotes=["*"])

        # Solvers setup
        self.nonlinear_solver = om.NonlinearBlockGS()
        self.nonlinear_solver.options["iprint"] = 0
        self.nonlinear_solver.options["maxiter"] = 50

        self.linear_solver = om.LinearBlockGS()
        self.linear_solver.options["iprint"] = 0


class OperatingWeightEmpty(om.Group):
    """Operating Empty Weight (OEW) estimation.

    This group aggregates weight from all components of the aircraft.
    """

    def setup(self):
        # Propulsion should be done before airframe, because it drives pylon mass.
        self.add_subsystem(
            "propulsion_weight",
            RegisterSubmodel.get_submodel(SERVICE_PROPULSION_MASS),
            promotes=["*"],
        )
        self.add_subsystem(
            "airframe_weight",
            RegisterSubmodel.get_submodel(SERVICE_AIRFRAME_MASS),
            promotes=["*"],
        )
        self.add_subsystem(
            "systems_weight",
            RegisterSubmodel.get_submodel(SERVICE_SYSTEMS_MASS),
            promotes=["*"],
        )
        self.add_subsystem(
            "furniture_weight",
            RegisterSubmodel.get_submodel(SERVICE_FURNITURE_MASS),
            promotes=["*"],
        )
        self.add_subsystem(
            "crew_weight",
            RegisterSubmodel.get_submodel(SERVICE_CREW_MASS),
            promotes=["*"],
        )

        self.add_subsystem("OWE_sum", OperatingWeightEmptyWithKFactor(), promotes=["*"])


class OperatingWeightEmptyWithKFactor(om.ExplicitComponent):
    def setup(self):

        self.add_input("data:weight:airframe:mass", units="kg", val=1.0)
        self.add_input("data:weight:propulsion:mass", units="kg", val=1.0)
        self.add_input("data:weight:systems:mass", units="kg", val=1.0)
        self.add_input("data:weight:furniture:mass", units="kg", val=1.0)
        self.add_input("data:weight:crew:mass", units="kg", val=1.0)

        self.add_input("data:weight:k_factor_OWE", val=1.0)

        self.add_output("data:weight:aircraft:OWE", val=20e3, units="kg")

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):

        outputs["data:weight:aircraft:OWE"] = inputs["data:weight:k_factor_OWE"] * (
            inputs["data:weight:airframe:mass"]
            + inputs["data:weight:propulsion:mass"]
            + inputs["data:weight:systems:mass"]
            + inputs["data:weight:furniture:mass"]
            + inputs["data:weight:crew:mass"]
        )

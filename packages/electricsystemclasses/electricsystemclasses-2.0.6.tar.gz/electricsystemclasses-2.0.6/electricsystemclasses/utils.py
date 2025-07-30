# Copyright 2025 ropimen
#
# This file is licensed under the Server Side Public License (SSPL), Version 1.0.
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
# https://www.mongodb.com/legal/licensing/server-side-public-license
#
# This file is part of ElectricSystemClasses.
#
# ElectricSystemClasses is a Python package providing a collection of classes for simulating electric systems.

from electricsystemclasses.simulation import SimulationGlobals

def powerToTotalEnergy( power_array ):
    return sum(p*SimulationGlobals.step_size_in_h for p in power_array)

def powerToEnergy( power_array ):
    return [x*SimulationGlobals.step_size_in_h for x in power_array]

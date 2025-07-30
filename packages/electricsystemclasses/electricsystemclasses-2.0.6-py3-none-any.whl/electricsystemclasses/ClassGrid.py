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

#class grid, it has no power limits

from electricsystemclasses.simulation import SimulationGlobals

class Grid:
    #class level counter
    all_grids = []

    def __init__(self, id):
        self.id = id
        self.power_history = [0]

        Grid.all_grids.append(self)


    def withdraw(self, power_value):
        power_value = abs(power_value)
        self.power_history.append(power_value)

    def inject(self, power_value):
        power_value = abs(power_value)
        self.power_history.append(-power_value)

    #method to get update the power history if the grid is not exchanging in the simul frame
    def update(self):

        i = SimulationGlobals.current_step_index

        if len(self.power_history) < i + 2:
            self.power_history.append(0)

    @classmethod
    def updateAllGrids(cls):
        for grid in cls.all_grids:
            grid.update()

    #class method to get the all generators
    @classmethod
    def getAllGrids(cls):
        return cls.all_grids
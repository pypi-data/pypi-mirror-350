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

#class representing a time invariant load requiring coonstant power
#when supplying the load the method returns the excess power and
#if required power greater than input power it returns the input power printing an error

from electricsystemclasses.simulation import SimulationGlobals

import random
import csv

class Variable_Load:
    #class-level counter
    all_loads = []

    def __init__(self, id, profile):
        self.load_id = id
        self.profile = profile
        self.power_history = [0]

        Variable_Load.all_loads.append(self)

    def now(self):

        i = SimulationGlobals.current_step_index

        return self.profile[i]

    def scale_profile(self, factor):
        self.profile = [val * factor for val in self.profile]

    #adapts the dimesnion of the profile to the new length
    #if the new length is smaller than the current one, it randomly deletes elements
    #if the new length is greater than the current one, it randomly adds elements
    #by taking the average of the two neighbours
    def resize_profile(self, new_len):
        while len(self.profile) > new_len:
            idx = random.randint(0, len(self.profile) - 1)
            del self.profile[idx]

        while len(self.profile) < new_len:
            idx = random.randint(1, len(self.profile) - 2)
            avg = (self.profile[idx - 1] + self.profile[idx + 1]) / 2
            self.profile.insert(idx, avg)

    def resize_profile_to_simulation(self, step, period):
        if period*3600/step != int(period*3600/step):
            raise ValueError("Simulation period must be divisible by step size.")
        new_len = 3600*period/step 
        while len(self.profile) > new_len:
            idx = random.randint(0, len(self.profile) - 1)
            del self.profile[idx]

        while len(self.profile) < new_len:
            idx = random.randint(1, len(self.profile) - 2)
            avg = (self.profile[idx - 1] + self.profile[idx + 1]) / 2
            self.profile.insert(idx, avg)

    #i is the current simulation step, for i in range
    def derivative(self):

        i = SimulationGlobals.current_step_index

        if i + 1 < len(self.profile):
            return (self.profile[i + 1] - self.profile[i])
        else:
            return 0

    def linearRegressionSlopeBackward(self, seconds = 5):

        i = SimulationGlobals.current_step_index
        t = SimulationGlobals.step_size_in_h

        subset_len = int(seconds/(3600 * t))
        xy = 0
        x = 0
        y = 0
        x2 = 0
        for j in range(subset_len):
            xy += self.profile[i - j] * (i - j)
            x += i - j
            y += self.profile[i - j]
            x2 += (i - j)**2
        b = (subset_len * xy - x * y)/(subset_len*x2 - x**2)
        return b

    def linearRegressionSlopeForward(self, seconds = 5):

        i = SimulationGlobals.current_step_index
        t = SimulationGlobals.step_size_in_h

        subset_len = int(seconds/(3600 * t))
        xy = 0
        x = 0
        y = 0
        x2 = 0
        for j in range(subset_len):
            xy += self.profile[i + j] * (i + j)
            x += i + j
            y += self.profile[i + j]
            x2 += (i + j)**2
        b = (subset_len * xy - x * y)/(subset_len*x2 - x**2)
        return b

    def supply(self, input_power):

        i = SimulationGlobals.current_step_index

        if input_power >= self.profile[i]:
            excess_power = input_power - self.profile[i]
            self.power_history.append(self.profile[i])
            return excess_power
        else:
            #not enough power, throw an error and block the execution of the script
            raise ValueError(f"Error: Not enough power to supply load {self.load_id}. Required Power: {self.required_power}. Input Power: {input_power}.")
    
    #class method to get all loads
    @classmethod
    def getAllLoads(cls):
        return cls.all_loads

    #class method to create a generator from a csv file column
    @classmethod
    def from_csv_column(cls, gen_id, filepath, col_index, delimiter=",", has_header=False):
        with open(filepath, newline='') as f:
            reader = csv.reader(f, delimiter=delimiter)
            if has_header:
                next(reader)
            profile = [float(row[col_index]) for row in reader if row]
        return cls(gen_id, profile)

    #class method to create a generator from a csv file row
    @classmethod
    def from_csv_row(cls, gen_id, filepath, row_index, delimiter=",", has_header=False):
        with open(filepath, newline='') as f:
            reader = list(csv.reader(f, delimiter=delimiter))
            if has_header:
                reader = reader[1:]
            profile = [float(val) for val in reader[row_index]]
        return cls(gen_id, profile)
    
    #No need for update(), is a profile...
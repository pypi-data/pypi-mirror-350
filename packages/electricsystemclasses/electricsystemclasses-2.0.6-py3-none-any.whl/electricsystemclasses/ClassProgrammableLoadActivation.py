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

#class representing a programmable load requiring coonstant power
#when supplying the load the method returns the excess power and
#if required power greater than input power it returns the input power printing an error
#ton min in hours, t is the time in the simulation frame in hours
# current step --> i; current step in hours --> h; step in hours --> t 
#deactivation_delay in seconds

from electricsystemclasses.simulation import SimulationGlobals

class Programmable_Load_W_Reactivation:
    #class-level counter
    all_programm_loads = []
    activable_loads = []
    active_loads = []

    def __init__(self, id, required_power, t_start, t_end, t_on_min, reactivation=False, deactivation_delay=10):
        self.load_id = id
        self.required_power = required_power
        self.t_start = t_start
        self.t_end = t_end
        self.t_on_min = t_on_min
        self.reactivation = reactivation
        self.deactivation_delay = deactivation_delay
        self.timer_deactivation = None
        self.checkCondition = False
        self.activation_time = None
        self.power_history = [0]
        self.toBeReactivated = True
        Programmable_Load_W_Reactivation.all_programm_loads.append(self)

    @classmethod
    def check_activable_loads(cls):

        h = SimulationGlobals.current_step_time_in_h

        cls.activable_loads.clear()
        for load in cls.all_programm_loads:
            if h < load.t_end and h >= load.t_start:
                cls.activable_loads.append(load)

    def activate(self):

        h = SimulationGlobals.current_step_time_in_h

        self.checkCondition = True
        if self in Programmable_Load_W_Reactivation.activable_loads:
            if self not in Programmable_Load_W_Reactivation.active_loads:
                    if self.toBeReactivated:
                        Programmable_Load_W_Reactivation.active_loads.append(self)
                        self.activation_time = h
                        if not self.reactivation:
                            self.toBeReactivated = False
                        #se il carico è riattivabile devo lavorare sulla h

    def supply(self, input_power):
        if self in Programmable_Load_W_Reactivation.active_loads:
            if input_power >= self.required_power:
                excess_power = input_power - self.required_power
                self.power_history.append(self.required_power)
                return excess_power
            else:
                #not enough power, throw an error and block the execution of the script
                raise ValueError(f"Error: Not enough power to supply load {self.load_id}.")
        else:
            self.power_history.append(0)
            return input_power
        
    #class method to get all loads
    @classmethod
    def get_allLoads(cls):
        return cls.all_loads
    
    @classmethod
    def update(cls):

        h = SimulationGlobals.current_step_time_in_h
        i = SimulationGlobals.current_step_index

        for load in cls.all_programm_loads:
            if load in cls.active_loads:
                if h - load.activation_time >= load.t_on_min:
                    if load.reactivation:

                        if load.checkCondition or load.timer_deactivation is None:
                            load.timer_deactivation = h
                        else:
                            if (h > load.timer_deactivation + load.deactivation_delay/3600):
                                cls.active_loads.remove(load)
                                load.activation_time = None
                                load.timer_deactivation = None
                    else:
                        cls.active_loads.remove(load)
                        load.activation_time = None
            else:
                if len(load.power_history) < i + 2:
                    load.power_history.append(0)
            load.checkCondition = False
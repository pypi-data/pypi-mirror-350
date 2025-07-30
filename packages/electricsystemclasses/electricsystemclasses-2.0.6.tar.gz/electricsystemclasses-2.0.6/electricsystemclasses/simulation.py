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

#step in seconds
#period in hours
import inspect

#Class to hold simulation parameters accessible for all compoments
class SimulationGlobals:

    current_step_index = None
    current_step_time_in_h = None
    step_size_in_h = None


def simulate(step_size, period, timeframe):
    if period*3600/step_size != int(period*3600/step_size):
        raise ValueError("Simulation period must be divisible by step size.")
    
    simulation_steps = int(period * 3600 / step_size)
    step_size_in_h = step_size / 3600

    SimulationGlobals.step_size_in_h = step_size_in_h

    # detecting how many arguments the user function expects
    user_args = inspect.signature(timeframe).parameters
    pass_args = {
        "current_step_index": None,
        "current_step_time_in_h": None,
        "step_size_in_h": None,
    }

    print("Starting Simulation")
    
    for i in range(simulation_steps):

        # step --> i
        # current step in hours --> h
        # step in hours --> t 

        print(f"Simulation step {i+1}/{simulation_steps}")
        
        current_step_time_in_h = i * step_size / 3600

        SimulationGlobals.current_step_index = i
        SimulationGlobals.current_step_time_in_h = current_step_time_in_h

        #passing values inside pass args
        pass_args["current_step_index"] = i
        pass_args["current_step_time_in_h"] = SimulationGlobals.current_step_time_in_h
        pass_args["step_size_in_h"] = SimulationGlobals.step_size_in_h

        timeframe(**{k: v for k, v in pass_args.items() if k in user_args})
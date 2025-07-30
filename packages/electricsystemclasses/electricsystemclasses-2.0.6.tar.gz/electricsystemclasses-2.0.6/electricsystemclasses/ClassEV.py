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

# current step --> i; current step in hours --> h; step in hours --> t 

from electricsystemclasses.simulation import SimulationGlobals

class EV:

    #class level counters for the EV number
    all_EV = []
    #class level counters for the EV classification
    crit_EV = []
    norm_EV = []
    prior_EV = []
    major_EV = []


    #constructor for the EV class, everything in kW, kWh and hours (t_arrival = 18.5 (18:30))
    def __init__(self, id, max_disch_power, max_charge_power, opt_power, capacity, soc_init_kwh, t_arrival, t_depart, soc_lim_kwh, soc_min_kwh):
        self.id = id
        self.max_disch_power = max_disch_power
        self.max_charge_power = max_charge_power
        self.opt_power = opt_power
        self.capacity = capacity
        self.t_depart = t_depart
        self.t_arrival = t_arrival
        self.soc_lim_kwh = soc_lim_kwh
        self.soc_min_kwh = soc_min_kwh
        self.soc_history_kwh = [soc_init_kwh]
        self.power_history = [0]

        EV.all_EV.append(self)

    #when charging an ev at a power it can handle but too energy to be contained
    #is treated as charging at a power equal to the available capacity/time frame
    #therefore calculated as the excess energy and then returned divided by t
    def charge(self, power):
    
        t = SimulationGlobals.step_size_in_h

        power = abs(power)    
        excess_power = power - self.max_charge_power
        excess_energy = 0
        #recharge power greater than max charge power
        if excess_power > 0:
            energy_to_charge = self.max_charge_power * t
            #energy to be stored greater than available capacity
            if self.soc_history_kwh[-1] + energy_to_charge > self.capacity:
                excess_energy = self.soc_history_kwh[-1] + energy_to_charge - self.capacity
                excess_power += excess_energy / t
                self.power_history.append((self.capacity-self.soc_history_kwh[-1]) / t)
                self.soc_history_kwh.append(self.capacity)
            #energy to be stored less than available capacity
            else:
                self.power_history.append(self.max_charge_power)
                self.soc_history_kwh.append(self.soc_history_kwh[-1] + energy_to_charge)
                excess_power = 0
        #recharge power less than max charge power
        else:
            #charge the vehicle at input power
            energy_to_charge = power * t
            #energy to be stored greater than available capacity
            if self.soc_history_kwh[-1] + energy_to_charge > self.capacity:
                excess_energy = self.soc_history_kwh[-1] + energy_to_charge - self.capacity
                excess_power = excess_energy / t
                self.power_history.append((self.capacity-self.soc_history_kwh[-1]) / t)
                self.soc_history_kwh.append(self.capacity)
            #energy to be stored less than available capacity
            else:
                self.soc_history_kwh.append(self.soc_history_kwh[-1] + energy_to_charge)
                self.power_history.append(power)
                excess_power = 0
        return excess_power
    
    #same reasoning as for the charge method
    #expects a positive discharge power and returns a positive excess power to be discharged
    def discharge(self, power):
    
        t = SimulationGlobals.step_size_in_h

        power = abs(power)
        excess_power = power - self.max_disch_power
        excess_energy = 0
        #discharge power greater than max discharge power
        if excess_power > 0:
            energy_to_discharge = self.max_disch_power * t
            #energy to be discharged greater than available capacity
            if self.soc_history_kwh[-1] - energy_to_discharge < self.soc_min_kwh:
                excess_energy = energy_to_discharge - self.soc_history_kwh[-1]
                excess_power += excess_energy / t
                self.power_history.append(-(self.soc_history_kwh[-1]-self.soc_min_kwh) / t)
                self.soc_history_kwh.append(self.soc_min_kwh)
            #energy to be discharged less than available capacity
            else:
                self.power_history.append(-self.max_disch_power)
                self.soc_history_kwh.append(self.soc_history_kwh[-1] - energy_to_discharge)
        #discharge power less than max discharge power
        else:
            #discharge the vehicle at input power
            energy_to_discharge = power * t
            #energy to be discharged greater than available capacity
            if self.soc_history_kwh[-1] - energy_to_discharge < self.soc_min_kwh:
                excess_energy = energy_to_discharge - self.soc_history_kwh[-1]
                excess_power = excess_energy / t
                self.power_history.append(-(self.soc_history_kwh[-1]-self.soc_min_kwh) / t)
                self.soc_history_kwh.append(self.soc_min_kwh)
            else:
                #energy to be discharged less than available capacity
                self.power_history.append(-power)
                self.soc_history_kwh.append(self.soc_history_kwh[-1] - energy_to_discharge)
                excess_power = 0
        return excess_power

    #h time of arrival in hours => 18:30 = 18.5
    @classmethod
    def classify_EV(cls):

        h = SimulationGlobals.current_step_time_in_h

        #empty the lists
        cls.crit_EV.clear()
        cls.norm_EV.clear()
        cls.prior_EV.clear()
        cls.major_EV.clear()

        for ev in cls.all_EV:
            #check times
            if h >= ev.t_arrival and h < ev.t_depart:
                #check crit state
                if ev.soc_history_kwh[-1] < ev.soc_min_kwh:
                    cls.crit_EV.append(ev)
                #check major state
                elif ev.soc_history_kwh[-1] > ev.soc_lim_kwh:
                    cls.major_EV.append(ev)
                #check prior state
                elif (ev.soc_lim_kwh - ev.soc_history_kwh[-1])/ev.opt_power >= (ev.t_depart - ev.t_arrival):
                      cls.prior_EV.append(ev)
                #check norm state
                else:
                    cls.norm_EV.append(ev)

    #charging group of EVs with the same power
    @classmethod     
    def charge_group(cls, group, power):

        if len(group) != 0:
            excess_power = 0
            charge_power = power / len(group)
            for ev in group:
                excess_power += ev.charge(charge_power)
            return excess_power
        else:
            return power

    #discharging group of EVs with the same power
    @classmethod     
    def discharge_group(cls, group, power):

        if len(group) != 0:
            excess_power = 0
            charge_power = power / len(group)
            for ev in group:
                excess_power += ev.discharge(charge_power)
            return excess_power
        else:
            return power
        
    #proportional discharge
    @classmethod
    def discharge_group_prop(cls, group, power):
        #calculate the total power the group can output
        ev_power = sum(ev.max_disch_power for ev in group)
        #check if availability greater than power required
        if ev_power >= power:
            #order the group by max discharge power
            group.sort(key=lambda x: x.max_disch_power, reverse=True)
            #loop over vehicles and discharge keeping track of the excess
            excess_power = 0
            for ev in group:
                #calculate discharge power proportionally
                ev_discharge_power = power * (ev.max_disch_power / ev_power)
                excess_power += ev.discharge(ev_discharge_power + excess_power)
        #availability less than power required
        else:
            #loop over the vehicles and discharge at max power keeping track of the excess
            excess_power = 0
            for ev in group:
                excess_power += ev.discharge(ev.max_disch_power)
        
        return excess_power
    
    #class methods to access cls variables cleanly
    @classmethod
    def getAllEV(cls):
        return cls.all_EV
    
    @classmethod
    def getCritEV(cls):
        return cls.crit_EV
    
    @classmethod
    def getNormEV(cls):
        return cls.norm_EV
    
    @classmethod
    def getPriorEV(cls):    
        return cls.prior_EV
    
    @classmethod
    def getMajorEV(cls):
        return cls.major_EV

    #method to update values of soc_history_kwh if left untouched at the end of the simulation  frame
    #if the vehicle is not charging or discharging, the soc_history_kwh is updated with the last value
    @classmethod
    def updateAllEV(cls):
        
        i = SimulationGlobals.current_step_index

        for ev in cls.all_EV:
            if len(ev.soc_history_kwh) < i + 2:
                ev.power_history.append(0)
                ev.soc_history_kwh.append(ev.soc_history_kwh[-1])

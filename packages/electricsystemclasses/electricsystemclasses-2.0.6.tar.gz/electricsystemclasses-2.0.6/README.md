# ElectricSystemClasses

A Python package providing a collection of classes for simulating electric systems. The library includes components like electric vehicles (EVs), generators, grids, storage systems, and loads. 
It is designed for use in simulations and modeling of power systems, focusing on flexible, easy-to-use components for energy management scenarios.

## Features

- **Electric Vehicles (EVs)**: Model and manage electric vehicle characteristics such as power, state-of-charge, and classification.
- **Generators**: Simulate electricity generation profiles, including scaling and adjusting the length of the profiles.
- **Grid**: Model the power exchange between the system and the grid, tracking the energy flow.
- **Storage Systems**: Simulate energy storage components, including charging and discharging behaviors.
- **Constant Load**: A basic class for representing time-invariant loads.
- **Variable Load**: A class representing time-variant loads.
- **Programmable Load With Activation**: A class for representing time-programmed loads with reactivation availability.

## Full DOC
At the bottom.

## Installation

You can install the `electricsystemclasses` package via pip.

`pip install electricsystemclasses`

## License

This project is licensed under the Server Side Public License (SSPL), Version 1.0. You may not use this file except in compliance with the License.

## Contributing

I welcome contributions to this project! If you'd like to contribute contact me. Ensure that your code adheres to the coding style of the project, and that you have tested your changes.

## Contact

email: rmmenichelli@gmail.com
Feel free to ask for clarification.

## Full DOC

The package provides a full simulation engine to study the behaviour of multiple electric components. Each component is represented by instances of different classes, each requiring different attributes.

The simulation is iterative-based and works around two main components, the `simulate` function and a user defined function representing a single time frame of simulation. 
The `simulate` function takes as arguments:
 
 `step_size`: the step size of the simulation in seconds `s`. Type `int` or `float`.

 `period`: the amount of hours to be simulated. The simulation works starting from zero and finishing at the value of `period`. The total simulated steps will be `period * 3600 / step_size`.

 `timeframe`: a function that needs to be defined by the user representing the logics within each timeframe. The name could be any, usually `timeframe` is chosen.
 
  This function need to be defined as:

    def timeframe():

        #user code

The function works without any arguments but, if needed, it provides to the user the simulation parameters.
By adding as arguments of the function one or more of the following variables, the user can use them within the definition of the logics in the timeframe
function.

- the iteration `current_step_index` of the simulation. 

- the current simulated step in hours `current_step_time_in_h`.

- the step size in hours `step_size_in_h`.

By adding these arguments, the `simulate` function automatically detects which arguments the user needs for more complex logics.

Another way to get those simulation parameters is to access them directly from as attributed of the class `SimulationGlobals`:

        # e.g. 

        h = SimulationGlobals.step_size_in_h

In each simulated step, the logics defined inside the `timeframe` function are applied. All attributes containing the power history and state of charge of instances are updated each simulation step.

To use additional arguments, define them outside the `timeframe` function and then add them inside using the `global` keyword.

E.g.

excess_counter = 0

        def timeframe():

            global excess_counter

            # now it s possible to use the counter within the timeframe function without 
            # resetting it to 0 each simulated step.

### **Classes**
 
#### **Constant Load**

The `ConstantLoad` class represents simple loads having constant power consumption. 

The `__init__` takes as arguments:

 `id`: could be of any type. Can be used to implement logics based on   numerical ids or to add descriptive informations about the load kind.
 
 e.g. `1` or `"hvac"`.

 `required_power`: the power consumption of the load in `kW`. Type `float` or `int`.

##### **Attributes**

All the arguments of the `__init__`.

- `power_history`: a list containing all the simulated power values of the instance, in `kW`. It gets filled during the simulation.

##### **Class Attributes**

- `all_loads`: a list containing all instances of the class.

##### **Class Methods**
- `get_allLoads(cls)`: returns a list containing all instances of the class.

- `update(cls)`: It updates the attribute `power_history` if not supplied during the user defined timeframe.

##### **Instance Methods**
- `supply(self, input_power)`: if the `input_power` is less than the `required_power` the function raises an error. The load can't be supplied. In any other cases it returns the excess power, difference of `input_power` and `required_power`.

#### **Electric Vehicle (EV)**

The `EV` class represents electric vehicles.

The `__init__` takes as arguments:

 `id`: could be of any type. Can be used to implement logics based on   numerical ids or to add descriptive informations about the load kind.
 
 e.g. `1` or `"EV1"`.

 `max_discharge_power`: the maximum power dischargeable by the vehicle in `kW`. Type `float` or `int`.

 `max_charge_power`: the maximum power the vehicle can charge at, in `kW`. Type `float` or `int`.

 `opt_power`: the optimal charge and discharge power of the vehicle in `kW`. Type `float` or `int`.

 `capacity`: the capacity of the vehicle in `kWh`. Type `float` or `int`.

 `t_depart`: the departure time of the vehicle in `h`. Type `float` or `int`.

 `t_arrival`: the arriving time of the vehicle in `h`. Type `float` or `int`.
 
 `soc_lim_kwh`: the minimum target state of charge to be reached during the time between `t_arrival` and `t_depart`, in `kwh`. It is not guaranteed due to the `max_charge_power` limitation.

 `soc_min_kwh`: the state of charge below which the vehicle is classified as critical, meaning having really low state of charge.

##### **Attributes**

All the arguments of the `__init__`.

`soc_history_kwh`: a list containing all values of the state of charge in `kWh`. It gets filled during the simulation.

`power_history`: a list containing all the simulated power values of the instance, in `kW`. It gets filled during the simulation.

##### **Class Attributes**

- `all_EV`: a list containing all instances of the class.

- `crit_EV`: a list containing all vehicles having state of charge below `soc_min_kwh`.

- `norm_EV`: a list containing all vehicles having state of charge above `soc_min_kwh` and below `soc_lim_kwh`.

- `major_EV`: a list containing all vehicles having state of charge above `soc_lim_kwh`.

- `prior_EV`: a list containing all vehicles having state of charge such that if recharged at `opt_power` they will not reach the target `soc_lim_kwh` in time, therefore having a priority state over `norm_EV`.

##### **Class Methods**

- `classify_EV(cls)`: a method that classifies the instances of the class based on the logics of `crit_EV`, `norm_EV`, `prior_EV`, `major_EV`, at instance `h`. `h` is the current simulated time in hours.

- `charge_group(cls, group, power)`: a method that charges a group of vehicles equally dividing the input power. It returns the power that could had not be handled by the vehicles in the group due to power or capacity limitations.
Arguments:

    `group`: a list containing instances of the class. Could also be one of the classifying groups such as `norm_EV`. Type `list`.
 
    `power`: the input power in `kW`. Type `int` or `float`.

- `discharge_group(cls, group, power)`: a method that discharges a group of vehicles equally dividing the requested power. It returns the requested power that could had not be handled by the vehicles in the group due to power or capacity limitations.
Arguments:

    `group`: a list containing instances of the class. Could also be one of the classifying groups such as `norm_EV`. Type `list`.

    `power`: the requested power in `kW`. Type `int` or `float`.

- `discharge_group_prop(cls, group, power)`: a method that discharges a group of vehicles proportionally, dividing the requested power based on the `max_discharge_power` of the instances. It returns the requested power that could had not be handled by the vehicles in the group due to power or capacity limitations.
Arguments:

    `group`: a list containing instances of the class. Could also be one of the classifying groups such as `norm_EV`. Type `list`.

    `power`: the requested power in `kW`. Type `int` or `float`.

- `get_allEV(cls)`: returns a list containing all instances of the class.

- `getCritEV(cls)`: returns the list `crit_EV`.

- `getNormEV(cls)`: returns the list `norm_EV`.

- `getPriorEV(cls)`: returns the list `prior_EV`.

- `getMajorEV(cls)`: returns the list `major_EV`.

- `updateAllEV(cls)`: It updates the attributes `power_history` and `soc_history_kwh` if untouched during the user defined timeframe.

##### **Instance Methods**
- `charge(self, power)`: a method that charges an instance of the class. Takes as arguments an input power `power`. It returns the excess power that could had not be handled by the vehicle due to power or capacity limitations.

- `discharge(self, power)`: a method that discharges an instance of the class. Takes as arguments a discharge power `power`. It returns the excess discharge power that could had not be handled by the vehicle due to power or capacity limitations.

#### **Generator**

A class representing generators.

The `__init__` takes as arguments:

 `id`: could be of any type. Can be used to implement logics based on   numerical ids or to add descriptive informations about the load kind.
 
 e.g. `1` or `"pv1"`.
 
 `profile`: a list containing the values of the generated power in `kW`. Type `list` containing `int` or `float`. The length must be equal or greater than the number of simulated steps. Can be scaled and resized using instance methods `scale_profile`, `resize_profile`, and `resize_profile_to_simulation`.

##### **Attributes**

All the arguments of the `__init__`.

##### **Class Attributes**

- `all_gen`: list containing all instances of the class.

##### **Class Methods**

- `getAllGen(cls)`: returns a list of all instances of the class.

- `from_csv_column(cls, gen_id, filepath, col_index, delimiter=",", has_header=False)`: a method that creates an instance of the class based on values contained in a csv column. Takes as arguments an `id` of any type, the `filepath` of the csv file, `col_index` the column index starting from 0, the delimiter of the csv file (`default=","`),and a boolean representing if an header is present and needs to be skipped (`default=False`).


- `from_csv_row(cls, gen_id, filepath, row_index, delimiter=",", has_header=False)`: a method that creates an instance of the class based on values contained in a csv row. Takes as arguments an `id` of any type, the `filepath` of the csv file, `row_index` the row index starting from 0, the delimiter of the csv file (`default=","`),and a boolean representing if an header is present and needs to be skipped (`default=False`).

##### **Instance Methods**

- `scale_profile(self, factor)`: a method that scales the profile. Takes as input the scale factor `factor`, type `int` or `float`.

- `resize_profile(self, new_len)`: adapts the dimension of the profile to a new length. If the new length is smaller than the current one, it randomly deletes elements, otherwise it randomly adds elements by taking the average of the two neighbours.

- `resize_profile_to_simulation(self, new_len)`: adapts the dimension of the profile to the one needed in the simulation, defined by `step` and `period`. If the required length is smaller than the current one, it randomly deletes elements, otherwise it randomly adds elements by taking the average of the two neighbours.

- `derivative(self)`: returns the derivative of the instance `profile` at current iteration.

- `linearRegressionSlopeBackward(self, seconds = 5)`: return the angular coefficient (slope) of the regression line based on the amount of data specified by the `seconds` argument. Default is 5 seconds. The backward kind takes the data of the 5 seconds prior to the call of the function.

- `linearRegressionSlopeForward(self, seconds = 5)`: return the angular coefficient (slope) of the regression line based on the amount of data specified by the `seconds` argument. Default is 5 seconds. The forward kind takes the data of the 5 seconds after the call of the function, therefore considering as known the future values of the generated power.

- `now(self)`: returns the value of the generator profile at the simulated time.

#### **Grid**

A class representing an infinite power grid.

The `__init__` takes as arguments:

 `id`: could be of any type. Can be used to implement logics based on   numerical ids or to add descriptive informations about the load kind.
 
 e.g. `1` or `"poc1"`.

##### **Attributes**

All the arguments of the `__init__`.

`power_history`: a list containing all values of the grid power in `kW`. It gets filled during the simulation.

##### **Class Attributes**

- `all_grids`: list containing all instances of the class.

##### **Class Methods**

- `getAllGrids(cls)`: returns a list of all instances of the class.

- `updateAllGrids(cls)`: method that calls the instance method `update` on each instance of the class. 

##### **Instance Methods**

- `withdraw(self, power_value)`: a method that represents withdrawing power from a grid instance.
 

- `inject(self, power_value)`: a method that represents injecting power from a grid instance.
 
- `update(self)`: a method that updates the instance `power_history` attribute if unchanged by the user defined logic.

#### **Programmable Load With Reactivation**

A class representing a programmable load defined:

 - a period of activation in hours, defined by a start time and an end time. This is the period in which the load can be activated, the period is defined representing as 0 hours the start of the simulation. Therefore in a simulation of a single day starting from midnight, a load that wants to be activated only between 10am and 3 pm will have start time 10 and end time 15. Only between this period the `activate()` function will execute.

 - a minimum of active time in hours, if greater than zero the load will not be disactivated before this time has passed.

 - a reactivation boolean, representing if the load needs to be reactivated when a repeated call of the activate method happens. 

 - a deactivation delay active only for reactivable loads in seconds. 

The `__init__` takes as arguments:

 `id`: could be of any type. Can be used to implement logics based on   numerical ids or to add descriptive informations about the load kind.
 
 e.g. `1` or `"programmable_load1"`.
  
 `required_power`: The required power to supply the load.

 `t_start`: the start of the activable interval of the instance. In hours, considering as 0 hours the start of the simulation.

 `t_end`: the end of the activable interval of the instance. In hours, considering as 0 hours the start of the simulation.

 `t_on_min`: the minimum time the load needs to be active, in hours. If 0.5 at the call of the `activate()` function, the load will be considered active for at least 0.5 hours, even if the condition that resulted in the activation is met no more.

 `reactivation`: a boolean representing if the load needs to be reactivated. If set to `False`, after a first activation the load will no more be activated even at a second call of the `activate()` function.

 `deactivation_delay`: a deactivation delay in seconds. The load will wait `deactivation_delay` seconds prior to be disconnected. This is done to limit the activations and deactivations when the condition that resulted in the `activate()` function is not met each simulated frame, resulting in a `power_history` full of discontinuities.
  

##### **Attributes**

All the arguments of the `__init__`.

`timer_deactivation`: keeps track of the time passing after a deactivation condition. Used for the deactivation delay logic.

`checkCondition`: a boolean that equals `True` if the activation function of the load has been called during the current iteration.

`activation_time`: attribute that contains the activation time of the load.

`power_history`: a list containing all values of the load power in `kW`. It gets filled during the simulation.

`toBeReactivated`: a support attribute representing whether a load needs to be activated or not at the next call of the `activate` method.

##### **Class Attributes**

- `all_programm_loads`: list containing all instances of the class.

- `activable_loads`: a list containing all loads that can be activated based on their activation interval.

- `active_loads`: a list containing all active loads.

##### **Class Methods**

- `check_activable_loads(cls)`: class method that updates the `activable_loads` list at the current iteration. Needs to be called at the start of each iteration, or in general, prior to the call of the `activate` method.

- `update(cls)`: a method that updates the instance `power_history` attribute if unchanged by the user defined logic.

- `get_allLoads(cls)`: returns a list of all instances of the class.

##### **Instance Methods**

- `activate(self)`: method that activates the instance if the current simulated time is in its activation interval.

- `supply(self, input_power)`: supplies the load at `required_power` and returns the excess. If `input_power` is lower than `required_power` an error is raised.


#### **Storage**

A class representing an electric storage (a battery).

The `__init__` takes as arguments:

 `id`: could be of any type. Can be used to implement logics based on   numerical ids or to add descriptive informations about the load kind.
 
 e.g. `1` or `"stg1"`.
  
 `capacity`: the capacity of the storage instance in kWh.

 `max_charge_power`: the maximum charge power in kW.
  
  `max_disch_power`: the maximum discharge power in kW.

##### **Attributes**

All the arguments of the `__init__`.

`soc_history_kwh`: array containing all State of Charge (SOC) values of the instance in kWh.

`power_history`: array containing the power history of the instance in kW.

##### **Class Attributes**

- `all_storages`: list containing all instances of the class.

##### **Class Methods**

- `get_all_storages(cls)`: class method that returns a list containing all instances of the class.

- `updateAllStg(cls)`:  class method that updates the instances `power_history` and `soc_history_kwh` attributes if unchanged by the user defined logic.

##### **Instance Methods**


- `charge(self, power)`: a method that charges the storage instance returning the excess power that could had not be handled by the storage due to power or capacity limitations.

Arguments:

   `power`: the input power in `kW`. Type `int` or `float`.

- `discharge(self, power)`: a method that discharges the storage instance returning the required power that could had not be handled by the storage due to power or capacity limitations.

Arguments:

   `power`: the input power in `kW`. Type `int` or `float`.

#### **Variable Load**

A class representing a variable load, represented by a load profile.

The `__init__` takes as arguments:

 `id`: could be of any type. Can be used to implement logics based on   numerical ids or to add descriptive informations about the load kind.
 
 e.g. `1` or `"variableLoad1"`.
 
 `profile`: a list containing the values of the load profile in `kW`. Type `list` containing `int` or `float`. The length must be equal or greater than the number of simulated steps. Can be scaled and resized using instance methods `scale_profile`, `resize_profile`, and `resize_profile_to_simulation`.

##### **Attributes**

All the arguments of the `__init__`.

`power_history`: a list containing the power history of the instance in kW.

##### **Class Attributes**

`all_loads`: list containing all instances of the class.

##### **Class Methods**

- `getAllLoads(cls)`: returns a list of all instances of the class.

- `from_csv_column(cls, gen_id, filepath, col_index, delimiter=",", has_header=False)`: a method that creates an instance of the class based on values contained in a csv column. Takes as arguments an `id` of any type, the `filepath` of the csv file, `col_index` the column index starting from 0, the delimiter of the csv file (`default=","`),and a boolean representing if an header is present and needs to be skipped (`default=False`).


- `from_csv_row(cls, gen_id, filepath, row_index, delimiter=",", has_header=False)`: a method that creates an instance of the class based on values contained in a csv row. Takes as arguments an `id` of any type, the `filepath` of the csv file, `row_index` the row index starting from 0, the delimiter of the csv file (`default=","`),and a boolean representing if an header is present and needs to be skipped (`default=False`).

##### **Instance Methods**

- `supply(self, input_power)`: supplies the variable load at `input_power` (in kW). If `input_power` is greater than the variable load required power at the simulated time, the method returns the excess power. If `input_power` is lower than the power required by the variable load an error is raised.

- `now(self)`: returns the load profile value at the simulated time.

- `scale_profile(self, factor)`: a method that scales the profile. Takes as input the scale factor `factor`, type `int` or `float`.

- `resize_profile(self, new_len)`: adapts the dimension of the profile to a new length. If the new length is smaller than the current one, it randomly deletes elements, otherwise it randomly adds elements by taking the average of the two neighbours.

- `resize_profile_to_simulation(self, new_len)`: adapts the dimension of the profile to the one needed in the simulation, defined by `step` and `period`. If the required length is smaller than the current one, it randomly deletes elements, otherwise it randomly adds elements by taking the average of the two neighbours.

- `derivative(self)`: returns the derivative of the instance `profile` at current iteration.

- `linearRegressionSlopeBackward(self, seconds = 5)`: return the angular coefficient (slope) of the regression line based on the amount of data specified by the `seconds` argument. Default is 5 seconds. The backward kind takes the data of the 5 seconds prior to the call of the function.

- `linearRegressionSlopeForward(self, seconds = 5)`: return the angular coefficient (slope) of the regression line based on the amount of data specified by the `seconds` argument. Default is 5 seconds. The forward kind takes the data of the 5 seconds after the call of the function, therefore considering as known the future values of the generated power.

#### **Utils**

Other useful functions provided by the package.

`powerToTotalEnergy(power_array)`: a function that returns the sum of the energy in kWh given a power profile in kW. The function automatically considers the simulation parameters set in the `simulate` function. `power_array` of type `list` containing `float` or/and `int` values.

`powerToEnergy(power_array)`: a function that returns an array containing all the exchanged energies in kWh for each simulated step and based on a power profile in kW. The function automatically considers the simulation parameters set in the `simulate` function. `power_array` of type `list` containing `float` or/and `int` values.
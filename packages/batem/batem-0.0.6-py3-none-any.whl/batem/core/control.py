"""
This code is protected under GNU General Public License v3.0

A helper module dedicated to the design of time-varying state space model approximated by bilinear state space model.

Author: stephane.ploix@grenoble-inp.fr
"""
from __future__ import annotations
from typing import Any
import numpy
import time
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
from itertools import product
from .components import Airflow
from .statemodel import StateModel
from .model import BuildingStateModelMaker
from .data import DataProvider
from .inhabitants import Preference


class VALUE_DOMAIN_TYPE(Enum):
    """An enum to define the type of the value domain of a control port"""
    CONTINUOUS = 0
    DISCRETE = 1


class AbstractPort(ABC):
    """A control port deals with a control variable: it is basically a dynamic value domain that might depends on other variables. 
    It acts as a dynamic filter with a control value domain as input and a restricted control value domain as output. 
    The dynamic value domain can be return on demand.
    AbstractPort is an abstract class.
    """

    def __init__(self, variable_name: str, value_domain: list[float], value_domain_type: VALUE_DOMAIN_TYPE, data_provider: DataProvider = None,  default_value: float = 0) -> None:
        """Create a control port.

        :param port_variable: name of the variable corresponding to the port
        :type port_variable: str
        :param value_domain_type: type of the value domain (continuous or discrete)
        :type value_domain_type: VALUE_DOMAIN_TYPE
        :param default_value: default value for the port, defaults to 0
        :type default_value: float, optional
        """
        super().__init__()
        self.data_provider: DataProvider = data_provider
        self.variable_name: str = variable_name
        self.in_provider: bool = self._in_provider(variable_name)
        self.recorded_data: dict[int, dict[int, float]] = {self.variable_name: dict()}
        self.value_domain_type: VALUE_DOMAIN_TYPE = value_domain_type
        self.mode_value_domains: dict[int, float] = {0: self._standardize_value_domain(value_domain)}
        self.default_value: float = default_value
        
    def _in_provider(self, variable_name: str) -> bool:
        return self.data_provider is not None and variable_name in self.data_provider
    
    def __call__(self, k: int, port_value: float | None = None) -> list[float] | float | None:
        """_summary_
        This is the hidden method that is used to apply the control port to the data provider. It acts as a filter, matching any value to the specified value domain, which can depends on modes: the value domain is therefore dynamic. If a port value is provided, it will be transformed to the nearest possible value in the value domain else, all the possible values are returned.

        :param modes_values: _description_, defaults to None
        :type modes_values: dict[str, float], optional
        :param port_value: _description_, defaults to None
        :type port_value: float | None, optional
        :return: _description_
        :rtype: list[float] | float | None
        """
        if port_value is None:
            return self._value_domain
        else:
            if self.value_domain_type == VALUE_DOMAIN_TYPE.DISCRETE:
                if port_value not in self._value_domain:
                    distance_to_value = tuple([abs(port_value - v) for v in self._value_domain])
                    port_value = self._value_domain[distance_to_value.index(min(distance_to_value))]
            else:  # VALUE_DOMAIN_TYPE.CONTINUOUS
                port_value = port_value if port_value <= self._value_domain[1] else self._value_domain[1]
                port_value = port_value if port_value >= self._value_domain[0] else self._value_domain[0]
            self.recorded_data[self.variable_name][k] = port_value
            if self.in_provider:
                self.data_provider(self.variable_name, k, port_value)
            return port_value

    def _standardize_value_domain(self, value_domain: int | float | tuple | float | list[float]) -> None | tuple[float]:
        """Standardize the value domain defined by a single float value to a tuple of floats.

        :param value_domain: the user-defined value domain
        :type value_domain: int | float | tuple | float | list[float]
        :return: the standardized value domain i.e. return tuples for single values and also tuples (min value, max value) for continuous value domains described by more than 2 values (e.g. [1, 2, 3, 4] -> (1, 4))
        :rtype: None | tuple[float]
        """
        if value_domain is None:
            return None
        else:
            if self.value_domain_type == VALUE_DOMAIN_TYPE.DISCRETE:
                if type(value_domain) is int or type(value_domain) is float:
                    return (value_domain,)
                if len(value_domain) > 1:
                    return tuple(sorted(list(set(value_domain))))
            else:  # continuous value domain
                if type(value_domain) is not list and type(value_domain) is not tuple:
                    return (value_domain, value_domain)
                else:
                    return (min(value_domain), max(value_domain))
                
    def get_recorded_variables(self) -> float:
        recorded_variables: list[str] = list()
        for variable_name in self.recorded_data:
            if len(self.recorded_data[variable_name]) > 0:
                recorded_variables.append(variable_name)
        return recorded_variables
    
    def get_recorded_data(self, variable_name: str) -> list[float]:
        data: list[float] = list()
        for k in range(len(self.data_provider)):
            if k in self.recorded_data[variable_name]:
                data.append(self.recorded_data[variable_name][k])
            else:
                data.append(self.default_value)
        return data
            
    def __repr__(self) -> str:
        """String representation of the control port

        :return: a descriptive string
        :rtype: str
        """
        return f"Control port {self.variable_name}"
    
    def __str__(self) -> str:
        """String representation of the control port

        :return: a descriptive string
        :rtype: str
        """
        if self.value_domain_type == VALUE_DOMAIN_TYPE.DISCRETE:
            string = 'Discrete'
        else:
            string = 'Continuous'
        string += f" control port on {self.variable_name} with value domain {self.mode_value_domains}"
        if self.in_provider:
            string += f", is in the data provider"
        else:
            string += f", is not in the data provider"
        string += f", recorded data: {self.get_recorded_variables()}"
        return string


class ContinuousPort(AbstractPort):
    """A control port with a continuous range of possible values.
    """
    def __init__(self, control_variable_name: str, value_domain: list[float], data_provider: DataProvider = None, default_value: float = 0) -> None:
        """Create a continuous control port.

        :param control_variable_name: name of the variable corresponding to the port
        :type control_variable_name: str
        :param value_domain: range of possible values [min, max]
        :type value_domain: list[float]
        :param default_value: default value for the port, defaults to 0
        :type default_value: float, optional
        """
        super().__init__(control_variable_name, value_domain=value_domain, value_domain_type=VALUE_DOMAIN_TYPE.CONTINUOUS, data_provider=data_provider, default_value=default_value)


class DiscretePort(AbstractPort):
    """A control port with a discrete set of possible values.
    """

    def __init__(self, control_variable_name: str, value_domain: list[float], data_provider: DataProvider = None, default_value: float = 0) -> None:
        """Create a discrete control port.

        :param control_variable_name: name of the variable corresponding to the port
        :type control_variable_name: str
        :param value_domain: list of possible discrete values
        :type value_domain: list[float]
        :param default_value: default value for the port, defaults to 0
        :type default_value: float, optional
        """
        super().__init__(control_variable_name, value_domain=value_domain, value_domain_type=VALUE_DOMAIN_TYPE.DISCRETE, data_provider=data_provider, default_value=default_value)


class BinaryPort(DiscretePort):
    """A control port with exactly two possible values: 0 and 1.
    """

    def __init__(self, control_variable_name: str, data_provider: DataProvider = None, default_value: float = 0) -> None:
        """Create a binary control port.

        :param control_variable_name: name of the variable corresponding to the port
        :type control_variable_name: str
        :param default_value: default value for the port (0 or 1), defaults to 0
        :type default_value: float, optional
        """
        super().__init__(control_variable_name, value_domain=(0, 1), data_provider=data_provider, default_value=default_value)


class ModePort(AbstractPort):
    """A control port that depends on a mode variable: the value domain is different depending on the mode.
    """

    def __init__(self, port_variable: str, mode_variable: str, data_provider: DataProvider, mode_value_domains: dict[int, list[float]], value_domain_type: VALUE_DOMAIN_TYPE,  default_value: float = 0, default_mode: int = 0) -> None:
        """Create a mode port.

        :param port_variable: name of the variable corresponding to the port
        :type port_variable: str
        :param mode_variable: name of the mode variable
        :type mode_variable: str
        :param mode_value_domains: description of the value domain for each mode
        :type mode_value_domains: dict[int, list[float]]
        :param value_domain_type: type of the value domain (continuous or discrete)
        :type value_domain_type: VALUE_DOMAIN_TYPE
        :param default_value: the default value to apply in case of unknown value, defaults to 0
        :type default_value: float, optional
        :param default_mode: the default mode to apply in case of unknown mode, defaults to 0
        :type default_mode: int, optional
        :raises ValueError: if the default mode is not defined in the mode_value_domains
        :raises ValueError: if the mode variable is not defined in the modes_values
        """
        super().__init__(port_variable, value_domain_type=value_domain_type, value_domain=mode_value_domains[default_mode], data_provider=data_provider, default_value=default_value)
        self.mode_value_domains = mode_value_domains
        self.mode_variable: str = mode_variable
        self.default_mode: int = default_mode
        if 0 not in mode_value_domains:
            raise ValueError('The mode_value_domain must contain the mode 0 (OFF)')
        self.mode_value_domains: dict[int, list[float]] = mode_value_domains
        if default_mode not in self.mode_value_domains:
            raise ValueError(f'The default mode {default_mode} is not defined in the mode_value_domain')
        self.mode_value_domains: dict[int, list[float]] = mode_value_domains

    def __call__(self, k: int, port_value: float | None = None) -> list[float] | float | None:
        """_summary_
        This is the hidden method that is used to apply the control port to the data provider. It acts as a filter, matching any value to the specified value domain, which can depends on modes: the value domain is therefore dynamic. If a port value is provided, it will be transformed to the nearest possible value in the value domain else, all the possible values are returned.

        :param modes_values: _description_, defaults to None
        :type modes_values: dict[str, float], optional
        :param port_value: _description_, defaults to None
        :type port_value: float | None, optional
        :return: _description_
        :rtype: list[float] | float | None
        """
        if port_value is None:
            return self.mode_value_domains[self.dp(self.mode_variable, k)]
        else:
            if self.value_domain_type == VALUE_DOMAIN_TYPE.DISCRETE:
                if port_value not in self.mode_value_domains[self.data_provider(self.mode_variable, k)]:
                    distance_to_value = tuple([abs(port_value - v) for v in self.mode_value_domains[self.data_provider(self.mode_variable, k)]])
                    port_value = self.mode_value_domains[self.data_provider(self.mode_variable, k)][distance_to_value.index(min(distance_to_value))]
            else:  # VALUE_DOMAIN_TYPE.CONTINUOUS
                port_value = port_value if port_value <= self.data_provider(self.mode_variable, k)[1] else self.data_provider(self.mode_variable, k)[1]
                port_value = port_value if port_value >= self.data_provider(self.mode_variable, k)[0] else self.data_provider(self.mode_variable, k)[0]
            self.recorded_data[self.variable_name][k] = port_value
            if self.in_provider:
                self.data_provider(self.variable_name, k, port_value)
            return port_value


class OpeningPort(ModePort):
    """A control port that models an opening binary variable depending on a presence binary variable.
    """
    #  port_variable: str, mode_variable: str, data_provider: DataProvider, mode_value_domains: dict[int, list[float]], value_domain_type: VALUE_DOMAIN_TYPE,  default_value: float = 0, default_mode: int = 0
    def __init__(self, opening_variable: str, presence_variable: str, data_provider: DataProvider, default_value: float = 0, default_mode: int = 0) -> None:
        """Create an opening port.

        :param opening_variable: name of the variable corresponding to the opening
        :type opening_variable: str
        :param presence_variable: name of the variable corresponding to the presence
        :type presence_variable: str
        :param default_mode: the default mode to apply in case of unknown mode, defaults to 0
        :type default_mode: int, optional
        :param default_value: the default value to apply in case of unknown value, defaults to 0
        :type default_value: float, optional
        """
        super().__init__(port_variable=opening_variable, mode_variable=presence_variable, data_provider=data_provider, mode_value_domains={1: [0, 1], 0: [0, 0]}, value_domain_type=VALUE_DOMAIN_TYPE.DISCRETE, default_value=default_value, default_mode=default_mode)


class ZoneTemperatureSetpointPort(ModePort):
    """A control port to model a temperature setpoint with discrete values depending on the heating mode. It is used in combination with a power port to model a temperature controller.
    """

    def __init__(self, temperature_setpoint_variable: str, mode_name: str, data_provider: DataProvider, mode_value_domains: dict[int, tuple[float]] = {1: (13, 19, 20, 21, 22, 23, 24), 0: None, -1: (24, 25, 26, 28, 29, 32)}, default_value: float = None) -> None:

        super().__init__(port_variable=temperature_setpoint_variable, mode_variable=mode_name, data_provider=data_provider, mode_value_domains=mode_value_domains, value_domain_type=VALUE_DOMAIN_TYPE.DISCRETE, default_value=default_value, default_mode=0)


class ZoneHvacContinuousPowerPort(ModePort):
    """A zoneHvacPowerPort is a control port modeling a power supply with an upper bound both for heating and cooling. If mode=0, it's off and mode = 1 or -1 are respectively the heating mode and the cooling mode.
    """

    def __init__(self, hvac_power_variable: str, hvac_mode: str, data_provider: DataProvider, max_heating_power: float, max_cooling_power: float, default_value: float = 0, full_range: bool = False):
        if not full_range:
            super().__init__(hvac_power_variable, hvac_mode, data_provider=data_provider, mode_value_domains={1: [0, max_heating_power], 0: [0, 0], -1: [-max_cooling_power, 0]}, value_domain_type=VALUE_DOMAIN_TYPE.CONTINUOUS)
        else:
            super().__init__(hvac_power_variable, hvac_mode, data_provider=data_provider, mode_value_domains={1: (-max_cooling_power, max_heating_power), 0: 0, -1: (-max_cooling_power, max_heating_power)}, value_domain_type=VALUE_DOMAIN_TYPE.CONTINUOUS, default_value=default_value)
        self.mode_variable_name: str | None = hvac_mode


class MultimodePort(ModePort):
    """A control port that models a variable depending on several mode variables. A MultimodePort should be used when you need to model a variable whose value domain depends on multiple mode variables that can take any integer values.
    For example:
    mode_port = MultimodePort(
    port_variable="temperature_setpoint",
    mode_variables=["occupancy", "time"],
    mode_value_domains={
        (0, 0): [15, 16, 17],  # Empty at night
        (0, 1): [16, 17, 18],  # Empty during day
        (1, 0): [18, 19, 20],  # Occupied at night
        (1, 1): [20, 21, 22]   # Occupied during day
    },
    value_domain_type=VALUE_DOMAIN_TYPE.DISCRETE)
    """

    def __init__(self, port_variable: str, mode_variables: list[str], data_provider: DataProvider, mode_value_domains: dict[tuple[int, int], list[float]], value_domain_type: VALUE_DOMAIN_TYPE, default_value: float = 0, default_mode: tuple[int, int] = 0) -> None:
        """Create a multimode port.

        :param port_variable: name of the variable corresponding to the port
        :type port_variable: str
        :param mode_variables: list of mode variables
        :type mode_variables: list[str]
        :param mode_value_domains: description of the value domain for each mode
        :type mode_value_domains: dict[tuple[int], list[float]]
        :param value_domain_type: type of the value domain (continuous or discrete)
        :type value_domain_type: VALUE_DOMAIN_TYPE
        :param default_value: the default value to apply in case of unknown value, defaults to 0
        :type default_value: float, optional
        """
        super().__init__(port_variable, value_domain_type=value_domain_type, value_domain=mode_value_domains[default_mode], data_provider=data_provider, default_value=default_value)
        self.mode_variables: list[str] = mode_variables
        self.mode_value_domains: dict[tuple[int], list[float]] = mode_value_domains
        
    def __call__(self, modes_values: dict[str, float] = None, port_value: float | None = None) -> list[float] | float | None:
        """See parent class definition"""
        possible_values: list[float] | None = self.possible_values(modes_values)
        if port_value is None:
            return possible_values
        if possible_values is None:
            return None
        port_value = port_value
        if self.value_domain_type == VALUE_DOMAIN_TYPE.DISCRETE:
            if port_value not in possible_values:
                distance_to_value = tuple([abs(port_value - v) for v in possible_values])
                port_value = possible_values[distance_to_value.index(min(distance_to_value))]
        else:
            port_value = port_value if port_value <= possible_values[1] else possible_values[1]
            port_value = port_value if port_value >= possible_values[0] else possible_values[0]
        return port_value
    
    def possible_values(self, modes_values: dict[str, float]) -> list[float] | None:
        """See parent class definition"""
        modes_tuple: tuple[int] = tuple(modes_values[v] for v in self.mode_variables)
        if modes_tuple not in self.mode_value_domains:
            raise ValueError(f'The mode tuple {modes_tuple} is not defined in the mode_value_domains')
        return self.mode_value_domains[modes_tuple]

    def value_domain(self, modes_values: dict[str, float]) -> list[float] | None:
        """See parent class definition"""
        mode_tuple: tuple[int] = (modes_values[v] for v in self.mode_variables)
        if mode_tuple not in self.mode_value_domains:
            return self.mode_value_domains[self.default_mode]


class MultiplexPort(AbstractPort):
    """A control port that models a variable depending on several binary variables. A MultiplexPort should be used you need to model a variable that depends on multiple binary switches (0/1 values)
    For example:
    multiplex_port = MultiplexPort(
    port_variable="fan_speed",
    binary_variables=["switch1", "switch2", "switch3"],
    multiplex={
        (0, 0, 0): (0,),      # All switches off -> speed 0
        (0, 0, 1): (1,),      # Only switch3 on -> speed 1
        (0, 1, 0): (2,),      # Only switch2 on -> speed 2
        (0, 1, 1): (3,),      # switch2 and 3 on -> speed 3
        (1, 0, 0): (4,),      # Only switch1 on -> speed 4
        (1, 0, 1): (5,),      # switch1 and 3 on -> speed 5
        (1, 1, 0): (6,),      # switch1 and 2 on -> speed 6
        (1, 1, 1): (7,)       # All switches on -> speed 7
    },
    default_input_values=(0, 0, 0),
    value_domain_type=VALUE_DOMAIN_TYPE.DISCRETE)
    """

    def __init__(self, port_variable: str, binary_variables: list[str], multiplex: dict[tuple[int], tuple[float]], default_input_values: tuple[int], value_domain_type: VALUE_DOMAIN_TYPE, default_output_value: float = 0) -> None:
        """Create a multiplex port.

        :param output_variable: name of the variable corresponding to the port
        :type output_variable: str
        :param binary_variables: list of binary variables
        :type binary_variables: list[str]
        :param multiplex: description of the value domain for each mode
        :type multiplex: dict[tuple[int], tuple[float]]
        :param default_input_values: the default input values
        :type default_input_values: tuple[int]
        :param value_domain_type: type of the value domain (continuous or discrete)
        :type value_domain_type: VALUE_DOMAIN_TYPE
        :param default_output_value: the default output value, defaults to 0
        :type default_output_value: float, optional
        """
        super().__init__(port_variable, value_domain_type=value_domain_type, default_value=default_output_value)
        self.binary_variables: tuple[str] = binary_variables
        self.multiplex: dict[tuple[int], tuple[float]] = multiplex
        if default_input_values not in multiplex:
            raise f'default multimode possible values {default_input_values} must be present'
        self.default_input_values: tuple[int] = default_input_values

    def value_domain(self, modes_values: dict[str, float]) -> tuple[float]:
        """See parent class definition"""
        input_values: tuple[int] = tuple(modes_values[v] for v in self.binary_variables)
        if input_values not in self.multiplex:
            return self.multiplex[self.default_input_values]
        else:
            return self.multiplex[input_values]

    def __call__(self, modes_values: list[str], port_value: float | None = None) -> list[float] | float | None:
        return super().__call__(modes_values, port_value)[0]


class AirflowPort(MultiplexPort):
    """Control port modeling different (discrete) levels of ventilation depending on the presence and on a mode"""

    def __init__(self, airflow_variable: str, infiltration_rate: float, ventilation_levels: dict[str, float]) -> None:
        level_variables: list[str] = list(ventilation_levels.keys())
        self.multimodes_value_domains: dict[tuple[int], tuple[float]] = dict()
        for mode_tuple in map(list, product([0, 1], repeat=len(ventilation_levels))):
            mode_air_renewal_rate: float = infiltration_rate
            for i in range(len(mode_tuple)):
                if mode_tuple[i] == 1:
                    mode_air_renewal_rate += ventilation_levels[level_variables[i]]
            self.multimodes_value_domains[tuple(mode_tuple)] = mode_air_renewal_rate
        super().__init__(airflow_variable, level_variables, self.multimodes_value_domains, default_input_values=tuple([0] * len(level_variables)), value_domain_type=VALUE_DOMAIN_TYPE.DISCRETE, default_output_value=infiltration_rate)


class ZoneTemperatureController:
    """A controller is controlling a power port to reach as much as possible a temperature setpoint modeled by a temperature port. The controller is supposed to be fast enough comparing to the 1-hour time slots, that its effect is immediate (level 0), or almost immediate (level 1, for modifying the next temperature).
    It would behave as a perfect controller if the power was not limited but it is.
    """

    def __init__(self, zone_temperature_name: str, free_power_name: str, zone_temperature_setpoint_port: ZoneTemperatureSetpointPort, zone_hvac_power_port: ZoneHvacContinuousPowerPort) -> None:
        """Create a zone temperature controller.

        :param zone_temperature: name of the variable corresponding to the zone temperature
        :type zone_temperature: str
        :param zone_power: name of the variable corresponding to the free total power of the zone including the metabolic gain, the Joule effect, the solar gain
        :type zone_power: str
        :param zone_temperature_setpoint_port: a port towards a temperature setpoint port
        :type zone_temperature_setpoint_port: ZoneTemperatureSetpointPort
        :param zone_hvac_power_port: a port towards a HVAC power port
        :type zone_hvac_power_port: ZoneHvacContinuousPowerPort
        """
        self.free_power_name: str = free_power_name
        self.hvac_power_name: str = zone_hvac_power_port.variable_name
        self.temperature_setpoint_name: str = zone_temperature_setpoint_port.variable_name
        self.zone_temperature_name: str = zone_temperature_name
        self.zone_hvac_power_port: ZoneHvacContinuousPowerPort = zone_hvac_power_port
        self.zone_temperature_setpoint_port: ZoneTemperatureSetpointPort = zone_temperature_setpoint_port
        self._level: int = None
        self.input_index: int = None
        self.output_index: int = None
 
    def _register_nominal_state_model(self, nominal_state_model: StateModel) -> None:
        """private method automatically by the manager to register a nominal state model to the controller.

        :param nominal_state_model: a nominal state model
        :type nominal_state_model: StateModel
        """
        if self.free_power_name not in nominal_state_model.input_names:
            raise ValueError(f'{self.free_power_name} is not an input of the state model')
        if self.zone_temperature_name not in nominal_state_model.output_names:
            raise ValueError(f'{self.zone_temperature_name} is not an output of the state model')

        self.input_index: int = nominal_state_model.input_names.index(self.free_power_name)
        self.input_names: list[str] = nominal_state_model.input_names
        self.output_index: int = nominal_state_model.output_names.index(self.zone_temperature_name)
        self.output_names: list[str] = nominal_state_model.output_names
        D_condition: numpy.matrix = nominal_state_model.D[self.output_index, self.input_index]
        CB: numpy.matrix = nominal_state_model.C * nominal_state_model.B
        CB_condition: numpy.matrix = CB[self.output_index, self.input_index]
        if D_condition != 0:
            self._level = 0
        elif CB_condition != 0:
            self._level = 1
        else:
            raise ValueError(f'{self.zone_temperature_name} cannot be controlled by {self.hvac_power_name}')

    def level(self) -> int:
        """Get the level of the controller. 0 means that the controller reach the setpoint immediately, 1 means that the controller reach the setpoint with a delay of one time slot.

        :return: the level of the controller
        :rtype: int 0 or 1
        """
        return self._level
    
    def __repr__(self) -> str:
        """String representation of the controller.
        :return: a string representation of the controller
        :rtype: str
        """
        return self.hvac_power_name + '>' + self.zone_temperature_name

    def __str__(self) -> str:
        """String representation of the controller.
        :return: a string representation of the controller
        :rtype: str
        """
        string: str = f'{self.zone_temperature_name} is controlled by {self.hvac_power_name}, contributing to {self.free_power_name} at level {self._level} thanks to the setpoint {self.temperature_setpoint_name}'
        return string

    def step(self, setpoint: float, state_model_k: StateModel, state: numpy.matrix, mode, current_context_inputs: dict[str, float], next_context_inputs: dict[str, float] = None) -> float:  # mode: int,
        if setpoint is None or numpy.isnan(setpoint) or type(setpoint) is float('nan'):
            return self.zone_hvac_power_port(0)
        setpoint = self.zone_temperature_setpoint_port({'mode': mode}, setpoint)
        current_context_inputs[self.free_power_name] = self.zone_hvac_power_port({'mode': mode}, current_context_inputs[self.free_power_name])
        U_k = numpy.matrix([[current_context_inputs[input_name]] for input_name in self.input_names])
        if self._level == 0:
            delta_control_value: numpy.matrix = (setpoint - state_model_k.C[self.output_index, :] * state - state_model_k.D[self.output_index, :] * U_k) / state_model_k.D[self.output_index, self.input_index]
        elif self._level == 1:
            if next_context_inputs is None:
                raise ValueError("Inputs at time k and k+1 must be provided for level-1 controller {self.control_input_name} -> {self.controlled_output_name}")
            U_kp1 = numpy.matrix([[next_context_inputs[input_name]] for input_name in self.input_names])
            delta_control_value: numpy.matrix = (setpoint - state_model_k.C[self.output_index, :] * state_model_k.A * state - state_model_k.C[self.output_index, :] * state_model_k.B * U_k - state_model_k.D[self.output_index, :] * U_kp1) / (state_model_k.C[self.output_index] * state_model_k.B[:, self.input_index])
            delta_control_value = delta_control_value[0, 0]
        else:  # unknown level
            raise ValueError('Unknown controller level')
        return delta_control_value
    

class ZoneManager(ABC):
    """A manager is a class that gathers all the data about a zone, including control rules.
    """
    
    def __init__(self, dp: DataProvider, zone_power_name: str, hvac_power_name: str, zone_temperature_name: str, state_model_maker: BuildingStateModelMaker,  preference: Preference, initial_temperature: float = 20, **available_ports: AbstractPort) -> None:
        self.recorded_data: dict[str, dict[int, list[float]]] = dict()
        self.dp: DataProvider = dp
        self.preference: Preference = preference
        self.state_model_maker: BuildingStateModelMaker = state_model_maker
        self.nominal_state_model: StateModel = self.state_model_maker.make_nominal(reset_reduction=True)
        self.input_names: list[str] = self.nominal_state_model.input_names
        self.output_names: list[str] = self.nominal_state_model.output_names
        self.initial_temperature: float = initial_temperature
        self.datetimes: list[datetime] = self.dp.series('datetime')
        self.day_of_week: list[int] = self.dp('day_of_week')
        self.available_ports: dict[str, AbstractPort] = available_ports
        self.zone_power_name: str = zone_power_name
        if zone_power_name not in self.input_names:
            raise ValueError(f'{zone_power_name} is not an input of the state model')
        self.zone_power_index: int = self.input_names.index(zone_power_name)
        self.hvac_power_name: str = hvac_power_name
        self.zone_temperature_name: str = zone_temperature_name
        if zone_temperature_name not in self.output_names:
            raise ValueError(f'{zone_temperature_name} is not an output of the state model')
        self.zone_temperature_index: int = self.output_names.index(zone_temperature_name)
        self.preference: Preference = preference
        
    def controls(self, k: int, X_k: numpy.matrix, current_output_dict: dict[str, float]) -> None:
        # if self.dp('presence', k) == 1:    ######### DESIGN YOUR OWN CONTROLS HERE #########
        #     self.window_opening_port(k, 1) # USE THE CONTROL PORTS FOR ACTION AND USE self.dp('variable', k) TO GET A VALUE
        pass
    
    def __str__(self) -> str:
        string: str = f"ZONE MANAGER\nBindings:\nzone_power == {self.zone_power_name}\nhvac_power == {self.hvac_power_name}\nzone_temperature == {self.zone_temperature_name}\n"
        string += 'Nominal state model:\n'
        string += str(self.nominal_state_model) + '\n'
        string += str(self.preference)
        string += f'\nInitial temperature: {self.initial_temperature}\n'
        string += "Available ports:\n"
        for port_name in self.available_ports:
            # string += f"{self.available_ports[port_name]}\n"
            # string += f"{port_name} with type {type(self.available_ports[port_name])}\n"
            string += str(self.available_ports[port_name]) + '\n'
        return string


class FedZoneManager(ZoneManager):
    """A manager is a class that gathers all the data about a zone, including control rules.
    """

    def __init__(self, dp: DataProvider, zone_power_name: str, hvac_power_name: str, zone_temperature_name: str, state_model_maker: BuildingStateModelMaker, preference: Preference, initial_temperature: float = 20, **available_ports: AbstractPort) -> None:
        super().__init__(dp, zone_power_name, hvac_power_name, zone_temperature_name, state_model_maker, preference, initial_temperature, **available_ports)


class ControlledZoneManager(ZoneManager):
    """A manager is a class that gathers all the data about a zone, including control rules.
    """

    def __init__(self, dp: DataProvider, zone_temperature_controller: ZoneTemperatureController, state_model_maker: BuildingStateModelMaker, preference: Preference, initial_temperature: float = 20, **available_ports: AbstractPort) -> None:
        super().__init__(dp, zone_temperature_controller.free_power_name, zone_temperature_controller.hvac_power_name, zone_temperature_controller.zone_temperature_name, state_model_maker, preference, initial_temperature, **available_ports)
       
        self.available_set_points: bool = False
        self.zone_temperature_controller: ZoneTemperatureController = zone_temperature_controller
        self.has_controller: bool = zone_temperature_controller is not None
        self.available_set_points = False
        
        if self.has_controller:
            self.zone_temperature_controller: ZoneTemperatureController = zone_temperature_controller
            self.zone_temperature_controller._register_nominal_state_model(self.nominal_state_model)
            if self.zone_temperature_controller.zone_temperature_name not in self.output_names:
                raise ValueError(f'{self.zone_temperature_controller.zone_temperature_name} is not an output of the state model')
            if self.zone_temperature_controller.free_power_name not in self.input_names:
                raise ValueError(f'{self.zone_temperature_controller.free_power_name} is not an input of the state model')
            
            if self.zone_temperature_controller.temperature_setpoint_name in self.dp:
                self.available_set_points = True
        else:  # no controller
            if self.zone_temperature_controller.temperature_setpoint_name in self.dp:
                self.available_set_points = True
            else:
                raise ValueError(f'{self.zone_temperature_controller.temperature_setpoint_name} is not in the data provider')
            
    def __str__(self) -> str:
        string: str = super().__str__()
        port = self.zone_temperature_controller.zone_hvac_power_port
        string += f'hvac_power_port on {port.variable_name} with type {type(port)}\n'
        string += str(port) + '\n'
        port: ZoneTemperatureSetpointPort = self.zone_temperature_controller.zone_temperature_setpoint_port
        string += f'temperature_setpoint_port on {port.variable_name} with type {type(port)}\n'
        string += str(port) + '\n'
        return string
    
        
        # Initialize with input values from DataProvider
        # inputs_k = {input_name: self.dp(input_name, 0) for input_name in self.input_names}
        # self.state_model_k.make().initialize(**inputs_k)
        # self.state_model_k.set_state(self.state_model_k.initialize(**inputs_k))
                
    # def run(self) -> None:
    #     preference = Preference(preferred_temperatures=(19, 24), extreme_temperatures=(16, 29), preferred_CO2_concentration=(500, 1500), temperature_weight_wrt_CO2=0.5, power_weight_wrt_comfort=0.5, mode_cop={1: 2, -1: 2})

    #     control_model = ControlModel(self.state_model_maker, self)
    #     print(control_model)
    #     control_model.simulate()

    #     preference.print_assessment(self.dp.series('datetime'), Pheater=self.dp.series('Pheater'), temperatures=self.dp.series('TZoffice'), CO2_concentrations=self.dp.series('CCO2office'), occupancies=self.dp.series('occupancy'), action_sets=(self.dp.series('window_opening'), self.dp.series('door_opening')), modes=self.dp.series('mode'))
    #     self.dp.plot()


class ControlModel:
    """The main class for simulating a living area with a control.
    """

    def __init__(self, building_state_model_maker: BuildingStateModelMaker, manager: ControlledZoneManager = None) -> None:
        self.building_state_model_maker: BuildingStateModelMaker = building_state_model_maker
        self.dp: DataProvider = building_state_model_maker.data_provider
        self.airflows: list[Airflow] = building_state_model_maker.airflows
        self.fingerprint_0 = self.dp.fingerprint(0)  # None
        self.state_model_0: StateModel = building_state_model_maker.make_k(k=0, reset_reduction=True, fingerprint=self.fingerprint_0)
        self.input_names: list[str] = self.state_model_0.input_names
        self.output_names: list[str] = self.state_model_0.output_names
        self.state_models_cache: dict[int, StateModel] = {self.fingerprint_0: self.state_model_0}
        self.manager: ControlledZoneManager = manager
        if manager is not None:
            self.manager.register_control_model(self)

    def simulate(self, suffix: str = ''):
        print("simulation running...")
        start: float = time.time()
        controller_controls: dict[str, list[float]] = {repr(self.manager.zone_temperature_controller): [self.manager.zone_temperature_controller]}  # list() for controller in self.manager.zone_temperature_controller}
        controller_setpoints: dict[str, list[float]] = {repr(self.manager.zone_temperature_controller): [self.manager.zone_temperature_controller]}  # {repr(controller): list() for controller in self.manager.zone_temperature_controller}

        X_k: numpy.matrix = None
        for k in range(len(self.dp)):
            current_outputs = None
            # compute the current state model
            current_fingerprint: list[int] = self.dp.fingerprint(k)
            if current_fingerprint in self.state_models_cache:
                state_model_k = self.state_models_cache[current_fingerprint]
                print('.', end='')
            else:
                state_model_k: StateModel = self.building_state_model_maker.make_k(k, reset_reduction=(k == 0))
                self.state_models_cache[self.dp.fingerprint(k)] = state_model_k
                print('*', end='')
            # compute inputs and state vector
            inputs_k: dict[str, float] = {input_name: self.dp(input_name, k) for input_name in self.input_names}
            if X_k is None:
                X_k: numpy.matrix = self.state_model_0.initialize(**inputs_k)
            # compute the output before change
            output_values: list[float] = state_model_k.output(**inputs_k)
            current_outputs: dict[str, float] = {self.output_names[i]: output_values[i] for i in range(len(self.output_names))}
            self.manager.controls(k, X_k, current_outputs)

            # compute the current state model after potential change by the "controls" function
            current_fingerprint: list[int] = self.dp.fingerprint(k)
            if current_fingerprint in self.state_models_cache:
                state_model_k = self.state_models_cache[current_fingerprint]
                print('.', end='')
            else:
                state_model_k: StateModel = self.building_state_model_maker.make_k(k, reset_reduction=(k == 0))
                self.state_models_cache[self.dp.fingerprint(k)] = state_model_k
                print('*', end='')
            # collect input data for time slot k (and k+1 if possible) from the data provided
            inputs_k: dict[str, float] = {input_name: self.dp(input_name, k) for input_name in self.input_names}
            if k < len(self.dp) - 1:
                inputs_kp1: dict[str, float] = {input_name: self.dp(input_name, k+1) for input_name in self.input_names}
            else:
                inputs_kp1 = inputs_k
            # update the input power value to reach the control temperature setpoints
            # for controller in self.manager.zone_temperature_controllers_initial_temperature:
            controller = self.manager.zone_temperature_controller
            controller_name: str = repr(controller)
            if controller._level == 0:
                setpoint_k: float = self.dp(controller.zone_temperature_setpoint_variable, k)
                control_k: float = controller.step(k, setpoint_k, state_model_k, X_k, inputs_k)
            elif controller._level == 1:
                if k < len(self.dp) - 1:
                    setpoint_k: float = self.dp(controller.temperature_setpoint_name, k+1)
                else:
                    setpoint_k: float = self.dp(controller.zone_temperature_setpoint_variable, k)
            control_k: float = controller.step(k, setpoint_k, state_model_k, X_k, inputs_k, inputs_kp1)
            controller_controls[controller_name].append(control_k)
            controller_setpoints[controller_name].append(setpoint_k)

            inputs_k[controller.free_power_name] = inputs_k[controller.free_power_name] + control_k
            self.dp(controller.free_power_name, k, control_k)

            state_model_k.set_state(X_k)
            output_values = state_model_k.output(**inputs_k)
            for output_index, output_name in enumerate(self.output_names):
                self.dp(output_name, k, output_values[output_index])
            X_k = state_model_k.step(**inputs_k)
        print(f"\nDuration in seconds {time.time() - start} with a state model cache size={len(self.state_models_cache)}")

    def __str__(self) -> str:
        string = 'ControlModel:'
        string += f'\n-{self.manager.zone_temperature_controller}'
        return string
"""
This code has been written by stephane.ploix@grenoble-inp.fr
It is protected under GNU General Public License v3.0

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


class VALUE_DOMAIN_TYPE(Enum):
    """An enum to define the type of the value domain of a control port"""
    CONTINUOUS = 0
    DISCRETE = 1


class AbstractPort(ABC):
    """ A control port deals with a control variable: it is basically a dynamic value domain that might depends on other variables. It acts as a dynamic filter with a control value domain as input and a restricted control value domain as output. The dynamic value domain can be return on demand.
    AbstractPort is an abstract class.
    """

    def __init__(self, port_variable: str, value_domain_type: VALUE_DOMAIN_TYPE, default_value: float = 0) -> None:
        """Create a control port.

        :param dp: the data provider, whose control values will be modified by the control port
        :type dp: DataProvider
        :param port_variable: name of the variable corresponding to the port
        :type port_variable: str
        :param discrete: a flag which is True if the possible values are a finite number of values, or False in case of an interval value domain, defaults to False
        :type discrete: bool, optional
        :param record: a flag used to collect locally the port values, defaults to False
        :type record: bool, optional
        """
        super().__init__()
        self.port_variable: str = port_variable
        self.value_domain_type: VALUE_DOMAIN_TYPE = value_domain_type
        self.default_value: float = default_value
    
    def __call__(self, modes_values: dict[str, float] = None, port_value: float | None = None) -> list[float] | float | None:
        possible_values: list[float] | None = self.possible_values(modes_values)
        if port_value is None:
            return possible_values
        if possible_values is None:
            return None
        port_value = port_value
        if self.value_domain_type == VALUE_DOMAIN_TYPE.DISCRETE:
            if port_value not in possible_values:
                distance_to_value = tuple([abs(port_value - value) for value in possible_values])
                port_value = possible_values[distance_to_value.index(min(distance_to_value))]
        else:
            port_value = port_value if port_value <= possible_values[1] else possible_values[1]
            port_value = port_value if port_value >= possible_values[0] else possible_values[0]
        return port_value

    def _standardize_value_domain(self, value_domain: int | float | tuple | float | list[float]) -> None | tuple[float]:
        if value_domain is None:
            return None
        else:
            if self.value_domain_type == VALUE_DOMAIN_TYPE.DISCRETE:
                if type(value_domain) is int or type(value_domain) is float:
                    return (value_domain,)
                if len(value_domain) > 1:
                    return tuple(sorted(list(set(value_domain))))
            else:
                if type(value_domain) is not list and type(value_domain) is not tuple:
                    return (value_domain, value_domain)
                else:
                    return (min(value_domain), max(value_domain))

    def __repr__(self) -> str:
        """String representation of the control port

        :return: a descriptive string
        :rtype: str
        """
        return f"Control port {self.port_variable}"

    def possible_values(self, modes_values: dict[str, float] = None) -> list[float]:
        return self._standardize_value_domain(self.value_domain(modes_values))

    @abstractmethod
    def value_domain(self, modes_values: dict[str, float] = None) -> list[float]:
        """An abstract method that must return at any time the list of possible control values
        :return: the list of possible control values for time slot k. If it returns None, all the control values are transmitted as they are.If the control is discrete, it returns an ascending ordered list of values that can be taken by the control. If the control port is continuous, only the 2 first elements of the ordered list are considered as bounds of the interval representing the range of possible values
        :rtype: list[float] | float | None
        """
        raise NotImplementedError


class Port(AbstractPort):
    """A control port is a control variable with a invariant value domain.
    """

    def __init__(self, control_variable_name: str, value_domain: list[float], value_domain_type: VALUE_DOMAIN_TYPE, default_value: float = 0) -> None:  # dp: DataProvider, 
        super().__init__(control_variable_name, value_domain_type=value_domain_type, default_value=default_value)
        self._value_domain: list[float] = value_domain

    def value_domain(self, modes_values_k: dict[str, float] = None) -> list[float] | None:
        return self._value_domain


class ContinuousPort(Port):

    def __init__(self, control_variable_name: str, value_domain: list[float], default_value: float = 0) -> None:
        super().__init__(control_variable_name, value_domain=value_domain, value_domain_type=VALUE_DOMAIN_TYPE.CONTINUOUS, default_value=default_value)


class DiscretePort(Port):

    def __init__(self, control_variable_name: str, value_domain: list[float], default_value: float = 0) -> None:
        super().__init__(control_variable_name, value_domain=value_domain, value_domain_type=VALUE_DOMAIN_TYPE.DISCRETE, default_value=default_value)


class BinaryPort(DiscretePort):

    def __init__(self, control_variable_name: str, default_value: float = 0) -> None:
        super().__init__(control_variable_name, value_domain=(0, 1), default_value=default_value)


class ModePort(AbstractPort):

    def __init__(self, port_variable: str, mode_variable: str, mode_value_domains: dict[int, list[float]], value_domain_type: VALUE_DOMAIN_TYPE, default_value: float = 0, default_mode: int = 0) -> None:
        super().__init__(port_variable, value_domain_type=value_domain_type, default_value=default_value)
        self.mode_variable: str = mode_variable
        self.default_mode: int = default_mode
        if 0 not in mode_value_domains:
            raise ValueError('The mode_value_domain must contain the mode 0 (OFF)')
        self.mode_value_domains: dict[int, list[float]] = mode_value_domains
        if default_mode not in self.mode_value_domains:
            raise ValueError(f'The default mode {default_mode} is not defined in the mode_value_domain')
        self.mode_value_domains: dict[int, list[float]] = mode_value_domains

    def value_domain(self, modes_values: dict[str, float]) -> list[float] | None:
        """See parent class definition"""
        # mode: int | None = self.dp(self.mode_variable, k)
        if modes_values is not None and self.mode_variable not in modes_values:
            raise ValueError(f'The mode variable {self.mode_variable} is not defined in the modes_values')
        mode: int | None = modes_values[self.mode_variable]
        try:
            result: list[float] = self.mode_value_domains[int(mode)]
        except (KeyError, TypeError, ValueError):
            result: list[float] = self.mode_value_domains[self.default_mode]
        return result

    def __call__(self, modes_values: dict[str, float], port_value: float | None = None) -> list[float] | float | None:
        return super().__call__(modes_values, port_value)


class MultimodePort(AbstractPort):

    def __init__(self, port_variable: str, mode_variables: list[str], mode_value_domains: dict[tuple[int], list[float]], value_domain_type: VALUE_DOMAIN_TYPE, default_value: float = 0) -> None:
        super().__init__(port_variable, value_domain_type=value_domain_type, default_value=default_value)
        self.mode_variables: list[str] = mode_variables
        self.mode_value_domains: dict[tuple[int], list[float]] = mode_value_domains
        
    def __call__(self, modes_values: dict[str, float] = None, port_value: float | None = None) -> list[float] | float | None:
        possible_values: list[float] | None = self.possible_values(modes_values)
        if port_value is None:
            return possible_values
        if possible_values is None:
            return None
        port_value = port_value
        if self.value_domain_type == VALUE_DOMAIN_TYPE.DISCRETE:
            if port_value not in possible_values:
                distance_to_value = tuple([abs(port_value - value) for value in possible_values])
                port_value = possible_values[distance_to_value.index(min(distance_to_value))]
        else:
            port_value = port_value if port_value <= possible_values[1] else possible_values[1]
            port_value = port_value if port_value >= possible_values[0] else possible_values[0]
        return port_value
    
    def possible_values(self, modes_values: dict[str, float]) -> list[float] | None:
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

    def __init__(self, output_variable: str, binary_variables: list[str], multiplex: dict[tuple[int], tuple[float]], default_input_values: tuple[int], value_domain_type: VALUE_DOMAIN_TYPE, default_output_value: float = 0) -> None:
        super().__init__(output_variable, value_domain_type=value_domain_type, default_value=default_output_value)
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


class ZoneHvacContinuousPowerPort(ModePort):
    """A zoneHvacPowerPort is a Control port modeling a power supply with an upper bound both for heating and cooling. If mode=0, it's off and mode=1 or -1, it's on: 1 for heating and -1 for cooling.
    """

    def __init__(self, hvac_power_variable: str, hvac_mode: str, max_heating_power: float, max_cooling_power: float, default_value: float = 0, full_range: bool = False):
        if not full_range:
            super().__init__(hvac_power_variable, hvac_mode, mode_value_domains={1: [0, max_heating_power], 0: [0, 0], -1: [-max_cooling_power, 0]}, value_domain_type=VALUE_DOMAIN_TYPE.CONTINUOUS)
        else:
            super().__init__(hvac_power_variable, hvac_mode, mode_value_domains={1: (-max_cooling_power, max_heating_power), 0: 0, -1: (-max_cooling_power, max_heating_power)}, value_domain_type=VALUE_DOMAIN_TYPE.CONTINUOUS, default_value=default_value)
        self.mode_variable_name: str | None = hvac_mode


class ZoneTemperatureSetpointPort(ModePort):
    """A control port to model a temperature setpoint with discrete values depending on the heating mode. It is used in combination with a power port to model a temperature controller.
    """

    def __init__(self, temperature_setpoint_variable: str, mode_variable_name: str, mode_value_domains: dict[int, tuple[float]] = {1: (13, 19, 20, 21, 22, 23, 24), 0: None, -1: (24, 25, 26, 28, 29, 32)}, default_value: float = None) -> None:

        super().__init__(temperature_setpoint_variable, mode_variable_name, mode_value_domains, value_domain_type=VALUE_DOMAIN_TYPE.DISCRETE, default_value=default_value, default_mode=0)


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

    def __init__(self, nominal_state_model: StateModel, zone_temperature_variable: str, zone_temperature_setpoint_port: ZoneTemperatureSetpointPort, zone_hvac_power_port: ZoneHvacContinuousPowerPort) -> None:
        self.zone_power_variable: str = zone_hvac_power_port.port_variable
        self.zone_hvac_power_port: ZoneHvacContinuousPowerPort = zone_hvac_power_port
        self.hvac_zone_power_variable: str = zone_hvac_power_port.port_variable

        self.zone_temperature_setpoint_port: ZoneTemperatureSetpointPort = zone_temperature_setpoint_port
        self.zone_temperature_setpoint_variable: str = zone_temperature_setpoint_port.port_variable
        self.zone_temperature_variable: str = zone_temperature_variable

        self.input_names: list[str] = nominal_state_model.input_names
        self.input_index: int = nominal_state_model.input_names.index(self.zone_power_variable)
        self.output_names: list[str] = nominal_state_model.output_names
        self.output_index: int = nominal_state_model.output_names.index(self.zone_temperature_variable)

        D_condition: numpy.matrix = nominal_state_model.D[self.output_index, self.input_index]
        CB: numpy.matrix = nominal_state_model.C * nominal_state_model.B
        CB_condition: numpy.matrix = CB[self.output_index, self.input_index]
        if D_condition != 0:
            self.level = 0
        elif CB_condition != 0:
            self.level = 1
        else:
            raise ValueError(f'{self.zone_temperature_variable} cannot be controlled by {zone_hvac_power_port.port_variable}')

    def __repr__(self) -> str:
        return self.hvac_zone_power_variable + '>' + self.zone_temperature_variable

    def __str__(self) -> str:
        string: str = f'{self.zone_temperature_variable} is controlled by {self.hvac_zone_power_variable}, contributing to {self.zone_power_variable} at level {self.level} thanks to {self.zone_temperature_setpoint_port.port_variable}'
        return string

    def power_control_variable(self) -> str:
        return self.zone_power_variable

    def step(self, setpoint: float, state_model: StateModel, state: numpy.matrix, mode, current_context_inputs: dict[str, float], next_context_inputs: dict[str, float] = None) -> float:  # mode: int,
        if setpoint is None or numpy.isnan(setpoint) or type(setpoint) is float('nan'):
            return self.zone_hvac_power_port.port_variable, 0
        setpoint = self.zone_temperature_setpoint_port({'mode': mode}, setpoint)
        current_context_inputs[self.zone_power_variable] = self.zone_hvac_power_port({'mode': mode}, current_context_inputs[self.zone_power_variable])
        U_k = numpy.matrix([[current_context_inputs[input_name]] for input_name in self.input_names])
        if self.level == 0:
            delta_control_value: numpy.matrix = (setpoint - state_model.C[self.output_index, :] * state - state_model.D[self.output_index, :] * U_k) / state_model.D[self.output_index, self.input_index]
        elif self.level == 1:
            if next_context_inputs is None:
                raise ValueError("Inputs at time k and k+1 must be provided for level-1 controller {self.control_input_name} -> {self.controlled_output_name}")
            U_kp1 = numpy.matrix([[next_context_inputs[input_name]] for input_name in self.input_names])
            delta_control_value: numpy.matrix = (setpoint - state_model.C[self.output_index, :] * state_model.A * state - state_model.C[self.output_index, :] * state_model.B * U_k - state_model.D[self.output_index, :] * U_kp1) / (state_model.C[self.output_index] * state_model.B[:, self.input_index])
            delta_control_value = delta_control_value[0, 0]
        else:  # unknown level
            raise ValueError('Unknown controller level')
        return delta_control_value


class Manager(ABC):

    def __init__(self, dp: DataProvider, state_model_maker: BuildingStateModelMaker) -> None:
        self.dp: DataProvider = dp
        self.state_model_maker: BuildingStateModelMaker = state_model_maker
        self.datetimes: list[datetime] = self.dp.series('datetime')
        self.day_of_week: list[int] = self.dp('day_of_week')
        self.make_ports()
        self.controllers_with_initial_value: dict[ZoneTemperatureController, float] = self.zone_controllers_with_initial_value()

    def make_zone_temperature_controller(self, zone_temperature_name: str, temperature_setpoint_port: ZoneTemperatureSetpointPort, zone_power_variable: str, zone_hvac_power_port: ZoneHvacContinuousPowerPort) -> ZoneTemperatureController:
        return ZoneTemperatureController(self.state_model_maker.make_k(k=None), zone_temperature_name, temperature_setpoint_port, zone_power_variable, zone_hvac_power_port)

    @abstractmethod
    def make_ports(self) -> None:
        raise NotImplementedError("Method 'make_ports' of the manager must be implemented")

    @abstractmethod
    def zone_controllers_with_initial_value(self) -> dict[ZoneTemperatureController, float]:
        raise NotImplementedError("Method 'make_controllers' of the manager must be implemented")

    @abstractmethod
    def controls(self, k: int, kwargs: dict[str, Any]) -> None:
        raise NotImplementedError("Method 'controls' of the manager must be implemented")


class ControlModel:
    """The main class for simulating a living area with a control.
    """

    def __init__(self, building_state_model_maker: BuildingStateModelMaker, manager: Manager) -> None:
        self.building_state_model_maker: BuildingStateModelMaker = building_state_model_maker
        self.manager = manager
        self.dp: DataProvider = building_state_model_maker.data_provider
        self.airflows: list[Airflow] = building_state_model_maker.airflows
        self.nominal_fingerprint = self.dp.fingerprint(0)  # None
        self.state_model_k: StateModel = building_state_model_maker.make_k(k=0, reset_reduction=True, fingerprint=self.nominal_fingerprint)
        self.input_names: list[str] = self.state_model_k.input_names
        self.output_names: list[str] = self.state_model_k.output_names
        self.manager: Manager = manager
        self.state_models_cache: dict[int, StateModel] = {self.nominal_fingerprint: self.state_model_k}

    def simulate(self, suffix: str = ''):
        print("simulation running...")
        start: float = time.time()
        controller_controls: dict[str, list[float]] = {repr(controller): list() for controller in self.manager.controllers_with_initial_value}
        controller_setpoints: dict[str, list[float]] = {repr(controller): list() for controller in self.manager.controllers_with_initial_value}

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
                X_k: numpy.matrix = self.state_model_k.initialize(**inputs_k)
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
            for controller in self.manager.controllers_with_initial_value:
                controller_name: str = repr(controller)
                if controller.level == 0:
                    setpoint_k: float = self.dp(controller.zone_temperature_setpoint_variable, k)
                    control_k: float = controller.step(k, setpoint_k, state_model_k, X_k, inputs_k)
                elif controller.level == 1:
                    if k < len(self.dp) - 1:
                        setpoint_k: float = self.dp(controller.zone_temperature_setpoint_variable, k+1)
                    else:
                        setpoint_k: float = self.dp(controller.zone_temperature_setpoint_variable, k)
                control_k: float = controller.step(k, setpoint_k, state_model_k, X_k, inputs_k, inputs_kp1)
                controller_controls[controller_name].append(control_k)
                controller_setpoints[controller_name].append(setpoint_k)

                inputs_k[controller.zone_power_variable] = inputs_k[controller.zone_power_variable] + control_k
                self.dp(controller.zone_power_variable, k, control_k)

            state_model_k.set_state(X_k)
            output_values = state_model_k.output(**inputs_k)
            for output_index, output_name in enumerate(self.output_names):
                self.dp(output_name, k, output_values[output_index])
            X_k = state_model_k.step(**inputs_k)
        print(f"\nDuration in seconds {time.time() - start} with a state model cache size={len(self.state_models_cache)}")

    def __str__(self) -> str:
        string = 'ControlModel:'
        string += '\n-'.join([str(controller) for controller in self.manager.controllers_with_initial_value])
        return string

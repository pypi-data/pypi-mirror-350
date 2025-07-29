from core.data import DataProvider
from core.control import BinaryPort, ZoneHvacContinuousPowerPort, ZoneTemperatureSetpointPort, ZoneTemperatureController, ControlModel, Manager
from core.signal import Merger, SignalGenerator
from core.inhabitants import Preference
from sites.building_h358 import make_building_state_model_k
from core.model import BuildingStateModelMaker
from sites.data_h358 import make_data_provider
import numpy


def make_data_and_signals(starting_stringdate, ending_stringdate, heater: bool = True) -> DataProvider:
    dp: DataProvider = make_data_provider(starting_stringdate, ending_stringdate, heater=False)
    temperature_signal_generator = SignalGenerator(dp.series('datetime'))
    temperature_signal_generator.daily([0, 1, 2, 3, 4], {0: 13, 6: 21, 18: 13})
    temperature_signal_generator.daily([5, 6], {0: 13})
    heating_period = temperature_signal_generator.seasonal('15/10', '15/4')
    cooling_period_temperature_signal_generator = SignalGenerator(dp.series('datetime'))
    cooling_period_temperature_signal_generator.daily([0, 1, 2, 3, 4], {0: 29, 6: 24, 18: 29})
    cooling_period_temperature_signal_generator.daily([5, 6], {0: 29})
    cooling_period = cooling_period_temperature_signal_generator.seasonal('15/6', '15/9')
    temperature_signal_generator.combine(cooling_period_temperature_signal_generator())
    dp.add_external_variable('TZoffice_setpoint', temperature_signal_generator())

    hvac_modes_sgen = SignalGenerator(dp.series('datetime'))
    hvac_modes_sgen.combine(heating_period)
    hvac_modes_sgen.combine(cooling_period, merger=Merger(lambda x, y: x - y, 'n'))
    dp.add_external_variable('mode', hvac_modes_sgen())
    return dp


class DirectManager(Manager):

    def __init__(self, dp: DataProvider) -> None:
        self.building_state_model_maker, self.nominal_state_model = make_building_state_model_k(dp,  periodic_depth_seconds=60*60, state_model_order_max=5)
        # building_state_model = BuildingStateModel(state_model_maker)
        super().__init__(dp, self.building_state_model_maker)

    def make_ports(self) -> None:
        self.temperature_setpoint_port = ZoneTemperatureSetpointPort(self.dp, 'TZoffice_setpoint', mode_variable_name='mode', mode_value_domains={1: (13, 19, 20, 21, 22, 23), 0: (0,), -1: (24, 25, 26, 28, 29, 32)})

        self.mode_power_port = ZoneHvacContinuousPowerPort(self.dp, 'Pheater', max_heating_power=2000, max_cooling_power=2000, hvac_mode='mode', full_range=False)

        self.window_opening_port = BinaryPort(self.dp, 'window_opening', 'presence')

        self.door_opening_port = BinaryPort(self.dp, 'door_opening', 'presence')

    def zone_controllers_with_initial_value(self) -> dict[ZoneTemperatureController, float]:
        return {self.make_zone_temperature_controller('TZoffice', self.temperature_setpoint_port, 'PZoffice', self.mode_power_port): 20}

    def controls(self, k: int, X_k: numpy.matrix, current_output_dict: dict[str, float]) -> None:
        # if self.dp('presence', k) == 1:    ######### DESIGN YOUR OWN CONTROLS HERE #########
        #     self.window_opening_port(k, 1) # USE THE CONTROL PORTS FOR ACTION AND USE self.dp('variable', k) TO GET A VALUE
        pass


def make_simulation(direct_manager: DirectManager) -> None:
    dp: DataProvider = direct_manager.dp
    building_state_model_maker: BuildingStateModelMaker = direct_manager.building_state_model_maker

    preference = Preference(preferred_temperatures=(19, 24), extreme_temperatures=(16, 29), preferred_CO2_concentration=(500, 1500), temperature_weight_wrt_CO2=0.5, power_weight_wrt_comfort=0.5, mode_cop={1: 2, -1: 2})

    control_model = ControlModel(building_state_model_maker, direct_manager)
    print(control_model)
    control_model.simulate()

    preference.print_assessment(dp.series('datetime'), Pheater=dp.series('Pheater'), temperatures=dp.series('TZoffice'), CO2_concentrations=dp.series('CCO2office'), occupancies=dp.series('occupancy'), action_sets=(dp.series('window_opening'), dp.series('door_opening')), modes=dp.series('mode'))
    dp.plot()


dp: DataProvider = make_data_and_signals('15/02/2015', '15/02/2016', heater=False)
direct_manager = DirectManager(dp)
make_simulation(direct_manager)

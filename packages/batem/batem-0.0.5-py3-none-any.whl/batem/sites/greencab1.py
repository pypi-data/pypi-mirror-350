import numpy
import time
from core.data import DataProvider, Bindings
from core.signal import SignalGenerator, Merger
from core.solar import SolarModel, SolarSystem, Collector
from core.data import DataProvider, Bindings
from core.model import BuildingStateModelMaker
from core.components import SideFactory
from core.control import ZoneTemperatureSetpointPort, ZoneTemperatureController, ControlModel, AirflowPort, ZoneHvacContinuousPowerPort, Manager
from core.signal import SignalGenerator, Merger
from core.inhabitants import Preference
from core.library import SIDE_TYPES, DIRECTIONS_SREF, SLOPES

surface_window = 1.8 * 1.9
direction_window = -90
solar_protection = 90  # no protection
solar_factor = 0.56
cabinet_length = 5.77
cabinet_width = 2.21
cabinet_height = 2.29
body_metabolism = 100
occupant_consumption = 200
body_PCO2 = 7

# Consequences
surface_cabinet: float = cabinet_length*cabinet_width
volume_cabinet: float = surface_cabinet*cabinet_height
surface_cabinet_wall: float = 2 * (cabinet_length + cabinet_width) * cabinet_height - surface_window
q_infiltration: float = volume_cabinet / 3600


def make_data_and_signals(starting_stringdate="1/1/2022", ending_stringdate="5/1/2023") -> DataProvider:
    bindings = Bindings()
    bindings('TZoutdoor', 'weather_temperature')
    
    dp = DataProvider(location='Saint-Julien-en-Saint-Alban', latitude_deg_north=44.71407488275519, longitude_deg_east=4.633318302898348, starting_stringdate=starting_stringdate, ending_stringdate=ending_stringdate, bindings=bindings, albedo=0.1, pollution=0.1, number_of_levels=4)
    
    solar_model = SolarModel(dp.weather_data)
    dp.solar_model = solar_model
    solar_system = SolarSystem(solar_model)
    Collector(solar_system, 'main', surface_m2=surface_window, exposure_deg=direction_window, slope_deg=90, solar_factor=solar_factor)
    solar_gains_with_mask = solar_system.powers_W()
    dp.add_external_variable('Psun_window', solar_gains_with_mask)

    occupancy_signal_generator = SignalGenerator(dp.series('datetime'))
    occupancy_signal_generator.daily([0, 1, 2, 3, 4], {0: 0, 8: 3, 18: 0})  # 12: 0, 13: 3,
    occupancy: list[float] = occupancy_signal_generator()
    dp.add_external_variable('occupancy', occupancy)
    presence: list[int] = [int(occupancy[k] > 0) for k in range(len(dp))]
    dp.add_external_variable('presence', presence)

    dp.add_external_variable('PZcabinet', [occupancy[k] * (body_metabolism + occupant_consumption) + solar_gains_with_mask[k] for k in dp.ks])
    
    # Data heating and cooling
    temperature_sgen = SignalGenerator(dp.series('datetime'), None)
    temperature_sgen.daily([0, 1, 2, 3, 4], {0: None, 7: 20, 19: None}, merger=Merger(min, 'r'))
    heating_period = temperature_sgen.seasonal('16/11', '15/3', 1, merger=Merger(max, 'b'))
    temp_sgen = SignalGenerator(dp.series('datetime'), None)
    temp_sgen.daily([0, 1, 2, 3, 4], {0: None, 7: 22, 19: None}, merger=Merger(min, 'r'))
    cooling_period = temp_sgen.seasonal('16/3', '15/11', 1, merger=Merger(max, 'b'))
    temperature_sgen.combine(temp_sgen(), merger=Merger(min, 'n'))
    dp.add_external_variable('TZcabinet_setpoint', temperature_sgen())

    hvac_modes_sgen = SignalGenerator(dp.series('datetime'))
    hvac_modes_sgen.combine(heating_period, merger=Merger(max, 'l'))
    hvac_modes_sgen.combine(cooling_period, merger=Merger(lambda x, y: x - y, 'n'))
    dp.add_external_variable('mode', hvac_modes_sgen())
    
    dp.add_parameter('CCO2outdoor', 400)
    dp.add_parameter('cabinet-outdoor:Q', q_infiltration)
    dp.add_parameter('cabinet:volume', volume_cabinet)
    dp.add_external_variable('PCO2cabinet', [body_PCO2 * occupancy[k] for k in range(len(dp))])
    
    return dp


def make_state_model_maker(dp: DataProvider) -> BuildingStateModelMaker:
    state_model_maker = BuildingStateModelMaker('cabinet', data_provider=dp, periodic_depth_seconds=3600, state_model_order_max=5)
    
    wall = SideFactory(('plaster', 13e-3), ('steel', 5e-3), ('wood', 3e-3))
    floor = SideFactory(('wood', 10e-3), ('steel', 5e-3))
    ceiling = SideFactory(('plaster', 13e-3), ('steel', 5e-3))
    glazing = SideFactory(('glass', 4e-3), ('air', 10e-3), ('glass', 4e-3), ('air', 10e-3), ('glass', 4e-3))

    # Cabinet
    state_model_maker.make_side(wall('cabinet', 'outdoor', SIDE_TYPES.WALL, surface_cabinet_wall))
    state_model_maker.make_side(floor('cabinet', 'outdoor', SIDE_TYPES.FLOOR, surface_cabinet))
    state_model_maker.make_side(ceiling('cabinet', 'outdoor', SIDE_TYPES.CEILING, surface_cabinet))
    state_model_maker.make_side(glazing('cabinet', 'outdoor', SIDE_TYPES.GLAZING, surface_window))
    state_model_maker.simulate_zone('cabinet')
    state_model_maker.connect_airflow('cabinet', 'outdoor', dp('cabinet-outdoor:Q'))  # nominal value
    print(state_model_maker)
    
    return state_model_maker, state_model_maker.make_k()


class DirectManager(Manager):

    def __init__(self, dp: DataProvider, building_state_model_maker: BuildingStateModelMaker) -> None:
        super().__init__(dp, building_state_model_maker)

    def make_ports(self) -> None:

        self.temperature_setpoint_port = ZoneTemperatureSetpointPort(self.dp, 'TZcabinet_setpoint', mode_variable_name='mode', mode_value_domains={1: (13, 19, 20, 21, 22, 23), 0: None, -1: (24, 25, 26, 28, 29, 32)})

        self.mode_power_control_port = ZoneHvacContinuousPowerPort(self.dp, 'Pheater', max_heating_power=3000, max_cooling_power=3000, hvac_mode='mode', full_range=False)

    def zone_controllers_with_initial_value(self) -> dict[ZoneTemperatureController, float]:
        return {self.make_zone_temperature_controller('TZcabinet', self.temperature_setpoint_port, 'PZcabinet', self.mode_power_control_port): 20}

    def controls(self, k: int, X_k: numpy.matrix, current_output_dict: dict[str, float]) -> None:
        pass


def make_simulation(dp: DataProvider, building_state_model_maker: BuildingStateModelMaker) -> None:

    manager = DirectManager(dp, building_state_model_maker)
    preference = Preference(preferred_temperatures=(19, 24), extreme_temperatures=(16, 29), preferred_CO2_concentration=(500, 1500), temperature_weight_wrt_CO2=0.5, power_weight_wrt_comfort=0.5, mode_cop={1: 2, -1: 2})

    control_model = ControlModel(building_state_model_maker, manager)
    print(control_model)
    start: float = time.time()
    control_model.simulate()
    print('\nmodel simulation duration: %f secondes' % (time.time() - start))

    Pheater: list[float] = dp.series('Pheater')
    occupancy = dp.series('occupancy')
    preference.print_assessment(dp.series('datetime'), Pheater=Pheater, temperatures=dp.series('TZcabinet'), CO2_concentrations=dp.series('CCO2cabinet'), occupancies=dp.series('occupancy'), action_sets=(), modes=dp.series('mode'), list_extreme_hours=True)
    electricity_needs = [abs(Pheater[k])/2 + occupancy[k] * occupant_consumption for k in dp.ks]
    dp.add_external_variable('electricity needs', electricity_needs)

    exposure_in_deg = 0
    slope_in_deg = 180
    solar_factor = .2
    surface = 7
    solar_system = SolarSystem(dp.solar_model)
    Collector(solar_system, 'PVpanel', surface_m2=surface, exposure_deg=exposure_in_deg, slope_deg=slope_in_deg, solar_factor=solar_factor)
    global_productions_in_Wh = solar_system.solar_gains_W()
    print('PV production in kWh:', round(sum(global_productions_in_Wh) / 1000))
    dp.add_external_variable('productionPV', global_productions_in_Wh)
    dp.plot()
    
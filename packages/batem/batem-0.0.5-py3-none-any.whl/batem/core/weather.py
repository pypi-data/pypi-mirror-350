"""This is a reader for openweathermap (https://openweathermap.org) historical weather files.

Author: stephane.ploix@grenoble-inp.fr
"""
from __future__ import annotations
import json
import requests
import configparser
import os
import sys
import glob
import pytz
from datetime import datetime
from math import exp
from .timemg import datetime_to_epochtimems, datetime_with_day_delta, epochtimems_to_datetime, epochtimems_to_stringdate, openmeteo_to_stringdate, stringdate_to_openmeteo_date, stringdate_to_epochtimems
from .utils import TimeSeriesPlotter
from timezonefinder import TimezoneFinder
config = configparser.ConfigParser()
config.read('setup.ini')


def absolute_humidity_kg_per_m3(temperature_deg: float, relative_humidity_percent: float) -> float:
    Rv_J_per_kg_K = 461.5  # J/kg.K
    saturation_vapour_pressure_Pa: float = 611.213 * exp(17.5043 * temperature_deg / (temperature_deg + 241.2))  # empirical formula of Magnus-Tetens
    partial_vapour_pressure_Pa: float = saturation_vapour_pressure_Pa * relative_humidity_percent / 100
    return partial_vapour_pressure_Pa / (Rv_J_per_kg_K * (temperature_deg + 273.15))


def absolute_humidity_kg_per_kg(temperature_deg: float, relative_humidity_percent: float, atmospheric_pressures_hPa: float = 1013.25) -> float:
    Rs_J_per_kg_K = 287.06
    density_kg_per_m3 = (atmospheric_pressures_hPa * 100 - 2.30617*relative_humidity_percent*exp(17.5043*temperature_deg/(241.2+temperature_deg)))/Rs_J_per_kg_K/(temperature_deg + 273.15)
    return absolute_humidity_kg_per_m3(temperature_deg, relative_humidity_percent) / density_kg_per_m3


def relative_humidity(temperature_deg, absolute_humidity_kg_per_m3) -> float:
    Rv_J_per_kg_K = 461.5  # J/kg.K
    saturation_vapour_pressure_Pa: float = 611.213 * exp(17.5043 * temperature_deg / (temperature_deg + 241.2))  # empirical formula of Magnus-Tetens
    partial_vapour_pressure_Pa: float = absolute_humidity_kg_per_m3 * Rv_J_per_kg_K * (temperature_deg + 273.15)
    return 100 * partial_vapour_pressure_Pa / saturation_vapour_pressure_Pa


class ElevationRetriever:
    """create or get elevations from google website corresponding to a localization characterized by a longitude and latitude. To avoid offline issues with Internet, anytime an elevation is collected, it is stored into the localizations.json file in order to use it a next time.
    """

    def __init__(self, json_database_name: str = 'localizations.json') -> None:
        """initializer of the elevation retriever
        :param json_database_name: name of the file where longitudes, latitudes and elevations are saved, defaults to 'localizations.json'
        :type json_database_name: str, optional
        """
        if not os.path.isdir(config['folders']['data']):
            os.mkdir(config['folders']['data'])
        filename: str = config['folders']['data'] + json_database_name
        self.json_database_name = filename
        if not os.path.isfile(filename):
            self.data = dict()
        else:
            with open(filename) as json_file:
                self.data: dict[tuple[str, str], str] = json.load(json_file)

    def get(self, longitude_deg_east: float, latitude_deg_north: float) -> float | tuple[float, float, float]:
        """functor returning the complete coordinate with the elevation or just the elevation at a given longitude and latitude
        :param longitude_deg_east: longitude in degree east
        :type longitude_deg_east: DMS or (degree, minute, seconde) | decimal angle
        :param latitude_deg_north: latitude in degree north
        :type latitude_deg_north: DMS or (degree, minute, seconde) | decimal angle
        :param elevation_only: True for elevation only, longitude, latitude and elevation otherwise, defaults to False
        :type elevation_only: bool, optional
        :return: longitude, latitude and elevation or just elevation
        :rtype: float | tuple[float, float, float]
        """
        coordinate = '(%s,%s)' % (longitude_deg_east, latitude_deg_north)
        if coordinate not in self.data:
            elevation = 200
            try:
                elevation = ElevationRetriever._webapi_elevation_meter(longitude_deg_east, latitude_deg_north)
            except:
                elevation = float(input('Enter manually the elevation:'))
            self.data[coordinate] = elevation
            with open(self.json_database_name, 'w') as json_file:
                json.dump(self.data, json_file)
        else:
            elevation: float = self.data[coordinate]
        return elevation

    def _webapi_elevation_meter(longitude_deg_east: float, latitude_deg_north: float) -> float:
        """search in local database if the coordinates exists, if so it gets the elevation in meters from google and add to the database.
        :param latitude_deg_north: north degree latitude
        :type latitude_deg_north: float
        :param longitude_deg_east: east degree longitude
        :type longitude_deg_east: float
        :return: the collected elevation
        :rtype: float
        """

        url = 'https://api.open-elevation.com/api/v1/lookup'

        params = {"locations": [{"latitude": latitude_deg_north, "longitude": longitude_deg_east}]}
        response = requests.post(url, json=params)
        try:
            response.raise_for_status()
            for info in response:
                print(info, response)

            data = response.json()
            elevations = [result['elevation'] for result in data['results']]
            return elevations[0]
        except requests.HTTPError as error:
            print("The elevation server does not respond: horizon mask has to be set manually.", error)
            elevation = int(input('Elevation in m: '))
            return elevation


class WeatherJsonReader:
    """Extract the content of a json openweather data file.

    :param json_filename: openweather data file in json format
    :param from_stringdate: initial date in format DD/MM/YYYY hh:mm:ss
    :param to_stringdate: final date in format DD/MM/YYYY hh:mm:ss
    :return: a tuple containing
        - city file_name
        - latitude in decimal north degree
        - longitude in decimal east degree
        - hourly time data variables as a dictionary with variable file_name as a key
        - units as a dictionary with variable file_name as a key
        - initial date as a string
        - final date as a string
    """

    def analyze_weather_files() -> None:
        print("Available weather files:\n")
        json_filenames: list[str] = glob.glob(config['folders']['data'] + '*.json')
        for json_filename in json_filenames:
            if not json_filename.endswith('localizations.json'):
                print('- ' + json_filename)
                weather_locations = list()
                with open(json_filename) as json_file:
                    json_content = json.load(json_file)
                    if 'generationtime_ms' in json_content:  # openmeteo file
                        location = json_filename.split('.json')[0].split('/')[-1]
                        weather_locations.append(location)
                        from_stringdate = epochtimems_to_stringdate(json_content['hourly']['epochtimems'][0])
                        to_stringdate = epochtimems_to_stringdate(json_content['hourly']['epochtimems'][-1])
                        print('\t- [open-meteo] "%s" (lat:%f,lon:%f) from %s to %s' % (location, float(json_content['latitude']), float(json_content['longitude']), openmeteo_to_stringdate(from_stringdate), openmeteo_to_stringdate(to_stringdate)))
                    else:  # openweathtermap file
                        for i in range(len(json_content)):
                            weather_location = json_content[i]['city_name']
                            if len(weather_locations) == 0 or weather_locations[-1] != weather_location:
                                weather_locations.append(weather_location)
                        for city_name in weather_locations:
                            print('\t- [openweathermap] "%s" latitude,longitude=(%f,%f) from %s to %s' % (city_name, float(json_content[0]['lat']), float(json_content[0]['lon']), epochtimems_to_stringdate(int(json_content[0]['dt'])*1000), epochtimems_to_stringdate(int(json_content[-1]['dt'])*1000)))

    @staticmethod
    def create_open_meteoDB(weather_file_name: str, latitude_deg_north: float, longitude_deg_east: float, weather_data: tuple[str] = ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "dew_point_2m", "precipitation", "rain", "showers", "snowfall", "snow_depth", "surface_pressure", "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m", "soil_temperature_0cm", "shortwave_radiation", "direct_radiation", "diffuse_radiation", "direct_normal_irradiance", "shortwave_radiation_instant", "direct_radiation_instant", "diffuse_radiation_instant", "direct_normal_irradiance_instant", "terrestrial_radiation_instant"], timezone: pytz.timezone = None) -> None:
        
        server_url = 'https://archive-api.open-meteo.com/v1/archive'
        if weather_file_name.endswith('.json'):
            weather_file_name = weather_file_name.split('.json')[0]
        if os.path.isfile(weather_file_name+'.json'):
            os.remove(weather_file_name+'.json')
        to_openmeteo_string_date: str = datetime_with_day_delta(datetime.now(timezone), number_of_days=-7, date_format='%d/%m/%Y')
        from_openmeteo_string_date: str = stringdate_to_openmeteo_date('1/1/1980', timezone)
        to_openmeteo_string_date = stringdate_to_openmeteo_date(to_openmeteo_string_date, timezone)

        response: requests.Response = requests.get(server_url, params={"latitude": latitude_deg_north, "longitude": longitude_deg_east, "start_date": from_openmeteo_string_date, "end_date": to_openmeteo_string_date, "hourly": weather_data}, headers={'Accept': 'application/json'}, timeout=300, stream=True)
        data: str = response.json()
        if 'error' in data:
            raise ValueError(data['reason'])
        data['site_latitude'] = latitude_deg_north
        data['site_longitude'] = longitude_deg_east
        data['timezone'] = timezone
        number_of_data_to_removed = 0
        for k in range(len(data['hourly']['time'])-1, -1, -1):
            if data['hourly']['temperature_2m'][k] is None:
                number_of_data_to_removed += 1
            else:
                break
        for v in data['hourly']:
            for i in range(number_of_data_to_removed):
                data['hourly'][v].pop(-1)
        data['hourly']['epochtimems'] = list()
        for openmeteo_stringtime in data['hourly']['time']:
            data['hourly']['epochtimems'].append(stringdate_to_epochtimems(openmeteo_stringtime, date_format='%Y-%m-%dT%H:%M', timezone_str=timezone))
        del data['hourly']['time']
        with open(config['folders']['data'] + weather_file_name + '.json', 'w') as json_file:
            json.dump(data, json_file)

    def __init__(self, location: str = None, albedo: float = .1, pollution: float = 0.1, latitude_north_deg: float = None, longitude_east_deg: float = None, from_requested_stringdate: str = None, to_requested_stringdate: str = None) -> None:
        """Read data from an openweather map json file.

        :param json_filename: name of the openweathermap historical weather file
        :type json_filename: str
        :param from_stringdate: starting date for the data collection, defaults to None
        :type from_stringdate: str: dd/mm/YY, optional
        :param to_stringdate: ending date for the data collection, defaults to None
        :type to_stringdate: str: dd/mm/YY, optional
        :param altitude: sea level in meter of the site location, defaults to 290
        :type altitude: float, optional
        :param albedo: albedo at current site location (see https://en.wikipedia.org/wiki/Albedo), defaults to .1
        :type albedo: float, optional
        :param pollution: turbidity coefficient to model the air pollution at the current site location, defaults to 0.1
        :type pollution: float, optional
        :param location: name of the location to select, if None, the first location name is selected
        :type location: str, defaults to None
        :param solar_model: True to use the solar model, False to use the weather data, defaults to False
        :type solar_model: bool, optional
        """

        # if from_requested_stringdate is None:
        #     from_requested_stringdate = '1/1/%i' % year
        # if to_requested_stringdate is None:
        #     to_requested_stringdate = '31/12/%i' % year
        if location.endswith('.json'):
            weather_file_name = location.rsplit('.json', 1)[0]
        if not os.path.isdir(config['folders']['data']):
            os.mkdir(config['folders']['data'])
        full_json_file_name: str = config['folders']['data'] + location + '.json'
        json_file_name: str = location + '.json'
        print("json weather file name is: %s" % full_json_file_name, file=sys.stderr)
        if location is None:
            location = weather_file_name

        if not os.path.isfile(full_json_file_name):  # load data from open-meteo.com and generate a weather file if not existing
            print('Weather file named %s not found: generate the missing json weather file' % full_json_file_name)
            WeatherJsonReader.create_open_meteoDB(json_file_name, latitude_north_deg, longitude_east_deg)

        with open(full_json_file_name) as json_file:
            weather_records = json.load(json_file)

            if 'error' in weather_records:
                raise ValueError(f'Delete file {full_json_file_name} and try because %s\n' % weather_records['reason'])

            elif 'generationtime_ms' in weather_records:
                print('Open-Meteo format selected', file=sys.stderr)
                if latitude_north_deg is None:
                    latitude_north_deg = float(weather_records['site_latitude'])
                if longitude_east_deg is None:
                    longitude_east_deg = float(weather_records['site_longitude'])
                timezone_finder = TimezoneFinder()
                self.timezone_str: str = timezone_finder.timezone_at(lat=latitude_north_deg, lng=longitude_east_deg)
                self.from_stringdate: str = from_requested_stringdate
                if from_requested_stringdate is not None:
                    self.requested_from_epochtimems: int = stringdate_to_epochtimems(from_requested_stringdate + ' 0:00:00', date_format='%d/%m/%Y %H:%M:%S', timezone_str=self.timezone_str)
                else:
                    self.requested_from_epochtimems = None
                self.to_stringdate: str = to_requested_stringdate
                if to_requested_stringdate is not None:
                    self.requested_to_epochtimems: int = stringdate_to_epochtimems(to_requested_stringdate + ' 23:00:00', date_format='%d/%m/%Y %H:%M:%S', timezone_str=self.timezone_str)
                else:
                    self.requested_to_epochtimems = None

                recorded_from_epochtimems: int = weather_records['hourly']['epochtimems'][0]
                recorded_to_epochtimems: int = weather_records['hourly']['epochtimems'][-1]
                if self.requested_from_epochtimems is not None and recorded_from_epochtimems > self.requested_from_epochtimems:
                    print("Beware: earliest requested date older than the recorded one", file=sys.stderr)
                if self.requested_to_epochtimems is not None and recorded_to_epochtimems < self.requested_to_epochtimems:
                    print("Beware: latest requested date more recent than the recorded one", file=sys.stderr)
                equivalence_openmeteo_weather_variables: dict[str, str] = {'temperature_2m': 'temperature', 'wind_speed_10m': 'wind_speed', 'wind_direction_10m': 'wind_direction_in_deg', 'apparent_temperature': 'feels_like', 'relative_humidity_2m': 'humidity', 'cloud_cover': 'cloudiness', 'surface_pressure': 'pressure'}

                weather_variables_values: dict[str, list[float]] = dict()
                weather_variables_units: dict[str, str] = {}  # {'epochtimems': 'ms'}
                weather_epochtimems: list[float] = list()
                openmeteo_epochtimems = weather_records['hourly']['epochtimems']
                openmeteo_variable_names = list(weather_records['hourly'].keys())
                openmeteo_variable_names.remove('epochtimems')
                if self.requested_from_epochtimems is None:
                    self.requested_from_epochtimems = openmeteo_epochtimems[0]
                if self.requested_to_epochtimems is None:
                    self.requested_to_epochtimems = openmeteo_epochtimems[-1]
                for k in range(len(openmeteo_epochtimems)):
                    if self.requested_from_epochtimems <= openmeteo_epochtimems[k] <= self.requested_to_epochtimems:
                        if len(weather_epochtimems) == 0:  # first data read
                            weather_epochtimems.append(openmeteo_epochtimems[k])
                            for openmeteo_variable_name in openmeteo_variable_names:
                                weather_variable_name = equivalence_openmeteo_weather_variables[openmeteo_variable_name] if openmeteo_variable_name in equivalence_openmeteo_weather_variables else openmeteo_variable_name
                                weather_variables_units[weather_variable_name] = weather_records['hourly_units'][openmeteo_variable_name]
                                weather_variables_values[weather_variable_name] = [weather_records['hourly'][openmeteo_variable_name][k]]
                        else:
                            delta_ms: float = (openmeteo_epochtimems[k] - openmeteo_epochtimems[k-1])
                            if delta_ms == 2 * 3600 * 1000:  # autumn time shift
                                weather_epochtimems.append(openmeteo_epochtimems[k-1] + 3600 * 1000)
                                for openmeteo_variable_name in openmeteo_variable_names:
                                    weather_variable_name = equivalence_openmeteo_weather_variables[openmeteo_variable_name] if openmeteo_variable_name in equivalence_openmeteo_weather_variables else openmeteo_variable_name
                                    weather_variables_values[weather_variable_name].append(weather_records['hourly'][openmeteo_variable_name][k-1])
                            if delta_ms > 0:
                                weather_epochtimems.append(openmeteo_epochtimems[k])
                                for openmeteo_variable_name in openmeteo_variable_names:
                                    weather_variable_name = equivalence_openmeteo_weather_variables[openmeteo_variable_name] if openmeteo_variable_name in equivalence_openmeteo_weather_variables else openmeteo_variable_name
                                    weather_variables_values[weather_variable_name].append(weather_records['hourly'][openmeteo_variable_name][k-1])
                self.site_weather_data = SiteWeatherData(location, latitude_north_deg, longitude_east_deg, albedo=albedo, pollution=pollution, _direct_call=False)
                self.site_weather_data.epochtimems = weather_epochtimems
                for weather_variable_name in weather_variables_values:
                    self.site_weather_data.add_variable(weather_variable_name, weather_variables_units[weather_variable_name], weather_variables_values[weather_variable_name])
                # if 'humidity_mass' in self.site_weather_data.variable_names:
                self.site_weather_data.add_variable('absolute_humidity', 'kg water/kg air', self.site_weather_data.absolute_humidity_kg_per_kg())
                self.site_weather_data.add_variable('precipitation_mass', 'kg/m2/s', [p/1000/60 for p in self.site_weather_data.get('precipitation')])
                self.site_weather_data.add_variable('snowfall_mass', 'kg/m2/s', [p/1000/60 for p in self.site_weather_data.get('snowfall')])
                self.site_weather_data.add_variable('wind_speed_m_per_s', 'm/s', [p/3.6 for p in self.site_weather_data.get('wind_speed')])
                self.site_weather_data.origin = "openmeteo"


class SiteWeatherData:
    """Gathers all the data related to a site dealing with location, albedo, pollution, timezone but also weather time data coming from an openweather json file."""

    def __init__(self, location: str, latitude_deg_north: float, longitude_deg_east: float, albedo: float = .1, pollution: float = .1, timezone_str: str = None, _direct_call: bool = True) -> None:
        """Create object containing data dealing with a specific site, including the weather data.

        :param location: name of the site
        :type location: str
        :param latitude_deg_north: latitude in East degree
        :type latitude_deg_north: float
        :param longitude_deg_east: longitude in North degree
        :type longitude_deg_east: float
        :param variable_names: name of the weather variables
        :type variable_names: tuple[str]
        :param variable_units: units of the weather variables
        :type variable_units: tuple[str]
        :param altitude: altitude of the site in meter from sea level, defaults to 290
        :type altitude: float, optional
        :param albedo: albedo of the site, defaults to .1
        :type albedo: float, optional
        :param timezone: timezone of the site, defaults to 'Europe/Paris'
        :type timezone: str, optional
        :param pollution: pollution coefficient between 0 and 1, defaults to 0.1
        :type pollution: float, optional
        :param _direct_call: internal use to prohibit direct calls of the initializer, defaults to True
        :type _direct_call: bool, optional
        :raises PermissionError: raised in case of direct use, the object must be created by OpenWeatherMapJsonReader
        """
        if _direct_call:
            raise PermissionError('SiteWeatherData cannot be called directly')
        self.origin: str = 'undefined'
        self.location: str = location
        self.latitude_deg_north: float = latitude_deg_north
        self.longitude_deg_east: float = longitude_deg_east
        if timezone_str is None:
            timezone_finder = TimezoneFinder()
            self.timezone_str = timezone_finder.timezone_at(lat=latitude_deg_north, lng=longitude_deg_east)
        else:
            self.timezone_str = timezone_str

        self.elevation: float | tuple[float, float, float] = ElevationRetriever().get(latitude_deg_north, longitude_deg_east)
        self.albedo: float = albedo
        self.pollution: float = pollution
        self._epochtimems = list()
        self._datetimes = list()
        self._stringdates = list()
        self._variable_data = dict()
        self.variable_units = dict()

    def remove(self, variable_name: str) -> bool:
        if variable_name in self._variable_data:
            del self._variable_data[variable_name]
            del self.variable_units[variable_name]

    def __contains__(self, variable_name: str) -> bool:
        return variable_name in self._variable_data

    @property
    def variable_names(self) -> list[str]:
        return list(self._variable_data.keys())

    @property
    def variable_names_without_time(self) -> list[str]:
        variable_names_without_time = list()
        for v in self._variable_data:
            if v not in ('datetime', 'stringdate', 'epochtimems'):
                variable_names_without_time.append(v)
        return variable_names_without_time

    def check(self) -> None:
        length = None
        if len(self._epochtimems) > 0:
            length = len(self._epochtimems)
        for variable in self._variable_data:
            if length is not None:
                if len(self._variable_data[variable]) != length:
                    raise ValueError('Variable %s has not a correct length (%i instead of %i)' % (variable, len(self._variable_data[variable]), length))
            else:
                length = len(self._variable_data[variable])

    def __len__(self) -> int:
        return len(self._epochtimems)

    def excerpt(self, from_stringdate: str, to_stringdate: str) -> "SiteWeatherData":
        excerpt_site_weather_data = SiteWeatherData(self.location, self.latitude_deg_north, self.longitude_deg_east, self.albedo, self.pollution, self.timezone_str,  _direct_call=False)  # self.variable_names, self._variable_units,
        excerpt_site_weather_data.origin = self.origin
        indices: list[int] = list()
        from_epochtimems: float = stringdate_to_epochtimems(from_stringdate + ' 0:00:00', timezone_str=self.timezone_str)
        if from_epochtimems < self._epochtimems[0]:
            raise ValueError('to stringdate (%s: 0:00:00) is greater than the one of the existing dataset')
        to_epochtimems: float = stringdate_to_epochtimems(to_stringdate + ' 23:00:00', timezone_str=self.timezone_str)
        if to_epochtimems > self._epochtimems[-1]:
            raise ValueError('from stringdate (%s: 0:00:00) is lower than the one of the existing dataset')

        excerpt_epochtimems = list()
        for i, t in enumerate(self._epochtimems):
            if from_epochtimems <= t <= to_epochtimems:
                indices.append(i)
                excerpt_epochtimems.append(t)
        excerpt_site_weather_data.epochtimems = excerpt_epochtimems
        for variable_name in self._variable_data:
            excerpt_site_weather_data.add_variable(variable_name, self.variable_units[variable_name], [self._variable_data[variable_name][i] for i in indices])
        return excerpt_site_weather_data

    def excerpt_year(self, year: int) -> "SiteWeatherData":
        return self.excerpt('1/1/%i' % year, '31/12/%i' % year)

    def __str__(self) -> str:
        string: str = "site is %s (lat:%f,lon:%f) " % (self.location, self.latitude_deg_north, self.longitude_deg_east)
        if self._epochtimems is not None:
            string += "with data from %s to %s\nweather variables are:\n" % (epochtimems_to_stringdate(self._epochtimems[0]), epochtimems_to_stringdate(self._epochtimems[-1]))
        else:
            string += "without data loaded yet\nweather variables are:\n"
        for v in self._variable_data:
            string += '- %s (%s)\n' % (v, self.variable_units[v])
        return string

    def units(self, variable_name: str = None):
        """Return the unit of a variable.

        :param variable_name: file_name of the variable
        :type variable_name: str
        :return: unit of this variable
        :rtype: str
        """
        if variable_name is None:
            return self.variable_units
        return self.variable_units[variable_name]

    @property
    def from_stringdate(self) -> str:
        """Return the starting data of the data collection.

        :return: first date where data are available in epoch time (ms)
        :rtype: int
        """
        return self._stringdates[0]

    @property
    def to_stringdate(self):
        """Return the ending date of the data collection.

        :return: last date where data are available
        :rtype: str
        """
        return self._stringdates[-1]

    @property
    def epochtimems(self) -> list[float]:
        return self._epochtimems

    @property
    def datetimes(self) -> list[datetime]:
        return self._datetimes

    @property
    def stringdates(self) -> list[str]:
        return self._stringdates

    @epochtimems.setter
    def epochtimems(self, the_epochtimems: list[float]):
        if type(the_epochtimems) is not list and type(the_epochtimems) is not tuple:
            raise ValueError("epochtimems must be a list or a tuple")
        self._epochtimems: list[float] = the_epochtimems
        self._stringdates: list[str] = [epochtimems_to_stringdate(t, timezone_str=self.timezone_str) for t in self._epochtimems]
        self._datetimes: list[datetime] = [epochtimems_to_datetime(t, timezone_str=self.timezone_str) for t in self._epochtimems]

    @datetimes.setter
    def datetimes(self, the_datetimes):
        if type(the_datetimes) is not list and type(the_datetimes) is not tuple:
            raise ValueError("datetimes must be a list or a tuple")
        self._datetimes: list[datetime] = the_datetimes
        self._epochtimems: list[float] = [datetime_to_epochtimems(dt) for dt in the_datetimes]
        self._datetimes: list[datetime] = [epochtimems_to_datetime(t, timezone_str=self.timezone_str) for t in self._epochtimems]

    def add_variable(self, variable_name: str, variable_unit: str, values: list[float | datetime]):
        if variable_name == 'epochtimems':
            self._epochtimems = [v - self.timezone_str / 3600000 for v in values]
        elif variable_name == 'stringdate':
            raise ValueError('string dates cannot be added directly: add epochtimems or datetimes instead')
        elif variable_name == 'datetime':
            self._epochtimems = [v.tz_convert(self.timezone_str) for v in values]
        else:
            self.variable_units[variable_name] = variable_unit
            self._variable_data[variable_name] = values

    def series(self, variable_name: str = None) -> list[float] | dict[str, list[float]]:
        if variable_name is not None:
            return self.get(variable_name)
        else:
            variable_values = dict()
            for variable_name in self.variable_names:
                if variable_name not in ('datetime', 'epochtimems', 'stringdate'):
                    variable_values[variable_name] = self.get(variable_name)
            return variable_values

    def __call__(self, variable_name: str) -> list[float | datetime.datetime]:
        return self.get(variable_name)

    def get(self, variable_name: str) -> list[float | datetime.datetime]:
        """Return the data collection related to one variable.

        :param variable_name: variable file_name
        :type variable_name: str
        :return: list of float or str values corresponding to common dates for the specified variable
        :rtype: list[float or str]
        """
        if variable_name == 'stringdate':
            return self._stringdates
        elif variable_name == 'datetime':
            return self._datetimes
        elif variable_name == 'epochtimems':
            return self._epochtimems
        elif variable_name in self._variable_data:
            return self._variable_data[variable_name]
        else:
            print(self)
            raise ValueError('Unknown variable: %s' % variable_name)

    def absolute_humidity_kg_per_kg(self) -> list[float]:
        Rs_J_per_kg_K = 287.06
        temperatures_deg: list[float] = self.get('temperature')
        relative_humidities_percent: list[float] = self.get('humidity')
        atmospheric_pressures_hPa: list[float] = self.get('pressure')
        _absolute_humidities_kg_per_kg: list[float] = list()
        for k in range(len(temperatures_deg)):
            density_kg_per_m3 = (atmospheric_pressures_hPa[k]*100 - 2.30617*relative_humidities_percent[k]*exp(17.5043*temperatures_deg[k]/(241.2+temperatures_deg[k])))/Rs_J_per_kg_K/(temperatures_deg[k] + 273.15)
            _absolute_humidities_kg_per_kg.append(absolute_humidity_kg_per_m3(temperatures_deg[k], relative_humidities_percent[k])/density_kg_per_m3)
        return _absolute_humidities_kg_per_kg

    def day_degrees(self, temperature_reference=18, heat=True):
        """Compute heating or cooling day degrees and print in terminal the sum of day degrees per month.

        :param temperature_reference: reference temperature (default is 18°C)
        :param heat: True if heating, False if cooling
        :return: list of day dates as string, list of day average, min and max outdoor temperature and day degrees per day
        :rtype: [list[str], list[float], list[float], list[float], list[float]]
        """
        datetimes: list[datetime] = self._datetimes
        stringdates: list[str] = self._stringdates
        temperatures: list[float] = self.get('temperature')
        dd_months: list[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        month_names: list[str] = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        day_stringdate_days = list()
        average_temperature_days = list()
        min_temperature_days = list()
        max_temperature_days = list()
        day_degrees = list()
        day_temperature = list()
        current_day = datetimes[0].day
        for k in range(len(datetimes)):
            if current_day == datetimes[k].day:
                day_temperature.append(temperatures[k])
            else:
                day_stringdate_days.append(stringdates[k-1].split(' ')[0])
                average_day_temperature: float = sum(day_temperature)/len(day_temperature)
                average_temperature_days.append(average_day_temperature)
                min_temperature_days.append(min(day_temperature))
                max_temperature_days.append(max(day_temperature))
                hdd = 0
                if heat:
                    if average_day_temperature < temperature_reference:
                        hdd = temperature_reference - average_day_temperature
                elif not heat:
                    if average_day_temperature > temperature_reference:
                        hdd = average_day_temperature - temperature_reference
                day_degrees.append(hdd)
                dd_months[datetimes[k].month-1] += hdd
                day_temperature = list()
            current_day = datetimes[k].day
        for i in range(len(dd_months)):
            print('day degrees', month_names[i], ': ', dd_months[i])
        return day_stringdate_days, average_temperature_days, min_temperature_days, max_temperature_days, day_degrees
    
    def data_datetimes_names(self) -> tuple[dict[str, list[float]], list[datetime], dict]:
        return self._variable_data, self._datetimes, self.variable_units

    def plot(self):
        TimeSeriesPlotter(self._variable_data, self._datetimes, self.variable_units)


if __name__ == '__main__':
    location: str = 'Cayenne'
    latitude_deg_north, longitude_deg_east = 4.924435336591809, -52.31276008988111
    weather_json_reader = WeatherJsonReader(location, latitude_north_deg=latitude_deg_north, longitude_east_deg=longitude_deg_east)
    site_weather_data: SiteWeatherData = weather_json_reader.site_weather_data
    print(site_weather_data)
    excerpt_site_weather_data: SiteWeatherData = site_weather_data.excerpt('1/1/2023', '31/12/2023')
    print(excerpt_site_weather_data)

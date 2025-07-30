"""
This code has been written by stephane.ploix@grenoble-inp.fr
It is protected under GNU General Public License v3.0
"""

import datetime
from typing import Any, Literal


class SignalCapper:
    """
    This class is a setpoint generator. It first generates a constant setpoint and proposes different
    methods to intersect with the original signal. The value None means no setpoint i.e. control
    is off.
    """

    def __init__(self, datetimes: list[datetime.datetime], base_values: float | list[float]):
        """
        Initialize the setpoint generator.

        :param reference_setpoint: the constant maximum setpoint value
        :type reference_setpoint: float
        :param datetimes: the list of dates (hours) corresponding to samples (that should be identical to
        to a Data object for integration)
        :type datetimes: list[datetime]
        """
        self.datetimes: list[datetime.datetime] = datetimes
        if type(base_values) is float:
            self.base_value: float = base_values
            self._values: list[float] = [base_values for _ in range(len(datetimes))]
        else:
            self._values = base_values

    def __call__(self) -> list[float]:
        """
        Return the setpoint values

        :return: setpoint values
        :rtype: list[float]
        """
        return self._values

    def _min(self, values: list[float]) -> list[float]:
        """
        Internal method used to intersect (take the minimum of the current setpoints and the provided ones)
        another list of setpoints

        :param setpoints: setpoints that will be compared to the current setpoint values: the minimum is
        computed for each sample and replace the current setpoint value. None is the minimum of all the possible values
        :type setpoints: list[float]
        """
        for i in range(len(self.datetimes)):
            if values[i] is not None:
                self._values[i] = min(self._values[i], values[i])

    def subtract(self, values: list[float]) -> None:
        for i in range(len(self.datetimes)):
            self._values[i] = self._values[i] - values[i]

    def add(self, values: list[float]) -> None:
        for i in range(len(self.datetimes)):
            self._values[i] = self._values[i] + values[i]

    def multiply(self, values: list[float]) -> None:
        for i in range(len(self.datetimes)):
            self._values[i] = self._values[i] * values[i]

    def period(self, period_start: tuple[int, int] = (15, 3), period_end: tuple[int, int] = (15, 10), in_between: bool = True) -> None:
        """
        Generate setpoints corresponding to seasonal start and stop of the HVAC system for instance.

        :param summer_period_start: starting date for the summer period (signal starts to be off), defaults to '15/03'
        :type summer_period_start: str, optional
        :param summer_period_end: ending date for the summer period (end of the off values), defaults to '15/10'
        :type summer_period_end: str, optional
        """
        values = list()
        for _datetime in self.datetimes:
            start_day, end_day = period_start[0], period_end[0]
            start_month, end_month = period_start[1], period_end[1]

            in_period = None
            if start_month < _datetime.month < end_month:
                in_period: bool = True
            elif (start_month == _datetime.month and _datetime.day >= start_day) and (end_month == _datetime.month and _datetime.day < end_day):
                in_period = True
            else:
                in_period = False
            if in_period:
                if in_between:
                    values.append(0)
                else:
                    values.append(None)
            else:
                if in_between:
                    values.append(None)
                else:
                    values.append(0)
        self._min(values)

    def daily(self, weekdays: list[int], value: float, hour_triggers: list[int], initial_on_state: bool = True):
        """
        Generate a setpoint corresponding to daily hours for selected days of the week.

        :param weekdays: list of the days of the week (0: Monday,... 6: Sunday) concerned by the setpoints
        :type weekdays: list[int]
        :param low_setpoint: low setpoint values used for computing the intersection with the current signal
        :type low_setpoint: float
        :param triggers: hours where the signal will switch from reference setpoint value to the low setpoint
        value and conversely, defaults to list[int]
        :type triggers: list[int], optional
        :param initial_on_state: initial setpoint value is low setpoint if False and reference setpoint value if True, defaults to False
        :type initial_on_state: bool, optional

        """
        current_state: bool = initial_on_state
        hour_triggers: list[int] = sorted(hour_triggers)
        on_triggers: dict[int, bool] = dict()
        for trigger in hour_triggers:
            on_triggers[trigger] = not current_state
            current_state = not current_state

        if type(weekdays) is int:
            weekdays: list[int] = [weekdays]
        setpoints: list[float] = list()
        profile: list[float] = list()
        on_state: bool = False
        for trigger_index in range(hour_triggers[0]):
            profile.append(self.base_value if not hour_triggers[0] else value)
        for trigger_index in on_triggers:
            while len(profile) < trigger_index:
                if on_state:
                    profile.append(self.base_value)
                else:
                    profile.append(value)
            on_state = on_triggers[trigger_index]
        for _ in range(trigger_index, 24):
            profile.append(self.base_value if on_triggers[trigger_index] else value)

        for _datetime in self.datetimes:
            if _datetime.weekday() in weekdays:
                setpoints.append(profile[_datetime.hour])
            else:
                setpoints.append(None)
        self._min(setpoints)

    def long_absence(self, number_of_days: int, presence: list[float]):
        """
        Detect long absences for setting the setpoints to 0.

        :param long_absence_setpoint: setpoint value in case of long absence detected
        :type long_absence_setpoint: float
        :param number_of_days: number of days over which a long absence is detected
        :type number_of_days: int
        :param presence: list of hours with presence (>0) and absence (=0)
        :type presence: list[float]
        """
        long_absence_start: int = None  # starting index for long absence
        long_absence_counter: int = 0
        values: list = list()
        for i in range(len(self.datetimes)):
            if presence[i] > 0:  # presence
                if long_absence_start is not None:  # long absence detected and ongoing
                    if long_absence_start + long_absence_counter > number_of_days * 24:  # long absence detected but is over (presence detected)
                        for i in range(long_absence_start, long_absence_counter):  # add long absence.endswith() setpoints
                            values.append(None)  # long_absence_value
                    else:  # long absence has not been detected
                        for i in range(long_absence_start, long_absence_counter):
                            values.append(0)
                    values.append(0)
                long_absence_counter = 0  # reinitialize the long absence counter
            else:  # absence
                if long_absence_start is None:  # first absence detection
                    long_absence_counter = 1
                    long_absence_start = i
                else:  # new absence detection
                    long_absence_counter += 1
        for i in range(len(values), len(self.datetimes)):
            values.append(None)
        self._min(values)

    def capping(self, capping_values: float, threshold: float, thresholding_values: list[float] = None, opposite: bool = False):
        """
        Modify setpoint values on the occurrence of setpoint (window opening ratio for instance) values of an extra-signal passing a threshold.

        :param opening_setpoint: setpoint value to be used in case of the extra signal pass a threshold
        :type opening_setpoint: list[float]
        :param opening_threshold: threshold over which the opening threshold value will be applied.
        :type opening_threshold: float
        :param openings: extra-signal whose values will trigger the right setpoint
        :type openings: list[float]
        """
        values: list = list()
        if thresholding_values is None:
            thresholding_values: list[float] = capping_values
        for i in range(len(self.datetimes)):
            if not opposite:
                values.append(capping_values if thresholding_values[i] >= threshold else self.base_value)
            else:
                values.append(None if thresholding_values[i] >= threshold else capping_values)
        self._min(values)


class DaySignalMaker:

    def __init__(self, datetimes: list[datetime.datetime], night_value: float = 0, integer: bool = False, default_hour_values: tuple[float, float] = ()) -> None:
        self.integer: bool = integer
        self.night_value: float = night_value
        self.datetimes: list[datetimes.datetimes] = datetimes
        if len(default_hour_values) == 0:
            self.default_day_profile = [night_value for _ in range(len(datetimes))]
        else:
            self.default_day_profile: list[float] = self.__expand(default_hour_values)
        self.day_profiles: dict[int, list[float]] = dict()

    def add_day_of_week_profile(self, days_of_week: tuple[int], hour_values: tuple[float, float]) -> None:
        profile: list[float] = self.__expand(hour_values)
        for d in days_of_week:
            self.day_profiles[d] = profile

    def __expand(self, hour_value_marks: tuple[tuple[float, float]]) -> list[float]:
        if len(hour_value_marks) == 0:
            day_values: list[float] = [self.night_value for _ in range(len(self.datetimes))]
        else:
            day_values = list()
            hour_value_marks = list(hour_value_marks)
            hour_value_marks.sort(key=lambda mark: mark[0])
            if hour_value_marks[0][0] < 0:
                raise "Error: hour in day can't be negative"
            if hour_value_marks[-1][0] >= 24:
                raise "Error: hour in day can't be greater or equal to 24"
            if hour_value_marks[0][0] > 0:
                hour_value_marks.insert(0, (hour_value_marks[0][0], self.night_value))
                hour_value_marks.insert(0, (0, self.night_value))
                hour_value_marks.append((hour_value_marks[-1][0], self.night_value))
                hour_value_marks.append((24, self.night_value))
            i = 0
            for day_hour in range(24):
                while not (hour_value_marks[i][0] <= day_hour <= hour_value_marks[i+1][0]):
                    i += 1
                if hour_value_marks[i][0] == hour_value_marks[i+1][0]:
                    value = (hour_value_marks[i][0] + hour_value_marks[i+1][0])/2
                    if self.integer:
                        value = round(value)
                    day_values.append(value)
                else:
                    value: float = DaySignalMaker.__interpolate(day_hour, hour_value_marks[i][0], hour_value_marks[i+1][0], hour_value_marks[i][1], hour_value_marks[i+1][1])
                    if self.integer:
                        value = round(value)
                    day_values.append(value)
        return day_values

    @staticmethod
    def __interpolate(time: int, previous_time: int, next_time: int, previous_value: float, next_value: float) -> float:
        return previous_value + (next_value - previous_value) * (time - previous_time) / (next_time - previous_time)

    def __call__(self) -> list[int] | list[float]:
        """generate a uniform random sequence of integer of float values
        :return: the random sequence
        :rtype: list[int]|list[float]
        """
        _value_sequence = list()
        for dt in self.datetimes:
            day_of_week: int = dt.weekday()
            hour_in_day: int = dt.hour
            if day_of_week in self.day_profiles:
                _value_sequence.append(self.day_profiles[day_of_week][hour_in_day])
            else:
                _value_sequence.append(self.default_day_profile[hour_in_day])

        return _value_sequence


class Merger:

    def __init__(self, operator: callable, dominance: Literal["left", "right", "both"]) -> None:
        self.operator: callable = operator
        self.dominance:  Literal["left", "right", "both"] = dominance

    def __call__(self, signal1: list[float | None], signal2: list[float | None]) -> Any:
        if self.dominance[0] == "l":
            return self._left_dom(signal1, signal2, self.operator)
        elif self.dominance[0] == "r":
            return self._right_dom(signal1, signal2, self.operator)
        elif self.dominance[0] == "b":
            return self._both_dom(signal1, signal2, self.operator)
        elif self.dominance[0] == "n":
            return self._no_one_dom(signal1, signal2, self.operator)
        else:
            raise ValueError('Unknown merger')

    def _left_dom(self, signal1: list[float | None], signal2: list[float | None], operator: callable):
        signal = list()
        for i in range(len(signal1)):
            if signal1[i] is None:
                signal.append(None)
            else:
                if signal2[i] is None:
                    signal.append(signal1[i])
                else:
                    signal.append(operator(signal1[i], signal2[i]))
        return signal

    def _right_dom(self, signal1: list[float | None], signal2: list[float | None], operator: callable):
        signal = list()
        for i in range(len(signal1)):
            if signal2[i] is None:
                signal.append(None)
            else:
                if signal1[i] is None:
                    signal.append(signal2[i])
                else:
                    signal.append(operator(signal1[i], signal2[i]))
        return signal

    def _both_dom(self, signal1: list[float | None], signal2: list[float | None], operator: callable):
        signal = list()
        for i in range(len(signal1)):
            if signal1[i] is None or signal2[i] is None:
                signal.append(None)
            else:
                signal.append(operator(signal1[i], signal2[i]))
        return signal

    def _no_one_dom(self, signal1: list[float | None], signal2: list[float | None], operator: callable):
        signal = list()
        for i in range(len(signal1)):
            if signal1[i] is None and signal2[i] is None:
                signal.append(None)
            else:
                if signal1[i] is not None and signal2[i] is not None:
                    signal.append(operator(signal1[i], signal2[i]))
                elif signal1[i] is not None:
                    signal.append(signal1[i])
                elif signal2[i] is not None:
                    signal.append(signal2[i])
        return signal


class SignalGenerator:
    """
    This class is a setpoint generator. It first generates a constant setpoint and proposes different
    methods to intersect with the original signal. The value None means no setpoint i.e. control is off.
    """

    def __init__(self, datetimes: list[datetime.datetime], constant: None | float = 0):
        """
        Initialize the setpoint generator.


        :param datetimes: the list of dates (hours) corresponding to samples (that should be identical to
        to a Data object for integration)
        :type datetimes: list[datetime]
        """
        self.signal: list[float | None] = [constant for _ in range(len(datetimes))]
        self.datetimes: list[datetime.datetime] = datetimes

    def __call__(self, signal: list[float] = None) -> list[float]:
        """
        Return the setpoint values

        :return: setpoint values
        :rtype: list[float]
        """
        if signal is None:
            return self.signal
        elif type(signal) is int:
            return self.signal[signal]
        else:
            self.signal = signal

    @staticmethod
    def day_months_to_days(dm_str: str):  # format dd/mm
        day, month = tuple([int(v) for v in dm_str.split('/')])
        return day + month * 32

    def offset(self, value: float, merger: Merger = Merger(lambda x, y: x + y, dominance='l')) -> list[float]:
        signal: list[float] = [value for _ in range(len(self.datetimes))]
        self.signal = merger(self.signal, signal)
        return signal

    def seasonal(self, day_month_start: str, day_month_end: str, in_value: float = 1, out_value: float = None,  merger: Merger = Merger(max, dominance='r')) -> list[float | None]:
        """
        Generate setpoints corresponding to seasonal start and stop of the HVAC system for instance.

        :param summer_period_start: starting date for the summer period (signal starts to be off), defaults to '15/03'
        :type summer_period_start: str, optional
        :param summer_period_end: ending date for the summer period (end of the off values), defaults to '15/10'
        :type summer_period_end: str, optional
        """
        day_start: int = SignalGenerator.day_months_to_days(day_month_start)
        day_end: int = SignalGenerator.day_months_to_days(day_month_end)
        direct: bool = day_start <= day_end
        signal = list()
        for dt in self.datetimes:
            dt_day: int = dt.day + 32 * dt.month
            if direct and (day_start <= dt_day <= day_end) or not direct and (dt_day <= day_end or dt_day >= day_start):
                signal.append(in_value)
            else:
                signal.append(out_value)
        self.signal = merger(self.signal, signal)
        return signal

    def daily(self, weekdays: list[int], hour_setpoints: dict[int, float], merger: Merger = Merger(max, dominance='l')):
        if 0 not in hour_setpoints:
            raise ValueError("0 must appear in the trigger dictionary")
        previous_hour, previous_setpoint = None, None
        day_sequence = list()
        for hour in hour_setpoints:
            if previous_hour is None:
                previous_hour, previous_setpoint = hour, hour_setpoints[hour]
            elif hour < previous_hour:
                raise ValueError("Hours must be strictly increasing")
            else:
                for _ in range(previous_hour, hour):
                    day_sequence.append(previous_setpoint)
                previous_hour, previous_setpoint = hour, hour_setpoints[hour]
        for hour in range(previous_hour, 24):
            day_sequence.append(previous_setpoint)

        signal = list()
        for dt in self.datetimes:
            if dt.weekday() in weekdays:
                signal.append(day_sequence[dt.hour])
            else:
                signal.append(None)
        self.signal = merger(self.signal, signal)
        return signal

    def long_absence(self, high_setpoint: float, long_absence_setpoint: float, number_of_days: int, presence: list[float], merger: Merger = Merger(min, dominance='b')):
        """
        Detect long absences for setting the setpoints to off.

        :param long_absence_setpoint: setpoint value in case of long absence detected
        :type long_absence_setpoint: float
        :param number_of_days: number of days over which a long absence is detected
        :type number_of_days: int
        :param presence: list of hours with presence (>0) and absence (=0)
        :type presence: list[float]
        """
        long_absence_start = None  # starting index for long absence
        long_absence_counter: int = 0
        signal: list = list()
        for i in range(len(self.datetimes)):
            if presence[i] > 0:  # presence
                if long_absence_start is not None:  # long absence detected and ongoing
                    if long_absence_start + long_absence_counter > number_of_days * 24:  # long absence detected but is over (presence detected)
                        for i in range(long_absence_start, long_absence_counter):  # add long absence.endswith() setpoints
                            signal.append(long_absence_setpoint)
                    else:  # long absence has not been detected
                        for i in range(long_absence_start, long_absence_counter):
                            signal.append(high_setpoint)
                    signal.append(high_setpoint)
                long_absence_counter = 0  # reinitialize the long absence counter
            else:  # absence
                if long_absence_start is None:  # first absence detection
                    long_absence_counter = 1
                    long_absence_start = i
                else:  # new absence detection
                    long_absence_counter += 1
        for i in range(len(signal), len(self.datetimes)):
            signal.append(high_setpoint)
        self.signal = merger(self.signal, signal)
        return signal

    def combine(self, *signals: list[float | None], merger: Merger = Merger(lambda x, y: x + y, dominance='n')):
        for signal in signals:
            self.signal = merger(self.signal, signal)

    def cap(self, capped_value: float, threshold: float, capping_values: list[float] = None):
        if capping_values is None:
            capping_values = self.signal
        for i in range(len(self.datetimes)):
            if capping_values[i] > threshold:
                self.signal[i] = capped_value

    def cup(self, cupped_value: float, threshold: float, cupping_values: list[float] = None):
        if cupping_values is None:
            cupping_values = self.signal
        for i in range(len(self.datetimes)):
            if cupping_values[i] < threshold:
                self.signal[i] = cupped_value

    def amplify(self, alpha: float):
        for k in range(len(self.datetimes)):
            if self.signal[k] is not None:
                self.signal[k] = self.signal[k] * alpha

    def integerize(self, none_value: int = 0):
        for k in range(len(self.datetimes)):
            if self.signal[k] is None:
                self.signal[k] = none_value

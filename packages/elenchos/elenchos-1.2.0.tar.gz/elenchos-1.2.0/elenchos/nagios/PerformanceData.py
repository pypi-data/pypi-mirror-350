from typing import Optional, Union

from elenchos.nagios.IncludeInDescription import IncludeInDescription
from elenchos.nagios.NagiosStatus import NagiosStatus


class PerformanceData:
    """
    Class for checking performance data against warning and critical levels and generating performance data string.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 name: str,
                 *,
                 value: Union[int, float, None] = None,
                 value_in_description: Optional[str] = None,
                 include_in_description: IncludeInDescription = IncludeInDescription.ALWAYS,
                 warning: Union[int, float, None] = None,
                 critical: Union[int, float, None] = None,
                 min_value: Union[int, float, None] = None,
                 max_value: Union[int, float, None] = None,
                 unit: Optional[str] = None,
                 type_check: str = 'asc'):
        """
        Object constructor.

        :param name: The name of the performance data.
        :param value: The value of the performance data.
        :param value_in_description: The representation of the value in the description.
        :param include_in_description: How to include the performance data in the description.
        :param warning: The warning level.
        :param critical: The critical level.
        :param min_value: The minium value to visualize.
        :param max_value: The maximum value to visualize.
        :param unit: The unit of the performance data.
        :param type_check: Either, 'asc' or 'desc', method to compare the performance data with warning and
                           critical levels.
        """
        if unit not in [None, 's', 'us', 'ms', '%', 'B', 'KB', 'TB', 'GB', 'c']:
            raise ValueError(unit)

        self.__name: str = name.strip()
        """
        The name of the performance data.
        """

        self.__value: Union[int, float, None] = PerformanceData.__convert_value(value)
        """
        The value of the performance data.
        """

        self.__value_in_description: Optional[str] = value_in_description
        """
        The representation of the value in the description.
        """

        self.__include_in_description: IncludeInDescription = include_in_description
        """
        How to include the performance data into the description.
        """

        self.__warning: Union[int, float, None] = PerformanceData.__convert_value(warning)
        """
        The warning level.
        """

        self.__critical: Union[int, float, None] = PerformanceData.__convert_value(critical)
        """
        The critical level.
        """

        self.__min: Union[int, float, None] = PerformanceData.__convert_value(min_value)
        """
        The minium value to visualise.
        """

        self.__max: Union[int, float, None] = PerformanceData.__convert_value(max_value)
        """
        The maximum value to visualise.
        """

        self.__unit: Optional[str] = unit
        """
        The unit of the performance data.
        """

        self.__type_check: str = type_check
        """
        Either, 'asc' or 'desc', method to compare the performance data with warning and critical levels.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __convert_value(value: Union[int, float, str, None]) -> Union[int, float, None]:
        """
        Converts a value, either an int, float, string, or None, to an int, float, or None.
        """
        if value in [None, '']:
            return None

        if float(value) == int(value):
            return int(value)

        return float(value)

    # ------------------------------------------------------------------------------------------------------------------
    def check(self) -> NagiosStatus:
        """
        Checks the performance data by comparing with warning and critical values and returns the appropriate status.
        """
        if self.__value is None and (self.__warning is not None or self.__critical is not None):
            return NagiosStatus.UNKNOWN

        if self.__type_check == 'asc':
            if self.__critical is not None and self.__critical <= self.__value:
                return NagiosStatus.CRITICAL

            if self.__warning is not None and self.__warning <= self.__value:
                return NagiosStatus.WARNING

            return NagiosStatus.OK

        if self.__type_check == 'desc':
            if self.__critical is not None and self.__critical >= self.__value:
                return NagiosStatus.CRITICAL

            if self.__warning is not None and self.__warning >= self.__value:
                return NagiosStatus.WARNING

            return NagiosStatus.OK

        raise ValueError('{}'.format(self.__type_check))

    # ------------------------------------------------------------------------------------------------------------------
    def header(self) -> str:
        """
        Returns the summary of the performance data.
        """
        if self.__value_in_description is not None:
            value = ' '.join(self.__value_in_description.strip().split())
            return "{} = {}".format(self.__name, value)

        return "{} = {}{}".format(self.__name, self.__value, self.__unit if self.__unit is not None else '')

    # ------------------------------------------------------------------------------------------------------------------
    def include_in_description(self) -> bool:
        """
        Returns whether the performance data must be included in the description.
        """
        if self.__include_in_description == IncludeInDescription.ALWAYS:
            return True

        status = self.check()

        if self.__include_in_description == IncludeInDescription.WARNING:
            return status in [NagiosStatus.WARNING, NagiosStatus.CRITICAL]

        if self.__include_in_description == IncludeInDescription.CRITICAL:
            return status == NagiosStatus.CRITICAL

        return False

    # ------------------------------------------------------------------------------------------------------------------
    def performance(self) -> str:
        """
        Returns the performance data in a structured format.
        """
        return "{}={}{};{};{};{};{}".format(self.__name.replace(' ', '_'),
                                            self.__value if self.__value is not None else '',
                                            self.__unit if self.__unit is not None else '',
                                            self.__warning if self.__warning is not None else '',
                                            self.__critical if self.__critical is not None else '',
                                            self.__min if self.__min is not None else '',
                                            self.__max if self.__max is not None else '')

# ----------------------------------------------------------------------------------------------------------------------

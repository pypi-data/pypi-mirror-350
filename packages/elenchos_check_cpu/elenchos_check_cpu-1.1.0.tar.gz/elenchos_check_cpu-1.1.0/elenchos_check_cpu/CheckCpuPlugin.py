import platform
from pathlib import Path
from time import sleep
from typing import Dict, Tuple

from elenchos.nagios.IncludeInDescription import IncludeInDescription
from elenchos.nagios.NagiosPlugin import NagiosPlugin
from elenchos.nagios.NagiosStatus import NagiosStatus
from elenchos.nagios.PerformanceData import PerformanceData


class CheckCpuPlugin(NagiosPlugin):
    """
    Élenchos plugin for CPU usage.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, interval: int, warning: float | None, critical: float | None):
        """
        Object constructor.
        """
        NagiosPlugin.__init__(self, 'CPU')

        self.__interval = interval
        """
        The interval between the two CPU statistics gatherings in seconds.
        """

        self.__warning: float | None = warning
        """
        The warning level for CPU user.
        """

        self.__critical: float | None = critical
        """
        The critical level for CPU user.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __self_check_linux_get_stats() -> Tuple[int, Dict[str, int]]:
        """
        Returns the CPU statistics on a Linux system.
        """
        cpus = 0
        stats: Dict[str, int] = {}

        text = Path('/proc/stat').read_text()
        lines = text.splitlines()
        for line in lines:
            words = line.split()
            if words[0] == 'cpu':
                stats['user'] = int(words[1])
                stats['nice'] = int(words[2])
                stats['system'] = int(words[3])
                stats['idle'] = int(words[4])
                stats['iowait'] = int(words[5]) if len(words) > 5 else 0
                stats['irq'] = int(words[6]) if len(words) > 6 else 0
                stats['softirq'] = int(words[7]) if len(words) > 7 else 0
                stats['guest'] = int(words[8]) if len(words) > 8 else 0
                stats['guestp'] = int(words[9]) if len(words) > 9 else 0
                stats['total'] = stats['user'] + \
                                 stats['nice'] + \
                                 stats['system'] + \
                                 stats['idle'] + \
                                 stats['iowait'] + \
                                 stats['irq'] + \
                                 stats['softirq'] + \
                                 stats['guest'] + \
                                 stats['guestp']

            if words[0].startswith('cpu') and len(words[0]) >= 4:
                cpus += 1

        return cpus, stats

    # ------------------------------------------------------------------------------------------------------------------
    def __self_check_linux(self) -> None:
        """
        Checks the memory on a Linux system.
        """
        cpus, stats1 = self.__self_check_linux_get_stats()
        sleep(self.__interval)
        _, stats2 = self.__self_check_linux_get_stats()

        stats_diff = {}
        for key in stats1.keys():
            stats_diff[key] = stats2[key] - stats1[key]

        stats = {}
        for key in stats_diff.keys():
            stats[key] = 100.0 * stats_diff[key] / stats_diff['total']

        self._add_performance_data(PerformanceData(name='CPUs', value=cpus))

        for key in stats.keys():
            if key != 'total':
                if key in ('user', 'nice', 'system', 'idle', 'iowait'):
                    include_in_description = IncludeInDescription.ALWAYS
                else:
                    include_in_description = IncludeInDescription.NEVER
                if key == 'user':
                    warning = self.__warning
                    critical = self.__critical
                else:
                    warning = None
                    critical = None
                self._add_performance_data(PerformanceData(name=key,
                                                           value=round(stats[key], 6),
                                                           include_in_description=include_in_description,
                                                           warning=warning,
                                                           critical=critical,
                                                           value_in_description=f'{stats[key]:.1f}%',
                                                           unit='%'))

    # ------------------------------------------------------------------------------------------------------------------
    def _self_check(self) -> NagiosStatus:
        """
        Checks the CPU usage.
        """
        system = platform.system()
        if system == 'Linux':
            self.__self_check_linux()

            return NagiosStatus.OK

        self.message = f'Unknown operating system {system}.'

        return NagiosStatus.UNKNOWN

# ----------------------------------------------------------------------------------------------------------------------

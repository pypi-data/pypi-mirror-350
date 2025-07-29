import time
from pathlib import Path
from typing import Dict

from elenchos.nagios.IncludeInDescription import IncludeInDescription
from elenchos.nagios.NagiosPlugin import NagiosPlugin
from elenchos.nagios.NagiosStatus import NagiosStatus
from elenchos.nagios.PerformanceData import PerformanceData

from elenchos_check_mymaria_replication.DataLayer import DataLayer


class MyMariaReplicationPlugin(NagiosPlugin):
    """
    Élenchos plugin for checking the replication of a MySQL or MariaDB instance.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, params: Dict):
        """
        Object constructor.
        """
        NagiosPlugin.__init__(self, params['nagios']['name'])

        self.__params: Dict = params
        """
        The connection parameters.
        """

        self.__dl: DataLayer = DataLayer(self.__params['database'])
        """
        The connection between Python and the MySQL or MariaDB instance.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def __check_exec_master_log_pos(self, slave_status: Dict) -> None:
        """
        Adds performance data about execute master log position.
        """
        self._add_performance_data(PerformanceData('Exec_Master_Log_Pos',
                                                   value=slave_status['Exec_Master_Log_Pos'],
                                                   include_in_description=IncludeInDescription.NEVER))

    # ------------------------------------------------------------------------------------------------------------------
    def __check_lag(self, last_heartbeat: int) -> None:
        """
        Checks whether there is no last SQL error and adds performance data.
        """
        now = int(time.time())
        lag = now - last_heartbeat

        if lag <= self.__params['nagios']['max_lag']:
            Path(self.__params['nagios']['timestamp_path']).write_text(str(now))

        try:
            timestamp = int(Path(self.__params['nagios']['timestamp_path']).read_text().strip())
            value = now - timestamp
        except FileNotFoundError:
            Path(self.__params['nagios']['timestamp_path']).write_text(str(now))
            value = 0

        self._add_performance_data(PerformanceData('Last Lag Compliance',
                                                   value=value,
                                                   include_in_description=IncludeInDescription.WARNING,
                                                   warning=self.__params['nagios']['warning'],
                                                   critical=self.__params['nagios']['critical'],
                                                   type_check='asc',
                                                   unit='s'))

    # ------------------------------------------------------------------------------------------------------------------
    def __check_last_heartbeat(self, last_heartbeat: int) -> None:
        """
        Checks whether there is no last SQL error and adds performance data.
        """
        value = int(time.time()) - last_heartbeat

        self._add_performance_data(PerformanceData('Last Heartbeat', value=value, type_check='asc', unit='s'))

    # ------------------------------------------------------------------------------------------------------------------
    def __check_last_sql_error(self, slave_status: Dict) -> None:
        """
        Checks whether there is no last SQL error and adds performance data.
        """
        value = 0 if slave_status['Last_SQL_Error'] in [None, ''] else 1

        self._add_performance_data(PerformanceData('Last SQL Error',
                                                   value=value,
                                                   value_in_description=slave_status['Last_SQL_Error'],
                                                   include_in_description=IncludeInDescription.WARNING,
                                                   critical=1,
                                                   type_check='asc'))

    # ------------------------------------------------------------------------------------------------------------------
    def __check_seconds_behind_master(self, slave_status: Dict) -> None:
        """
        Adds performance data about seconds behind master.
        """
        self._add_performance_data(PerformanceData('Seconds Behind Master',
                                                   value=slave_status['Seconds_Behind_Master'],
                                                   include_in_description=IncludeInDescription.NEVER,
                                                   unit='s'))

    # ------------------------------------------------------------------------------------------------------------------
    def __check_slave_io(self, slave_status: Dict) -> None:
        """
        Checks whether IO thread is running and adds performance data.
        """
        value = 1 if slave_status['Slave_IO_Running'] == 'Yes' else 0

        self._add_performance_data(PerformanceData('Slave IO Running',
                                                   value=value,
                                                   value_in_description=slave_status['Slave_IO_Running'],
                                                   include_in_description=IncludeInDescription.WARNING,
                                                   critical=0,
                                                   type_check='desc'))

    # ------------------------------------------------------------------------------------------------------------------
    def __check_slave_sql_running(self, slave_status: Dict) -> None:
        """
        Adds performance data about SQL thread is running.
        """
        value = 1 if slave_status['Slave_SQL_Running'] == 'Yes' else 0

        self._add_performance_data(PerformanceData('Slave SQL Running',
                                                   value=value,
                                                   include_in_description=IncludeInDescription.NEVER))

    # ------------------------------------------------------------------------------------------------------------------
    def _self_check(self) -> NagiosStatus:
        """
        Checks the replication status.
        """
        slave_status = self.__dl.slave_status()
        last_heartbeat = self.__dl.last_heartbeat()

        self.__check_exec_master_log_pos(slave_status)
        self.__check_lag(last_heartbeat)
        self.__check_last_heartbeat(last_heartbeat)
        self.__check_last_sql_error(slave_status)
        self.__check_seconds_behind_master(slave_status)
        self.__check_slave_io(slave_status)
        self.__check_slave_sql_running(slave_status)

        return NagiosStatus.OK

# ----------------------------------------------------------------------------------------------------------------------

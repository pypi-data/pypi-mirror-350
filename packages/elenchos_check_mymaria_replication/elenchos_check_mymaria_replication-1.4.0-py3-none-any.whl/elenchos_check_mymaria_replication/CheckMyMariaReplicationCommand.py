import os
from configparser import ConfigParser
from typing import Dict, Optional

from cleo.helpers import argument
from elenchos.command.CheckCommand import CheckCommand

from elenchos_check_mymaria_replication.MyMariaReplicationPlugin import MyMariaReplicationPlugin


class CheckMyMariaReplicationCommand(CheckCommand):
    """
    Élenchos command for checking the replication of a MySQL or MariaDB instance.
    """
    name = 'check:mariadb-replication'
    description = 'Replication test of a MySQL or MariaDB database instance'
    arguments = [argument('config.cfg', description='The configuration file')]

    # ------------------------------------------------------------------------------------------------------------------
    def __read_configuration_file(self) -> Dict:
        """
        Reads connections parameters from the configuration file.
        """
        config_filename = self.argument('config.cfg')
        config = ConfigParser()
        config.read(config_filename)

        if 'database' in config and 'supplement' in config['database']:
            path = os.path.join(os.path.dirname(config_filename), config.get('database', 'supplement'))
            config_supplement = ConfigParser()
            config_supplement.read(path)

            if 'database' in config_supplement:
                options = config_supplement.options('database')
                for option in options:
                    config['database'][option] = config_supplement['database'][option]

        params = {
            'nagios':
                {
                    'name':           self.__get_option_str(config, 'nagios', 'name'),
                    'max_lag':        self.__get_option_int(config, 'nagios', 'max_lag'),
                    'warning':        self.__get_option_int(config, 'nagios', 'warning'),
                    'critical':       self.__get_option_int(config, 'nagios', 'critical'),
                    'timestamp_path': os.path.join(os.path.dirname(config_filename),
                                                   self.__get_option_str(config,
                                                                         'nagios',
                                                                         'timestamp_path')),
                },
            'database':
                {
                    'host':      self.__get_option_str(config, 'database', 'host', fallback='localhost'),
                    'user':      self.__get_option_str(config, 'database', 'user'),
                    'password':  self.__get_option_str(config, 'database', 'password'),
                    'database':  self.__get_option_str(config, 'database', 'database'),
                    'port':      self.__get_option_int(config, 'database', 'port', fallback=3306),
                    'charset':   self.__get_option_str(config, 'database', 'charset', fallback='utf8mb4'),
                    'collation': self.__get_option_str(config, 'database', 'collation', fallback='utf8mb4_general_ci')
                }}

        return params

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __get_option_str(config: ConfigParser,
                         section: str,
                         option: str,
                         fallback: Optional[str] = None) -> str:
        """
        Reads an option for a configuration file.

        :param config: The main config file.
        :param section: The name of the section op the option.
        :param option: The name of the option.
        :param fallback: The fallback value of the option if it is not set in either configuration files.

        :raise KeyError:
        """
        value = config.get(section, option, fallback=fallback)

        if fallback is None and value is None:
            raise KeyError("Option '{0!s}' is not found in section '{1!s}'.".format(option, section))

        return value

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __get_option_int(config: ConfigParser,
                         section: str,
                         option: str,
                         fallback: Optional[int] = None) -> int:
        """
        Reads an option for a configuration file.

        :param config: The main config file.
        :param section: The name of the section op the option.
        :param option: The name of the option.
        :param fallback: The fallback value of the option if it is not set in either configuration files.

        :raise KeyError:
        """
        value = config.getint(section, option, fallback=fallback)

        if fallback is None and value is None:
            raise KeyError("Option '{0!s}' is not found in section '{1!s}'.".format(option, section))

        return value

    # ------------------------------------------------------------------------------------------------------------------
    def _handle(self) -> int:
        """
        Executes this command.
        """
        plugin = MyMariaReplicationPlugin(self.__read_configuration_file())

        return plugin.check().value

# ----------------------------------------------------------------------------------------------------------------------

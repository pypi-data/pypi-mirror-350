from typing import Dict, Union

from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursorBufferedDict


class DataLayer:
    """
    Class for connecting to a MySQL instance and executing SQL statements.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, params: Dict[str, Union[str, int]]):
        """
        Object constructor.
        """

        self._connection: MySQLConnection = MySQLConnection(**params)
        """
        The connection between Python and the MySQL instance.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def __del__(self):
        """
        Object destructor.
        """
        self._connection.close()

    # ------------------------------------------------------------------------------------------------------------------
    def slave_status(self) -> Dict:
        """
        Returns the slave status.
        """
        cursor = MySQLCursorBufferedDict(self._connection)
        cursor.execute('show slave status')
        ret = cursor.fetchall()
        cursor.close()

        return ret[0]

    # ------------------------------------------------------------------------------------------------------------------
    def last_heartbeat(self) -> int:
        """
        Returns the timestamp of the last heartbeat.
        """
        cursor = MySQLCursorBufferedDict(self._connection)
        cursor.execute('select unix_timestamp(heartbeat) as heartbeat from heartbeat')
        ret = cursor.fetchall()
        cursor.close()

        return ret[0]['heartbeat']

# ----------------------------------------------------------------------------------------------------------------------

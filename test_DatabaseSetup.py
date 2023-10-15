'''
See lines 22, 23, and 24. Please replace with your own MySQL details when testing
'''

import unittest
from unittest.mock import patch, Mock
from DatabaseSetup import DatabaseSetup, DbConnectionError


class TestDatabaseSetup(unittest.TestCase):

    # test to check connection to sql
    @patch('mysql.connector.connect')
    def test_insert_into_database(self, mock_connect):
        db_setup = DatabaseSetup()
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_db_connection = mock_connect.return_value

        db_setup.insert_into_database('test_db', 'Test Affirmation')

        mock_connect.assert_called_once_with(
            host='localhost',       # if you test, replace with your details from config file
            user='root',            # if you test, replace with your details from config file
            password='090781',      # if you test, replace with your details from config file
            auth_plugin='mysql_native_password',
            database='test_db'
        )
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO favourited (affirmation) VALUES (%s)",
            ('Test Affirmation',)
        )
        mock_db_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db_connection.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
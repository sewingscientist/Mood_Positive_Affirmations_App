import mysql.connector
from config import USER, PASSWORD, HOST


class DbConnectionError(Exception):
    pass


class DatabaseSetup:
    # Connects to mySQL
    def _connect_to_db(self, db_name):
        cnx = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            auth_plugin='mysql_native_password',
            database=db_name
        )
        return cnx

    # Inserts affirmation into the MySQL table
    def insert_into_database(self, db_name, affirmation_text):
        try:
            db_connection = self._connect_to_db(db_name)
            cursor = db_connection.cursor()

            insert_query = "INSERT INTO favourited (affirmation) VALUES (%s)"
            cursor.execute(insert_query, (affirmation_text,))
            db_connection.commit()
            cursor.close()

        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            db_connection.rollback()

        finally:
            if db_connection:
                db_connection.close()

    # Pulls all affirmations out of the table when my affirmations <3 button clicked
    def view_all_affirmations(self, db_name):
        try:
            db_connection = self._connect_to_db(db_name)
            cur = db_connection.cursor() # cursor needs to be used any time we have queries in sql

            query = """SELECT affirmation FROM favourited"""
            cur.execute(query)
            affirmations = cur.fetchall()  # this is a list with db records where each record is a tuple

            cur.close()

            return [affirmation[0] for affirmation in affirmations]

        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")

        finally:
            if db_connection:
                db_connection.close()



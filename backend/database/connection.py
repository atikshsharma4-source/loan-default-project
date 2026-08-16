import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


class DatabaseConnection:

    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        self.connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            ssl_disabled=False,
            connection_timeout=10,
            autocommit=False
        )

        print("MySQL connected successfully!")

    def ensure_connection(self):

        try:
            if self.connection is None:
                self.connect()

            elif not self.connection.is_connected():
                print("MySQL connection lost. Reconnecting...")
                self.connect()

            else:
                # Check whether the connection is actually usable
                self.connection.ping(
                    reconnect=True,
                    attempts=3,
                    delay=2
                )

        except mysql.connector.Error:
            print("MySQL reconnecting...")
            self.connect()

    def cursor(self, *args, **kwargs):

        self.ensure_connection()

        return self.connection.cursor(
            *args,
            **kwargs
        )

    def commit(self):

        self.ensure_connection()

        self.connection.commit()

    def rollback(self):

        self.ensure_connection()

        self.connection.rollback()


connection = DatabaseConnection()
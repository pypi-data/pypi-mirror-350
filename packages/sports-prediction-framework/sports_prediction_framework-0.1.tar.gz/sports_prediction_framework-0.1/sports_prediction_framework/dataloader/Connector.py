import paramiko
from sshtunnel import SSHTunnelForwarder
import psycopg2
from dotenv import load_dotenv, dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path=os.path.join(os.getcwd(), ".env")

class Connector:
    """
    Manages connection to a PostgreSQL database, optionally through an SSH tunnel.
    """

    def __init__(self):
        """
        Initializes the Connector by loading configuration values from a .env file.
        """
        self.config = dotenv_values(dotenv_path)

    def connect_to_db(self):
        """
        Establishes a direct connection to the PostgreSQL database using SQLAlchemy.
        Creates an engine and a session for interacting with the database.
        """
        try:
            self.eng = create_engine(f'postgresql+psycopg2://{self.config["DB_USER"]}:{self.config["DB_PASSWORD"]}@127.0.0.1:5433/{self.config["DB_NAME"]}')
            session_func = sessionmaker(bind=self.eng)
            self.session = session_func()
            print("Connected to database")
        except Exception as e:
            print("Connection to database failed.")

    def connect_to_db_via_ssh(self):
        """
        Establishes an SSH tunnel to the remote host and connects to the database through the tunnel.
        Starts the tunnel and calls `connect_to_db()` for the actual database connection.
        """
        try:
            # Establish SSH tunnel
            self.tunnel = SSHTunnelForwarder(
                (self.config['SSH_HOST'], 22),  # SSH server and port
                ssh_username=self.config['SSH_USER'],
                ssh_pkey=self.config['SSH_KEY_PATH'],
                remote_bind_address=(self.config['DB_HOST'], int(self.config['DB_PORT'])),  # Remote database address
                local_bind_address=('127.0.0.1', 5433)  # Local forwarding
            )

            self.tunnel.start()

            self.connect_to_db()
        except Exception as e:
            pass

    def close(self):
        """
        Closes the SSH tunnel (if open), the database session, and disposes of the SQLAlchemy engine.
        """
        self.tunnel.stop()
        self.session.close()
        self.eng.dispose()

    def get_engine(self):
        """
        Returns the SQLAlchemy engine object.

        Returns:
            sqlalchemy.engine.Engine: The SQLAlchemy engine connected to the database.
        """
        return self.eng


import argparse
import logging.config
import sqlite3
import typing

import pandas as pd
import sqlalchemy.orm
from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)

Base: typing.Any = declarative_base()


class User_info(Base):
    """Creates a data model for the database to be set up for capturing body measurement info.
    """

    __tablename__ = 'user_info'

    id = Column(Integer, primary_key=True)
    age = Column(Integer, unique=False,
                 nullable=False)
    weight = Column(Float, unique=False,
                    nullable=False)
    height = Column(Float, unique=False,
                    nullable=False)
    neck = Column(Float, unique=False,
                  nullable=False)
    chest = Column(Float, unique=False,
                   nullable=False)
    abdomen = Column(Float, unique=False,
                     nullable=False)
    hip = Column(Float, unique=False,
                 nullable=False)
    thigh = Column(Float, unique=False,
                   nullable=False)
    knee = Column(Float, unique=False,
                  nullable=False)
    ankle = Column(Float, unique=False,
                   nullable=False)
    biceps = Column(Float, unique=False,
                    nullable=False)
    forearm = Column(Float, unique=False,
                     nullable=False)
    wrist = Column(Float, unique=False,
                   nullable=False)

    def __repr__(self):
        return "<User No. %i>" % self.index


class UserManager:
    """Creates a SQLAlchemy connection to the tracks table.

    Args:
        app (:obj:`flask.app.Flask`): Flask app object for when connecting from
            within a Flask app. Optional.
        engine_string (str): SQLAlchemy engine string specifying which database
            to write to. Follows the format
    """

    def __init__(self, engine_string: typing.Optional[str] = None):
        engine = sqlalchemy.create_engine(engine_string)
        session_maker = sqlalchemy.orm.sessionmaker(bind=engine)
        self.session = session_maker()

    def close(self) -> None:
        """Closes SQLAlchemy session

        Returns: None

        """
        self.session.close()

    def add_user(self, age: int, weight: float, height: float, neck: float, chest: float, abdomen: float,
                  hip: float, thigh: float, knee: float, ankle: float, biceps: float, forearm: float,
                  wrist: float) -> None:
        """Seeds an existing database with additional songs.

        Args:
            title (str): Title of song to add to database
            artist (str): Artist of song to add to database
            album (str): Album of song to add to database

        Returns:
            None
        """

        session = self.session
        user = User_info(age=age, weight=weight, height=height, neck=neck, chest=chest,
                         abdomen=abdomen, hip=hip, thigh=thigh, knee=knee, ankle=ankle,
                         biceps=biceps, forearm=forearm, wrist=wrist
                         )
        session.add(user)
        session.commit()
        logger.info("User %s is added to database", id)


def create_db(engine_string: str) -> None:
    """Create database with Tracks() data model from provided engine string.

    Args:
        engine_string (str): SQLAlchemy engine string specifying which database
            to write to

    Returns: None

    """
    engine = sqlalchemy.create_engine(engine_string)

    Base.metadata.create_all(engine)
    logger.info("Database created.")


def add_user(self, input_path) -> None:
    """Parse command line arguments and add song to database.

    Args:
        args (:obj:`argparse.Namespace`): object containing the following
            fields:

            - args.title (str): Title of song to add to database
            - args.artist (str): Artist of song to add to database
            - args.album (str): Album of song to add to database
            - args.engine_string (str): SQLAlchemy engine string specifying
              which database to write to

    Returns:
        None
    """
    session = self.session
    data_list = pd.read_csv(input_path).to_dict(orient='records')

    persist_list = []
    for data in data_list:
        persist_list.append(User_info(**data))

    try:
        session.add_all(persist_list)
        session.commit()
    except sqlalchemy.exc.OperationalError:
        my_message = ('You might have connection error. Have you configured \n'
                      'SQLALCHEMY_DATABASE_URI variable correctly and connect to Northwestern VPN?')
        logger.error(f"{my_message} \n The original error message is: ", exc_info=True)
    except sqlalchemy.exc.IntegrityError:
        my_message = ('Have you already inserted the same record into the database before? \n'
                      'This database does not allow duplicate in the input-recommendation pair')
        logger.error(f"{my_message} \n The original error message is: ", exc_info=True)
    else:
        logger.info(f'{len(persist_list)} records were added to the table')
    # user_manager = UserManager(engine_string=args.engine_string)
    # try:
    #     user_manager.add_user(args.age, args.weight, args.height, args.neck, args.chest,
    #                      args.abdomen, args.hip, args.thigh, args.knee, args.ankle,
    #                      args.biceps, args.forearm, args.wrist)
    # except sqlite3.OperationalError as e:
    #     logger.error(
    #         "Error page returned. Not able to add song to local sqlite "
    #         "database: %s. Is it the right path? Error: %s ",
    #         args.engine_string, e)
    # except sqlalchemy.exc.OperationalError as e:
    #     logger.error(
    #         "Error page returned. Not able to add song to MySQL database.  "
    #         "Please check engine string and VPN. Error: %s ", e)
    # user_manager.close()
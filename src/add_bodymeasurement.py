import logging.config
import typing

import flask
import sqlalchemy
import sqlalchemy.orm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)

Base: typing.Any = declarative_base()


class UserInput(Base):
    """Creates a data model for the database to be set up for capturing body measurement info.
    """
    __tablename__ = 'UserInputs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), unique=False, nullable=False)
    age = Column(Integer, unique=False, nullable=False)
    weight = Column(Float, unique=False, nullable=False)
    height = Column(Float, unique=False, nullable=False)
    neck = Column(Float, unique=False, nullable=True)
    chest = Column(Float, unique=False, nullable=True)
    abdomen = Column(Float, unique=False, nullable=True)
    hip = Column(Float, unique=False, nullable=True)
    thigh = Column(Float, unique=False, nullable=True)
    knee = Column(Float, unique=False, nullable=True)
    ankle = Column(Float, unique=False, nullable=True)
    biceps = Column(Float, unique=False, nullable=True)
    forearm = Column(Float, unique=False, nullable=True)
    wrist = Column(Float, unique=False, nullable=True)

    def __repr__(self):
        return f'User_id: {self.id}, age: {self.age}, weight: {self.weight}, height:{self.height}'


def create_db(engine_string: str) -> None:
    """Create database from provided engine string.
    Args:
        engine_string (str): SQLAlchemy engine string specifying which database
                             to write to
    Returns: None
    """

    try:
        engine = sqlalchemy.create_engine(engine_string)
        Base.metadata.create_all(engine)
    except sqlalchemy.exc.ArgumentError:
        logger.error('%s is not a valid engine string', engine_string)
    except sqlalchemy.exc.OperationalError:
        logger.error('Failed to connect to server. '
                     'Please check if you are connected to Northwestern VPN')
    else:
        logger.info("Database created at %s", engine_string)


class UserInputManager:

    def __init__(self, app: typing.Optional[flask.app.Flask] = None,
                 engine_string: typing.Optional[str] = None):
        """
             Args:
                app (Flask): Flask app
                engine_string (str): Engine string
        """
        if app:
            self.database = SQLAlchemy(app)
            self.session = self.database.session
        elif engine_string:
            engine = sqlalchemy.create_engine(engine_string)
            session_maker = sqlalchemy.orm.sessionmaker(bind=engine)
            self.session = session_maker()
        else:
            raise ValueError(
                "Need either an engine string or a Flask app to initialize")

    def close(self) -> None:
        """Closes SQLAlchemy session
        Returns: None
        """
        self.session.close()

    def add_user(self, name: str, age: int, weight: float, height: float, neck: float = None,
                 chest: float = None, abdomen: float = None, hip: float = None, thigh: float = None,
                 knee: float = None, ankle: float = None, biceps: float = None, forearm: float = None,
                 wrist: float = None) -> None:
        """Seeds an existing database with additional songs.
        Args:
            name (str): User's name
            age (int): User's age
            weight (float): User's weight in pound
            height (float): User's height in inch
            neck (float): User's neck circumference in centimeter
            chest (float): User's chest circumference in centimeter
            abdomen (float): User's abdomen circumference in centimeter
            hip (float): User's hip circumference in centimeter
            thigh (float): User's thigh circumference in centimeter
            knee (float): User's knee circumference in centimeter
            ankle (float): User's ankle circumference in centimeter
            biceps (float): User's biceps circumference in centimeter
            forearm (float): User's forearm circumference in centimeter
            wrist (float): User's wrist circumference in centimeter
        Returns:
            None
        """

        try:
            session = self.session
            user = UserInput(name=name, age=age, weight=weight, height=height, neck=neck,
                             chest=chest, abdomen=abdomen, hip=hip, thigh=thigh,
                             knee=knee, ankle=ankle, biceps=biceps, forearm=forearm, wrist=wrist)
            session.add(user)
            session.commit()
        except sqlalchemy.exc.OperationalError:
            logger.error('Failed to connect to server. '
                         'Please check if you are connected to Northwestern VPN')
        else:
            logger.info("The user's body measurement information is added to database")
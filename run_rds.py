import argparse
import logging.config

from src.add_bodymeasurement import UserInputManager, create_db
from config.flaskconfig import SQLALCHEMY_DATABASE_URI

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('rds-pipeline')

if __name__ == '__main__':

    # Add parsers for both creating a database and adding applications to it
    parser = argparse.ArgumentParser(description="Create and/or add data to database")
    subparsers = parser.add_subparsers(dest="subparser_name")

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="Create database")
    sb_create.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")

    # Sub-parser for ingesting new data
    sb_ingest = subparsers.add_parser("ingest", description="Add data to database")
    # sb_ingest.add_argument("--id", help="App user's id")
    sb_ingest.add_argument("--name", help="App user's name")
    sb_ingest.add_argument("--age", help="App user's age")
    sb_ingest.add_argument("--height", help="App user's height in inches")
    sb_ingest.add_argument("--weight", help="App user's weight in pounds")
    sb_ingest.add_argument("--neck", help="App user's neck circumstance in cm")
    sb_ingest.add_argument("--chest", help="App user's chest circumstance in cm")
    sb_ingest.add_argument("--abdomen", help="App user's abdomen circumstance in cm")
    sb_ingest.add_argument("--hip", help="App user's hip circumstance in cm")
    sb_ingest.add_argument("--thigh", help="App user's thigh circumstance in cm")
    sb_ingest.add_argument("--knee", help="App user's knee circumstance in cm")
    sb_ingest.add_argument("--ankle", help="App user's ankle circumstance in cm")
    sb_ingest.add_argument("--biceps", help="App user's biceps circumstance in cm")
    sb_ingest.add_argument("--forearm", help="App user's forearm circumstance in cm")
    sb_ingest.add_argument("--wrist", help="App user's wrist circumstance in cm")
    sb_ingest.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")
    args = parser.parse_args()
    sp_used = args.subparser_name

    if sp_used == 'create_db':
        create_db(args.engine_string)
    elif sp_used == 'ingest':
        am = UserInputManager(engine_string=args.engine_string)
        am.add_user(args.name, args.age, args.height, args.weight, args.neck,
                    args.chest, args.abdomen, args.hip, args.thigh, args.knee,
                    args.ankle, args.biceps, args.forearm, args.wrist)
    else:
        parser.print_help()

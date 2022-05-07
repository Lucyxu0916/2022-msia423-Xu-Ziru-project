import argparse
import os
import sqlalchemy

import logging.config

from src.add_bodyfat import UserManager, create_db
from config.flaskconfig import SQLALCHEMY_DATABASE_URI

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('rds-pipeline')

if __name__ == '__main__':

    # Add parsers for both creating a database and adding pokemons to it
    parser = argparse.ArgumentParser(description="Create and/or add data to database")
    subparsers = parser.add_subparsers(dest='subparser_name')

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="Create database")
    sb_create.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")

    # Sub-parser for ingesting all data from a csv
    sb_ingest = subparsers.add_parser("ingest-csv", description="Add data to database")
    sb_ingest.add_argument("--input_path", default="=data/bodyfat.csv ", help="Name of file to be added")
    sb_ingest.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")

    args = parser.parse_args()
    sp_used = args.subparser_name
    if sp_used == 'create_db':
        create_db(args.engine_string)
    elif sp_used == 'ingest-csv':
        pm = UserManager(engine_string=args.engine_string)
        pm.add_user(args.input_path)
        pm.close()
    else:
        parser.print_help()
import logging.config
import argparse
import yaml

from src.preprocess_data import preprocess_data
from src.generate_features import get_features
from src.train_model import train
from src.score_model import predict
from src.evaulate_model import evaluate

LOGGING_CONFIG = "config/logging/local.conf"
logging.config.fileConfig(LOGGING_CONFIG, disable_existing_loggers=True)
logger = logging.getLogger("run.py")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="pipeline for running body fat prediction model")

    parser.add_argument("step",
                        help="Which step to run",
                        choices=["preprocess", "get_features", "train", "predict", "evaluate"])

    parser.add_argument("--config",
                        default="config/config.yaml",
                        help="Path to configuration file")

    args = parser.parse_args()

    with open(args.config, "r") as f:
        try:
            config = yaml.load(f, Loader=yaml.FullLoader)
        except yaml.error.YAMLError as e:
            logger.error("Error while loading configuration from %s", args.config)
        else:
            logger.info("Configuration file loaded from %s", args.config)

    if args.step == "preprocess":
        preprocess_data(config)
    elif args.step == "get_features":
        get_features(config)
    elif args.step == "train":
        train(config)
    elif args.step == "predict":
        predict(config)
    elif args.step == "evaluate":
        evaluate(config)

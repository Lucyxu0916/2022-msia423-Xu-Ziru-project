import logging
import pickle
import typing

import pandas as pd
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


def extract_features(data: pd.DataFrame, features_column: typing.List) -> pd.DataFrame:
    """ Extract features from dataframe
             Args:
                data (`:obj:`pd.DataFrame`): Dataframe
                features_column(`list` of `str`):  Column names for features
             Returns:
                features (`:obj:`pd.DataFrame`): Feature dataframe
    """
    try:
        features = data[features_column]
    except KeyError as e:
        logger.error("The key %s does not exist in the data", str(e))
    else:
        logger.info("Successfully extract features %s", str(features_column))

    return features


def extract_target(data: pd.DataFrame, target_column: str) -> pd.DataFram:
    """ Extract features from dataframe
             Args:
                data (`:obj:`pd.DataFrame`): Dataframe
                target_column(`list` of `str`):  Column name for target
             Returns:
                target (`:obj:`pd.DataFrame`): Target dataframe
    """
    try:
        target = data[target_column]
    except KeyError as e:
        logger.error("The key %s does not exist in the data", str(e))
    else:
        logger.info("Successfully extract target %s", str(target_column))

    return target


def scale_feature(feature: pd.DataFrame, scaler_path: str) -> pd.DataFrame:
    """ Extract features from dataframe
            Args:
               feature (`:obj:`pd.DataFrame`): The feature dataframe
               scaler_path (`str`): The path to save the scaler
            Returns:
               scaled_feature (`:obj:`pd.DataFrame`): The scaled feature dataframe
    """
    # standardize features
    scaler = StandardScaler()
    try:
        scaled_feature = scaler.fit_transform(feature)
    except TypeError as e:
        logger.error(e)
        raise e
    else:
        logger.info("Successfully scale features")

    # save the scaler at the scaler_path
    try:
        pickle.dump(scaler, open(scaler_path, "wb"))
    except FileNotFoundError as e:
        logger.error("The specified path %s does not exist", scaler_path)
    else:
        logger.info("Successfully save the scaler as %s", scaler_path)

    return scaled_feature

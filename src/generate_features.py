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
        raise e
    else:
        logger.info("Successfully extract features %s", str(features_column))

    return features


def extract_target(data: pd.DataFrame, target_column: str) -> pd.DataFrame:
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
        raise e
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

    # convert to dataframe
    scaled_feature_df = pd.DataFrame(scaled_feature, columns=feature.columns)

    # save the scaler at the scaler_path
    try:
        pickle.dump(scaler, open(scaler_path, "wb"))
    except FileNotFoundError as e:
        logger.error("The specified path %s does not exist", scaler_path)
    else:
        logger.info("Successfully save the scaler as %s", scaler_path)

    return scaled_feature_df


def save_data(data: pd.DataFrame, save_path: str) -> None:
    """ Save data to the specified path
     Args:
        data (`:obj:`pd.DataFrame`): Cleaned dataframe
        save_path (`str`): The path to save the cleaned data

     Returns:
        None
    """
    # save the data to the save_path
    try:
        data.to_csv(save_path, index=False)
    except FileNotFoundError as e:
        logger.error("The specified path %s does not exist", save_path)
        raise e
    else:
        logger.info("Successfully save data as %s", save_path)
        logger.debug("The shape of the data is %s", str(data.shape))


def get_features(config: dict) -> pd.DataFrame:
    """Applies featurization operations to input data.
        Args:
            config (`dict`): Dictionary of configurations
        Returns:
            features(`:obj:`pd.DataFrame`):dataset with features
    """

    # load the processed data
    try:
        path = config["get_features"]["load_path"]
        cleaned = pd.read_csv(path)
    except FileNotFoundError:
        logger.error("The specified path %s does not contain the file", path)
    else:
        logger.info("Successfully load the raw data from path %s", path)

    # extract features
    features = extract_features(cleaned, config["get_features"]["features_column"])
    # scale features
    scaled_features = scale_feature(features, config["get_features"]["scaler_path"])
    # extract target
    target = extract_target(cleaned, config["get_features"]["target_column"])
    # save scale features at the specified path
    save_data(scaled_features, config["get_features"]["feature_path"])
    # save target at the specified path
    save_data(target, config["get_features"]["target_path"])

    return features

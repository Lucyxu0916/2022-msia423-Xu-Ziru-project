import logging
import pickle
import typing

import pandas as pd
import sklearn
from sklearn import model_selection
from sklearn import linear_model

logger = logging.getLogger(__name__)


def data_split(features: pd.DataFrame, target: pd.DataFrame, feature_columns: typing.List, target_column: str,
               test_size: float, random_state: int, save_path: str) \
        -> typing.Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """ Splits dataframe into train and test feature sets and targets.
            Args:
                features (`pd.DataFrame`): Features data
                target (`pd.DataFrame`): Target data
                feature_columns (`list`): List of column name for features
                target_column (`str`): Column name of target variable
                test_size (`float`): Fraction of set to randomly sample to create test data
                random_state (`int`): Random state to make split reproducible
                save_path (`str`): The path to save train and test feature sets and targets
            Returns:
                x_train (`pd.DataFrame`): Features for training dataset
                x_test (`pd.DataFrame`): Features for testing dataset
                y_train (`pd.Series`): True target values for training dataset
                y_test (`pd.Series`): True target values for testing dataset
        """
    try:
        x_train, x_test, y_train, y_test = model_selection.train_test_split(
            features, target, test_size=test_size, random_state=random_state)
    except TypeError as e:
        logger.error(e)
        raise e
    except ValueError as e:
        logger.error(e)
        raise e
    else:
        logger.info("Successfully split the train and test set")

    try:
        file_path = save_path + "x_train.csv"
        x_train.to_csv(save_path + "x_train.csv", header=feature_columns, index=False)
    except FileNotFoundError as e:
        logger.error("The specified path %s does not exist", save_path)
        raise e
    else:
        logger.info("Successfully save the x_train file as %s", file_path)
        logger.debug("The shape of x_train is %s", str(x_train.shape))

    try:
        file_path = save_path + "x_test.csv"
        x_test.to_csv(file_path, header=feature_columns, index=False)
    except FileNotFoundError as e:
        logger.error("The specified path %s does not exist", save_path)
        raise e
    else:
        logger.info("Successfully save the x_test data as %s", file_path)
        logger.debug("The shape of x_test is %s", str(x_test.shape))

    try:
        file_path = save_path + "y_train.csv"
        y_train.to_csv(file_path, header=target_column, index=False)
    except FileNotFoundError as e:
        logger.error("The specified path %s does not exist", save_path)
        raise e
    else:
        logger.info("Successfully save the y_train data as %s", file_path)
        logger.debug("The shape of y_train is %s", str(y_train.shape))

    try:
        file_path = save_path + "y_test.csv"
        y_test.to_csv(file_path, header=target_column, index=False)
    except FileNotFoundError as e:
        logger.error("The specified path %s does not exist", file_path)
        raise e
    else:
        logger.info("Successfully save the y_test data as %s", file_path)
        logger.debug("The shape of y_test is %s", str(y_test.shape))

    return x_train, x_test, y_train, y_test


def model_train(x_train: pd.DataFrame, y_train: pd.Series, initial_features: typing.List[str],
                alpha: float, random_state: int, save_path: str) -> sklearn.base.BaseEstimator:
    """Fits a lasso regression model
        Args:
            x_train (`pd.DataFrame`): Features for training dataset
            y_train (`pd.Series`): True target values for training dataset
            initial_features (`list` of `str`): List of features to train on
            alpha (`float`): Constant that multiplies the L1 term, controlling regularization strength
            random_state (`int`): Random state to make model training reproducible
            save_path (`str`): The path to save the trained model
        Returns:
            model: Trained model object
        """
    # generate the model
    try:
        model = linear_model.Lasso(alpha=alpha, random_state=random_state)
    except ValueError as e:
        logger.error("Failed to generate the model")
        raise e
    else:
        logger.info("Successfully generate the Lasso model")

    # train the model
    try:
        model.fit(x_train[initial_features], y_train)
    except KeyError as e:
        logger.error("They key %s does not exist in the x_train data", str(e))
        raise e
    else:
        logger.info("Successfully train the Lasso model on x_train")

    # save the model
    try:
        pickle.dump(model, open(save_path, "wb"))
    except FileNotFoundError as e:
        logger.error("The specified path %s does not exist", save_path)
        raise e
    else:
        logger.info("Successfully save the model as %s", save_path)


def train(config: dict) -> None:
    """ Orchestrate model training by creating train test split, training model, and writing out trained model object
             Args:
                config (`dict`): Dictionary of configurations

             Returns:
                None
    """
    try:
        path = config["train"]["feature_path"]
        features = pd.read_csv(path)
    except FileNotFoundError:
        logger.error("The specified path %s does not contain the file", path)
    else:
        logger.info("Successfully load the features from path %s", path)

    try:
        path = config["train"]["target_path"]
        target = pd.read_csv(path)
    except FileNotFoundError:
        logger.error("The specified path %s does not contain the file", path)
    else:
        logger.info("Successfully load the target from path %s", path)

    # train test split
    x_train, _, y_train, _ = data_split(features, target, features.columns, target.columns,
                                        **config["train"]["data_split"])
    # train the model
    model_train(x_train, y_train, **config["train"]["model_train"])

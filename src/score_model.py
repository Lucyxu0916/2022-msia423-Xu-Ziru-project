import logging
import pickle
import typing

import pandas as pd
import numpy as np
import sklearn

logger = logging.getLogger(__name__)


def model_test(model: sklearn.base.BaseEstimator, x_test: pd.DataFrame, initial_features: typing.List[str],
               save_path: str) -> None:
    """Generate predictions
        Args:
            model (`sklearn.linear_model.LogisticRegression`): Trained model object
            x_test (`pd.DataFrame`): x_test data
            initial_features (`list` of `str`): List of features that were trained on
            save_path (`str`): The path to save the prediction result
        Returns:
            None
        """
    # generate predictions
    y_pred = model.predict(x_test[initial_features])
    try:
        np.savetxt(save_path, y_pred)
    except FileNotFoundError as e:
        logger.error("The specified path %s does not exist", save_path)
        raise e
    else:
        logger.info("Successfully save the prediction result as %s", save_path)


def predict(config: dict) -> None:
    """Score the provided model
        Args:
            config (`dict`): Dictionary of configurations

        Returns:
            None
    """

    # load x_test
    try:
        load_path = config["predict"]["load_path"]
        x_test = pd.read_csv(load_path)
    except FileNotFoundError as e:
        logger.error("The file does not exist at %s", load_path)
        raise e
    else:
        logger.info("Successfully load the x_test data")
        logger.debug("The shape of x_test is %s", str(x_test.shape))

    # load the model
    try:
        model_path = config["predict"]["model_path"]
        model = pickle.load(open(model_path, "rb"))
    except FileNotFoundError as e:
        logger.error("The model file does not exist at %s", model_path)
        raise e
    else:
        logger.info("Successfully load the model from %s", model_path)
    # generate predictions
    model_test(model, x_test, **config["predict"]["model_test"])

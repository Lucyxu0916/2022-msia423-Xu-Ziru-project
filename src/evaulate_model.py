import logging

import pandas as pd
import sklearn

logger = logging.getLogger(__name__)


def model_evaluate(y_test: pd.DataFrame, y_pred: pd.DataFrame, save_path: str) -> None:
    """Evaluate performance of model
        Args:
            y_test (`pd.DataFrame`): y_test data
            y_pred (`pd.DataFrame`): Prediction results
            save_path (`str`): The path to save evaluation results
        Returns:
            None
    """

    # calculate the MSE
    try:
        mean_squared_error = sklearn.metrics.mean_squared_error(y_test, y_pred)
    except TypeError as e:
        logger.error(e)
        raise e
    except ValueError as e:
        logger.error(e)
        raise e
    else:
        logger.info("Successfully calculate the MSE. The MSE was %0.2f", mean_squared_error)

    # calculate the RMSE
    try:
        rmse = sklearn.metrics.mean_squared_error(y_test, y_pred, squared=False)
    except TypeError as e:
        logger.error(e)
    except ValueError as e:
        logger.error(e)
        raise e
    else:
        logger.info("Successfully calculate the RMSE. The RMSE was %0.2f", rmse)

    # calculate the MAPE
    try:
        mean_absolute_percentage_error = sklearn.metrics.mean_absolute_percentage_error(y_test, y_pred)
    except TypeError as e:
        logger.error(e)
    except ValueError as e:
        logger.error(e)
        raise e
    else:
        logger.info("Successfully calculate the MAPE. The MAPE was %0.2f", mean_absolute_percentage_error)

    # calculate the R^2
    try:
        rsquared = sklearn.metrics.r2_score(y_test, y_pred)
    except TypeError as e:
        logger.error(e)
    except ValueError as e:
        logger.error(e)
        raise e
    else:
        logger.info("Successfully calculate the R squared. The R squared was %0.2f", rsquared)

    # save the performance metrics
    try:
        with open(save_path, "w") as file:
            file.write("MSE on test: %0.3f \n" % mean_squared_error)
            file.write("RMSE on test: %0.3f \n" % rmse)
            file.write("MAPE on test: %0.3f \n" % mean_absolute_percentage_error)
            file.write("R-squared on test: %0.3f \n" % rsquared)
    except FileNotFoundError as e:
        logger.error("The specified path %s does not exist", save_path)
        raise e
    except IOError as e:
        logger.error("IO Error %s", str(e))
        raise e
    else:
        logger.info("Successfully write and save the evaluation result as %s", save_path)


def evaluate(config: dict) -> None:
    """ Evaluate performance of model
             Args:
                config (`dict`): Dictionary of configurations

             Returns:
                None
    """
    # load y_test data
    try:
        load_path = config["evaluate"]["test_path"]
        y_test = pd.read_csv(load_path)
    except FileNotFoundError as e:
        logger.error("The file does not exist at the specified location %s", load_path)
        raise e
    else:
        logger.info("Successfully load the y_test data from %s", load_path)
        logger.debug("The shape of y_test is %s", str(y_test.shape))

    # load predictions
    try:
        prediction_path = config["evaluate"]["prediction_path"]
        y_pred = pd.read_csv(prediction_path, header=None)
    except FileNotFoundError as e:
        logger.error("The file does not exist at the specified location %s", prediction_path)
        raise e
    else:
        logger.info("Successfully load the class prediction from %s", prediction_path)
        logger.debug("The shape of class prediction is %s", str(y_pred.shape))

    # evaluate model
    model_evaluate(y_test, y_pred, config["evaluate"]["save_path"])

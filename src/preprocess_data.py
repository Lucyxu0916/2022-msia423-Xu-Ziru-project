import logging

import pandas as pd

logger = logging.getLogger(__name__)

def remove_outliers(data: pd.DataFrame, column_name: str, minimum: float, maximum: float) -> pd.DataFrame:
    """ Remove outliers from the specified column based on minimum and maximum value specified
             Args:
                data (`:obj:`pd.DataFrame`): Dataframe
                column_name (`str`): The name of the column whose outliers are removed
                minimum (`int`): The minimum value that should be kept
                maximum (`int`): The maximum value that should be kept
             Returns:
                data (`:obj:`pd.DataFrame`): Dataframe with no outlier
    """
    # drop values smaller than the minimum and larger than the maximum
    try:
        df = data.drop(data[data[column_name] < minimum].index)
        df = df.drop(data[data[column_name] > maximum].index)
    except KeyError as e:
        logger.error("The key %s does not exist in the data", str(e))
    else:
        logger.info("Successfully remove the outliers from %s column", column_name)

    return df


def save_cleaned_data(data: pd.DataFrame, save_path: str) -> None:
    """ Save cleaned data to the specified path
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
        logger.info("Successfully save the cleaned data as %s", save_path)
        logger.debug("The shape of the cleaned data is %s", str(data.shape))

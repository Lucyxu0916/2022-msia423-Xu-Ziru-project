import logging
import pandas as pd

logger = logging.getLogger(__name__)


def acquire_data(path: str) -> pd.DataFrame:
    """Acquires data from the path
       Args:
           path (`str`): Path to where data to be acquired is stored

       Returns:
           df (`pd.Dataframe`): Dataframe
       """
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        logger.error("The specified path %s does not contain the file", path)
    else:
        logger.info("Successfully acquire the data from path %s", path)

    return df

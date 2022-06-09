import pandas as pd
import pytest

from src.preprocess_data import remove_outliers

columns = ["Density", "BodyFat", "Age", "Weight", "Height", "Neck", "Chest",
           "Abdomen", "Hip", "Thigh", "Knee", "Ankle", "Biceps", "Forearm",
           "Wrist"]
raw_data = [[1.0502, 20.9, 24., 210.25, 74.75, 39.,
             104.5, 94.4, 107.8, 66., 42., 25.6,
             35.7, 30.6, 18.8],
            [1.0549, 19.2, 26., 181., 69.75, 36.4,
             105.1, 90.7, 100.3, 58.4, 38.3, 22.9,
             31.9, 27.8, 17.7],
            [1.0704, 12.4, 25., 176., 72.5, 37.8,
             99.6, 88.5, 97.1, 60., 39.4, 23.2,
             30.5, 29., 18.8],
            [1.09, 4.1, 25., 191., 30, 38.1,
             100.9, 82.5, 99.9, 62.9, 38.3, 23.8,
             35.9, 31.1, 18.2],
            [1.0722, 11.7, 23., 198.25, 100, 42.1,
             99.6, 88.6, 104.1, 63.1, 41.7, 25.,
             35.6, 30., 19.2]]
data = [[float(d) for d in row] for row in raw_data]


# happy path for testing remove_outliers
def test_remove_outliers():
    """test if remove_outliers function works as expected"""
    input_data = pd.DataFrame(data, columns=columns)

    expected_output = pd.DataFrame([[1.0502, 20.9, 24., 210.25, 74.75, 39.,
                                     104.5, 94.4, 107.8, 66., 42., 25.6,
                                     35.7, 30.6, 18.8],
                                    [1.0549, 19.2, 26., 181., 69.75, 36.4,
                                     105.1, 90.7, 100.3, 58.4, 38.3, 22.9,
                                     31.9, 27.8, 17.7],
                                    [1.0704, 12.4, 25., 176., 72.5, 37.8,
                                     99.6, 88.5, 97.1, 60., 39.4, 23.2,
                                     30.5, 29., 18.8]], columns=columns)

    output = remove_outliers(input_data, "Height", 60, 90)

    assert expected_output.equals(output)


# unhappy path for testing remove_outliers
def test_remove_outliers_not_existing():
    """test if remove_outliers function works as expected if the column given does not exist in the dataframe"""

    input_data = pd.DataFrame(data, columns=columns)
    non_exist_feature = "BMI"

    with pytest.raises(KeyError):
        remove_outliers(input_data, non_exist_feature, 30, 50)

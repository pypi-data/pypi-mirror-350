import numpy as np
import pandas as pd


def ensure_numpy_array(arr):
    """
    Helper function to ensure that the input is converted to a numpy array.

    Parameters:
        arr: Can be a list, pd.Series, or numpy array.

    Returns:
        numpy array: The converted array.
    """
    if isinstance(arr, pd.Series):
        return arr.to_numpy()
    elif isinstance(arr, list):
        return np.array(arr)
    return arr


class Metrics:
    """
    This class provides a set of metrics specific to time series analysis.
    Including measures such as Theil's U, WPODIC, among others, it provides useful tools for evaluating
    forecasting models and their performance in time series.

    ---
    References: [A non-central beta model for forecasting and evaluating pandemic time series](https://www.sciencedirect.com/science/article/pii/S096007792030607X)
    """

    @staticmethod
    def theil(y_true, y_pred):
        """
        Theil's U metric to compare model performance with a random walk model,
        returning a value greater than 0, the closer to 0 your model is,
        the better it performs against a random walk model, if Theil'U > 1,
        your prediction is worse than a random walk model, if Theil'U < 1,
        the model has better predictions than the random walk model,
        if Theil'U = 1, your model is equivalent to a random walk.

        Parameters:
            y_true: Actual values of the time series (can be list, pd.Series, or numpy array).
            y_pred: Predicted values by the model (can be list, pd.Series, or numpy array).

        Returns:
            float: Theil's U value.
        """
        y_true = ensure_numpy_array(y_true)
        y_pred = ensure_numpy_array(y_pred)

        if len(y_true) < 2 or len(y_pred) < 2:
            return np.nan

        # Naive prediction: one-period shift
        naive_pred = np.roll(y_true, 1)[1:]
        y_true = y_true[1:]  # Remove the first value (no prediction)
        y_pred = y_pred[1:]  # Remove the first value (no prediction)

        numerator = np.sum((y_true - y_pred) ** 2)
        denominator = np.sum((y_true - naive_pred) ** 2)

        return numerator / denominator if denominator != 0 else np.nan

    @staticmethod
    def mape(y_true, y_pred):
        """
        Mean Absolute Percentage Error (MAPE). Calculate the percentage error measure, no different from other packages.

        Parameters:
            y_true: Actual values of the time series (can be list, pd.Series, or numpy array).
            y_pred: Predicted values by the model (can be list, pd.Series, or numpy array).

        Returns:
            float: MAPE value.
        """
        y_true = ensure_numpy_array(y_true)
        y_pred = ensure_numpy_array(y_pred)

        # Avoid division by zero when true values are zero
        with np.errstate(divide="ignore", invalid="ignore"):
            percentage_errors = np.abs((y_true - y_pred) / y_true)
            percentage_errors = np.where(
                np.isfinite(percentage_errors), percentage_errors, np.nan
            )

        return np.nanmean(percentage_errors)

    @staticmethod
    def arv(y_true, y_pred):
        """
        ARV (Average Relative Variance) compares the performance of the
        predictor with the simple average of the past values ​​of the series,
        that is, the average is calculated point by point and compared with the prediction up to time n.

        Parameters:
            y_true: Actual values of the time series (can be list, pd.Series, or numpy array).
            y_pred: Predicted values by the model (can be list, pd.Series, or numpy array).

        Returns:
            float: ARV value.
        """
        y_true = ensure_numpy_array(y_true)
        y_pred = ensure_numpy_array(y_pred)

        y_mean = np.mean(y_true)

        numerator = np.sum((y_true - y_pred) ** 2)
        denominator = np.sum((y_true - y_mean) ** 2)

        return numerator / denominator if denominator != 0 else np.nan

    @staticmethod
    def disagreement_index(y_true, y_pred):
        """
        The ID (Discordance Index) disregards the unit of measurement, presenting values ​​in the range [0, 1].

        Parameters:
            y_true: Actual values of the time series (can be list, pd.Series, or numpy array).
            y_pred: Predicted values by the model (can be list, pd.Series, or numpy array).

        Returns:
            float: ID value.
        """
        y_true = ensure_numpy_array(y_true)
        y_pred = ensure_numpy_array(y_pred)

        y_mean = np.mean(y_pred)

        numerator = np.sum((y_pred - y_true) ** 2)
        denominator = np.sum((np.abs(y_pred - y_mean) + np.abs(y_true - y_mean)) ** 2)

        return numerator / denominator if denominator != 0 else np.nan

    @staticmethod
    def wpocid(y_true, y_pred):
        """
        WPOCID measures how well the model predicts the trend of the target time series,
        presenting values ​​between 0 and 1, where the models perform better the higher the WPOCID,
        if WPOCID = 0.6, the model was correct 60% of the time in the trend of the series, that is,
        it predicted correct rises or falls.

        Parameters:
            y_true: Actual values of the time series (can be list, pd.Series, or numpy array).
            y_pred: Predicted values by the model (can be list, pd.Series, or numpy array).

        Returns:
            float: WPOCID value.
        """
        y_true = ensure_numpy_array(y_true)
        y_pred = ensure_numpy_array(y_pred)

        sum_D_t = 0

        for t in range(1, len(y_true)):
            if (y_true[t] - y_true[t - 1]) * (y_pred[t] - y_pred[t - 1]) >= 0:
                sum_D_t += 1

        N = len(y_true)
        return 1 - (sum_D_t / (N - 1)) if N > 1 else np.nan

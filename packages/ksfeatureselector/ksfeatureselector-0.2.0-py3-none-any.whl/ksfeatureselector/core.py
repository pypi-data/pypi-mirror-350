from scipy import stats
import pandas as pd
import numpy as np
from itertools import combinations
import warnings

RANDOM_SEED = 42

def sort_tuple(tup, reverse=False):
    """
    Sorts a list of 2-element tuples based on the second element.

    This helper function is designed to sort lists of 2-element tuples, typically
    where the first element is a feature name (string) and the second is a
    p-value (float) from a statistical test like the Kolmogorov-Smirnov test.
    The sorting order (ascending or descending) is controlled by the `reverse` flag.

    Parameters 
    ----------
    tup : list of tuples
        A list where each element is a tuple of the form (str, float). The
        first element is expected to be a feature identifier (e.g., column name),
        and the second element is a numerical value, typically a p-value,
        between 0 and 1.
    reverse : bool, optional
        If True, the list of tuples will be sorted in descending order based
        on the second element of each tuple. If False (default), it sorts
        in ascending order.

    Returns
    -------
    list of tuples
        The input list of tuples, sorted according to the specified order
        based on their second element.

    Raises
    ------
    AssertionError
        - If `tup` is not a list.
        - If `reverse` is not a boolean.
        - If any element within `tup` is not a tuple.
        - If the first element of any inner tuple is not a string.
        - If the second element of any inner tuple is not a float between 0 and 1.
    """
    assert isinstance(tup, list), "'tup' must be a list."
    assert isinstance(reverse, bool), "'reverse' must be of type bool."
    for x in tup:
        assert isinstance(x, tuple), "List given has elements of type other than tuple."
        assert len(x) == 2, "Each tuple in 'tup' must have exactly 2 elements."
        assert isinstance(x[0], str), "First element of tuple not a column name (string)."
        assert isinstance(x[1], (int, float)), "Second element of tuple not a number."
        assert 0 <= x[1] <= 1, "P-value out of bounds (must be between 0 and 1)."

    tup.sort(key=lambda x: x[1], reverse=reverse)
    return tup

class KSFeatureSelector:
    """
    A feature selector that uses the Kolmogorov-Smirnov (KS) test to identify
    discriminatory features for binary and multi-class classification problems.

    This class provides a flexible framework to perform feature selection based
    on the KS test. It supports two main comparison strategies for multi-class
    targets: 'pairwise' (comparing every unique pair of classes) and 'one-vs-rest'
    (comparing each class against all other classes combined). The p-values
    resulting from these comparisons are then aggregated using either Fisher's
    method, or by taking the minimum or maximum p-value.

    The maximum number of supported classes in the target variable is internally
    limited to 10 for robustness and to prevent excessive computational load
    for the underlying statistical tests.

    Parameters
    ----------
    aggregation_method : str, optional
        The strategy to use for performing KS tests when the target variable
        has multiple classes.
        - 'pairwise' (default): Performs KS tests between every unique pair of classes.
        - 'one-vs-rest': Performs KS tests for each class against the combined data
          of all other classes.
        Raises AssertionError if the value is not 'pairwise' or 'one-vs-rest'.
    p_value_aggregation_method : str, optional
        The method to aggregate the individual p-values obtained from multiple
        KS tests for a single feature.
        - 'fisher' (default): Uses Fisher's combined probability test.
        - 'min': Takes the minimum p-value among all individual tests for the feature.
        - 'max': Takes the maximum p-value among all individual tests for the feature.
        Raises AssertionError if the value is not 'fisher', 'min', or 'max'.

    Attributes
    ----------
    selected_features_ : list of str
        A list of feature names that are selected by the `transform` method
        based on the specified `top_n` or `top_p` criteria. This attribute
        is populated after `fit` and updated by `transform`.
    feature_p_values_ : list of tuple
        A list of (feature_name, aggregated_p_value) tuples for all features
        considered during `fit`. The list is sorted in ascending order of
        aggregated p-values (lower p-value indicates higher discriminatory power).
        This attribute is populated after `fit`.
    """

    # Internal constant for the maximum number of classes allowed in the target variable.
    # This is a library-imposed limit for performance and appropriate use cases.
    _MAX_ALLOWED_CLASSES = 10
    # Internal constant for the minimum recommended number of observations per category
    # in the target variable for reliable KS test results.
    _MIN_OBS_PER_CATEGORY_WARNING = 10

    def __init__(self, aggregation_method='pairwise', p_value_aggregation_method='fisher'):
        """
        Initializes the KSFeatureSelector with the specified comparison and
        p-value aggregation methods.

        Parameters
        ----------
        aggregation_method : str, optional
            The strategy to use for performing KS tests when the target variable
            has multiple classes.
            - 'pairwise' (default): Performs KS tests between every unique pair of classes.
            - 'one-vs-rest': Performs KS tests for each class against the combined data
              of all other classes.
        p_value_aggregation_method : str, optional
            The method to aggregate the individual p-values obtained from multiple
            KS tests for a single feature.
            - 'fisher' (default): Uses Fisher's combined probability test.
            - 'min': Takes the minimum p-value among all individual tests for the feature.
            - 'max': Takes the maximum p-value among all individual tests for the feature.

        Raises
        ------
        AssertionError
            - If `aggregation_method` is not 'pairwise' or 'one-vs-rest'.
            - If `p_value_aggregation_method` is not 'fisher', 'min', or 'max'.
        """
        assert aggregation_method in ['pairwise', 'one-vs-rest'], \
            f"Invalid aggregation_method: '{aggregation_method}'. Must be 'pairwise' or 'one-vs-rest'."
        assert p_value_aggregation_method in ['fisher', 'min', 'max'], \
            f"Invalid p_value_aggregation_method: '{p_value_aggregation_method}'. Must be 'fisher', 'min', or 'max'."

        self.aggregation_method = aggregation_method
        self.p_value_aggregation_method = p_value_aggregation_method
        self.selected_features_ = None
        self.feature_p_values_ = None

    def _validate_inputs(self, df, x_cols, y_var):
        """
        Internal helper method to validate the input DataFrame, feature columns,
        and target variable. It performs type checks and checks for data integrity
        relevant to the KS test.

        Parameters
        ----------
        df : pandas.DataFrame
            The input DataFrame containing features and the target variable.
        x_cols : list of str
            A list of column names representing the features to be considered.
        y_var : str
            The name of the target variable column in the DataFrame.

        Returns
        -------
        None
            This method does not return any value. It raises an AssertionError
            or issues a UserWarning if validation fails.

        Raises
        ------
        AssertionError
            - If `df` is not a pandas DataFrame.
            - If `x_cols` is not a list.
            - If `y_var` is not found in the DataFrame's columns.
            - If the number of unique classes in `y_var` is less than 2 or
              exceeds `_MAX_ALLOWED_CLASSES`.
            - If any column in `x_cols` is not found in the DataFrame.
            - If any feature column in `x_cols` contains non-numeric values.

        Warnings
        --------
        UserWarning
            - If any category in the `y_var` column has fewer observations than
              `_MIN_OBS_PER_CATEGORY_WARNING`. This indicates that statistical
              power for comparisons involving that category might be low.
        """
        assert isinstance(df, pd.DataFrame), "'df' must be a pandas DataFrame."
        assert isinstance(x_cols, list), "'x_cols' must be a list of column names."
        assert y_var in df.columns, f"Target variable '{y_var}' does not exist in the dataframe."

        num_unique_classes = len(df[y_var].unique())
        assert 2 <= num_unique_classes <= self._MAX_ALLOWED_CLASSES, \
            f"The target variable '{y_var}' has {num_unique_classes} distinct values. " \
            f"This selector supports 2 to {self._MAX_ALLOWED_CLASSES} distinct values."

        # Check minimum observations per category in the target variable
        category_counts = df[y_var].value_counts()
        for category, count in category_counts.items():
            if count < self._MIN_OBS_PER_CATEGORY_WARNING:
                warnings.warn(
                    f"UserWarning: Category '{category}' in target variable '{y_var}' "
                    f"has only {count} observations, which is less than the recommended minimum "
                    f"of {self._MIN_OBS_PER_CATEGORY_WARNING} for reliable KS test results."
                )

        for col in x_cols:
            assert col in df.columns, f"Feature variable '{col}' does not exist in the dataframe."
            if not pd.api.types.is_numeric_dtype(df[col]):
                 raise AssertionError(f"Not all values in '{col}' are numeric. Please ensure all feature columns are numeric.")

    @staticmethod
    def _aggregate_p_values(p_values_for_feature, method):
        """
        Aggregates a list of individual p-values using the specified statistical method.

        This static method is used internally to combine multiple p-values
        (obtained from pairwise or one-vs-rest KS tests for a single feature)
        into a single, summary p-value. If the input list of p-values is empty,
        it returns 1.0, indicating no significant comparison could be made.

        Parameters
        ----------
        p_values_for_feature : list of float
            A list containing the individual p-values obtained from various
            KS test comparisons for a single feature. Each p-value should be
            between 0 and 1.
        method : str
            The aggregation method to apply. Valid options are:
            - 'fisher': Uses Fisher's combined probability test.
            - 'min': Returns the minimum p-value from the list.
            - 'max': Returns the maximum p-value from the list.

        Returns
        -------
        float
            The single, aggregated p-value, which will be between 0 and 1.

        Raises
        ------
        ValueError
            - If an unknown `method` is provided (though this should be caught
              by `__init__` validation).
        """
        if not p_values_for_feature:
            # This case should ideally not be reached if comparison methods append 1.0
            # for insufficient samples, but included for robustness.
            return 1.0 # Return a non-significant p-value if no comparisons were made

        if method == 'fisher':
            p_values_for_feature = np.array(p_values_for_feature)
            # Replace 0 with a very small number to avoid log(0) issues in Fisher's method.
            p_values_for_feature[p_values_for_feature == 0] = np.finfo(float).eps
            chi_squared_stat = -2 * np.sum(np.log(p_values_for_feature))
            df_fisher = 2 * len(p_values_for_feature)
            # Use survival function (1 - CDF) of chi-squared distribution
            aggregated_p_value = stats.chi2.sf(chi_squared_stat, df_fisher)
        elif method == 'min':
            aggregated_p_value = np.min(p_values_for_feature)
        elif method == 'max':
            aggregated_p_value = np.max(p_values_for_feature)
        else:
            # This should be caught by __init__ validation, but for robustness
            raise ValueError(f"Unknown p_value_aggregation_method: '{method}'.")

        return aggregated_p_value

    def _get_pairwise_p_values(self, feature_series, target_series, unique_classes):
        """
        Performs Kolmogorov-Smirnov (KS) tests for a single feature by comparing
        all unique pairs of classes within the target variable.

        If a comparison cannot be performed due to insufficient samples in one
        or both groups, a UserWarning is issued, and a p-value of 1.0 (non-significant)
        is recorded for that specific comparison.

        Parameters
        ----------
        feature_series : pandas.Series
            A pandas Series representing the data for a single feature column.
        target_series : pandas.Series
            A pandas Series representing the target variable data.
        unique_classes : numpy.ndarray or list
            An array or list of the unique class labels present in the target variable.

        Returns
        -------
        list of float
            A list of p-values obtained from all valid pairwise KS tests for the
            given feature. Includes 1.0 for skipped comparisons.

        Warnings
        --------
        UserWarning
            - If a KS test between two classes cannot be performed because one
              or both of the class samples for the given feature are empty.
              The warning message will include the feature name, class values,
              and the sizes of the empty samples.
        """
        p_values = []
        class_pairs = list(combinations(unique_classes, 2))
        for class1_val, class2_val in class_pairs:
            data_class1 = feature_series[target_series == class1_val]
            data_class2 = feature_series[target_series == class2_val]

            if data_class1.empty or data_class2.empty:
                warnings.warn(
                    f"UserWarning: Skipping KS test for feature '{feature_series.name}' between classes "
                    f"'{class1_val}' and '{class2_val}' due to insufficient samples in one or both groups ({len(data_class1)} vs {len(data_class2)}). "
                    f"P-value for this comparison will be treated as 1.0."
                )
                p_values.append(1.0)
            else:
                _, p_value = stats.ks_2samp(data_class1, data_class2)
                p_values.append(p_value)
        return p_values

    def _get_one_vs_rest_p_values(self, feature_series, target_series, unique_classes):
        """
        Performs Kolmogorov-Smirnov (KS) tests for a single feature by comparing
        each class against all other classes combined (one-vs-rest strategy).

        If a comparison cannot be performed due to insufficient samples in one
        or both groups, a UserWarning is issued, and a p-value of 1.0 (non-significant)
        is recorded for that specific comparison.

        Parameters
        ----------
        feature_series : pandas.Series
            A pandas Series representing the data for a single feature column.
        target_series : pandas.Series
            A pandas Series representing the target variable data.
        unique_classes : numpy.ndarray or list
            An array or list of the unique class labels present in the target variable.

        Returns
        -------
        list of float
            A list of p-values obtained from all valid one-vs-rest KS tests for the
            given feature. Includes 1.0 for skipped comparisons.

        Warnings
        --------
        UserWarning
            - If a KS test for a specific class (one-vs-rest) cannot be performed
              because the class's sample or the 'rest' sample for the given feature
              is empty. The warning message will include the feature name, class value,
              and the sizes of the empty samples.
        """
        p_values = []
        for class_val in unique_classes:
            class_data = feature_series[target_series == class_val]
            rest_data = feature_series[target_series != class_val]

            if class_data.empty or rest_data.empty:
                warnings.warn(
                    f"UserWarning: Skipping KS test for feature '{feature_series.name}' for class "
                    f"'{class_val}' (one-vs-rest) due to insufficient samples in one or both groups ({len(class_data)} vs {len(rest_data)}). "
                    f"P-value for this comparison will be treated as 1.0."
                )
                p_values.append(1.0)
            else:
                _, p_value = stats.ks_2samp(class_data, rest_data)
                p_values.append(p_value)
        return p_values

    def fit(self, df, x_cols, y_var):
        """
        Fits the feature selector to the data.

        This method calculates the aggregated p-value for each feature based
        on the specified `aggregation_method` and `p_value_aggregation_method`.
        The results (feature names and their aggregated p-values) are stored
        internally in `self.feature_p_values_` and sorted in ascending order
        of p-value. `self.selected_features_` is also initialized to contain
        all features in this sorted order.

        Parameters
        ----------
        df : pandas.DataFrame
            The input DataFrame containing the features and the target variable.
            All feature columns specified in `x_cols` must be numeric.
        x_cols : list of str
            A list of column names representing the features to be evaluated
            for discriminatory power.
        y_var : str
            The name of the target variable column in the DataFrame. This
            column is expected to contain categorical labels (binary or multi-class).

        Returns
        -------
        self : object
            Returns the instance of the KSFeatureSelector itself, allowing for
            method chaining (e.g., `selector.fit(...).transform(...)`).

        Raises
        ------
        AssertionError
            - Propagates from `_validate_inputs` if input data types or structure
              are invalid.
            - Propagates from `sort_tuple` if the internal list of tuples is
              malformed (unlikely with correct internal logic).

        Warnings
        --------
        UserWarning
            - Propagates from `_validate_inputs` if target categories have too few observations.
            - Propagates from `_get_pairwise_p_values` or `_get_one_vs_rest_p_values`
              if specific KS tests cannot be performed due to insufficient samples.
        """
        self._validate_inputs(df, x_cols, y_var)

        unique_classes = df[y_var].unique()
        feature_p_values_list = []

        for col in x_cols:
            individual_p_values = []
            if self.aggregation_method == 'pairwise':
                individual_p_values = self._get_pairwise_p_values(df[col], df[y_var], unique_classes)
            elif self.aggregation_method == 'one-vs-rest':
                individual_p_values = self._get_one_vs_rest_p_values(df[col], df[y_var], unique_classes)
            
            if individual_p_values: # Only aggregate if there are p-values to aggregate
                aggregated_p_value = self._aggregate_p_values(individual_p_values, self.p_value_aggregation_method)
                feature_p_values_list.append((col, aggregated_p_value))

        self.feature_p_values_ = sort_tuple(feature_p_values_list)
        self.selected_features_ = [tup[0] for tup in self.feature_p_values_] # All features initially

        return self

    def transform(self, top_n=None, top_p=None):
        """
        Selects and returns a list of feature names based on the specified
        selection criteria (either `top_n` or `top_p`).

        This method must be called after the `fit` method has been executed,
        as it relies on the calculated feature p-values. If neither `top_n`
        nor `top_p` is provided, all features (sorted by p-value) are returned.

        Parameters
        ----------
        top_n : int, optional
            The number of top features to return. Features are ranked by their
            aggregated p-value in ascending order (lower p-value is better).
            This parameter is mutually exclusive with `top_p`.
            If provided, must be a positive integer not exceeding the total
            number of features.
        top_p : float, optional
            The maximum allowed aggregated p-value for a feature to be selected.
            Features with an aggregated p-value less than or equal to this
            threshold will be returned. This parameter is mutually exclusive
            with `top_n`. If provided, must be a float between 0 and 1.

        Returns
        -------
        list of str
            A list of selected feature names, sorted by their discriminatory power
            (ascending aggregated p-value).

        Raises
        ------
        ValueError
            - If the `fit` method has not been called prior to `transform`.
            - If both `top_n` and `top_p` are provided simultaneously.
            - If `top_p` is provided but is not a float between 0 and 1.
            - If `top_n` is provided but is not a positive integer within the
              valid range (1 to total number of features).
        """
        if self.feature_p_values_ is None:
            raise ValueError("The selector has not been fitted yet. Call 'fit' before 'transform'.")

        if top_n is not None and top_p is not None:
            raise ValueError("Only one of 'top_p' or 'top_n' should be provided, not both.")
        
        # If neither is provided, return all sorted features
        if top_n is None and top_p is None:
            return self.selected_features_

        selected_features_list = []
        if top_p is not None:
            if not (0 <= top_p <= 1):
                raise ValueError(f"'top_p' must be between {0} and {1}. Got: {top_p}")
            selected_features_list = [tup[0] for tup in self.feature_p_values_ if tup[1] <= top_p]
        elif top_n is not None:
            if not (1 <= top_n <= len(self.feature_p_values_)):
                raise ValueError(f"'top_n' must be between {1} and the total number of features ({len(self.feature_p_values_)}). Got: {top_n}")
            selected_features_list = [tup[0] for tup in self.feature_p_values_[:top_n]]

        return selected_features_list

    def get_feature_p_values(self):
        """
        Retrieves the calculated aggregated p-values for all features.

        This method returns a list of tuples, where each tuple contains a
        feature name and its corresponding aggregated p-value. The list is
        sorted in ascending order based on the p-values, making it easy to
        see the ranking of features by their discriminatory power.

        Parameters
        ----------
        None

        Returns
        -------
        list of tuple
            A list of (feature_name, aggregated_p_value) tuples. This list
            is sorted from the most discriminatory feature (lowest p-value)
            to the least discriminatory (highest p-value).

        Raises
        ------
        ValueError
            - If the `fit` method has not been called prior to `get_feature_p_values`.
        """
        if self.feature_p_values_ is None:
            raise ValueError("The selector has not been fitted yet. Call 'fit' before 'get_feature_p_values'.")
        return self.feature_p_values_

# The `select_ks_features` wrapper function
def select_ks_features(df, x_cols, y_var, top_n=None, top_p=None, aggregation_method='pairwise', p_value_aggregation_method='fisher'):
    """
    A convenience wrapper function for the KSFeatureSelector class.

    This function provides a simplified interface for performing one-off
    feature selection using the Kolmogorov-Smirnov test without needing
    to explicitly instantiate and manage a `KSFeatureSelector` object.
    It creates a selector instance, fits it to the data, and then
    transforms it to return the selected features directly.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing the features and the target variable.
        All feature columns specified in `x_cols` must be numeric.
    x_cols : list of str
        A list of column names representing the features to be evaluated
        for discriminatory power.
    y_var : str
        The name of the target variable column in the DataFrame. This
        column is expected to contain categorical labels (binary or multi-class).
    top_n : int, optional
        The number of top features to return. Features are ranked by their
        aggregated p-value in ascending order (lower p-value is better).
        This parameter is mutually exclusive with `top_p`.
        If provided, must be a positive integer not exceeding the total
        number of features.
    top_p : float, optional
        The maximum allowed aggregated p-value for a feature to be selected.
        Features with an aggregated p-value less than or equal to this
        threshold will be returned. This parameter is mutually exclusive
        with `top_n`. If provided, must be a float between 0 and 1.
    aggregation_method : str, optional
        The strategy to use for performing KS tests when the target variable
        has multiple classes.
        - 'pairwise' (default): Performs KS tests between every unique pair of classes.
        - 'one-vs-rest': Performs KS tests for each class against the combined data
          of all other classes.
    p_value_aggregation_method : str, optional
        The method to aggregate the individual p-values obtained from multiple
        KS tests for a single feature.
        - 'fisher' (default): Uses Fisher's combined probability test.
        - 'min': Takes the minimum p-value from the list.
        - 'max': Takes the maximum p-value from the list.

    Returns
    -------
    list of str
        A list of selected feature names, sorted by their discriminatory power
        (ascending aggregated p-value).

    Raises
    ------
    AssertionError
        - Propagates from `KSFeatureSelector.__init__` if `aggregation_method` or
          `p_value_aggregation_method` are invalid.
        - Propagates from `KSFeatureSelector._validate_inputs` if input data types
          or structure are invalid (e.g., non-existent columns, non-numeric features,
          invalid number of target classes).

    ValueError
        - Propagates from `KSFeatureSelector.transform` if both `top_n` and `top_p`
          are provided, or if their values are out of valid ranges.

    Warnings
    --------
    UserWarning
        - Propagates from `KSFeatureSelector._validate_inputs` if target categories
          have too few observations.
        - Propagates from `KSFeatureSelector._get_pairwise_p_values` or
          `KSFeatureSelector._get_one_vs_rest_p_values` if specific KS tests cannot
          be performed due to insufficient samples.
    """
    selector = KSFeatureSelector(
        aggregation_method=aggregation_method,
        p_value_aggregation_method=p_value_aggregation_method
    )
    selector.fit(df, x_cols, y_var)
    return selector.transform(top_n=top_n, top_p=top_p)

from scipy import stats
import pandas as pd
RANDOM_SEED = 42

def sort_tuple(tup,rev = False):
    """
    Sorts a list of 2-element tuples based on the second element.

    This function is designed to sort tuples where the second element is
    a p-value from a statistical test (e.g., KS test). Sorting is
    done in ascending or descending order based on the `reverse` flag.

    Parameters
    ----------
    tup : list of tuple
        A list where each element is a tuple of the form (str, float). The
        first element is typically a feature name, and the second is a p-value.
    rev : bool, optional
        If True, sorts in descending order of the second element (default is False).

    Returns
    -------
    list of tuple
        Sorted list of tuples based on the second element.
    
    Raises
    ------
    AssertionError
        If the input is not a list of valid 2-element tuples or if the 'reverse' flag is not boolean
    """
    assert isinstance(tup,list), "'tup' must be a list"
    assert isinstance(rev,bool), "'rev' must be of type bool"
    for x in tup:
       assert isinstance(x,tuple), "list given has elements of type other than tuple"
       assert isinstance(x[0],str), "first element of tuple not a column name"
       assert x[1] <= 1 and x[1] >= 0, "k-s test statistic out of bounds"

    tup.sort(key = lambda x: x[1],reverse = rev)
    return tup

def ks_sorted_features(feat_df,y_var,top_p,top_n):
    """
    Selects the most discriminatory features using the KS test p-value.

    This function calculates the Kolmogorov–Smirnov (KS) test between the two
    classes in the target variable for each feature. It ranks features by their
    ability to discriminate between the classes (lower p-values are better discriminators).

    Parameters
    ----------
    feat_df : pandas.DataFrame
        A DataFrame containing the features and the target variable.
    y_var : str
        The name of the binary target variable in the DataFrame.
    top_p : float or None
        Maximum allowed p-value to consider a feature significant. Must be between 0 and 1.
    top_n : int or None
        Number of top features to return based on KS significance.

    Returns
    -------
    list of str
        A list of selected feature names sorted by discriminatory power (ascending p-values).

    Raises
    ------
    AssertionError
        If `y_var` is not found in the DataFrame, or is not binary.
    ValueError
        If both `top_p` and `top_n` are provided, or if bounds are violated.
    """
    assert y_var in feat_df.columns, f"target variable '{y_var}' does not exist in the dataframe"
    assert len(feat_df[y_var].unique()) == 2, f"the target value '{y_var}' has \
    more than 2 distinct values, this function works only for binary classification"

    # check bounds for top_p and top_n, top_p is the p-value threshold, must be between 0 and 1
    if top_p is not None:
        if not (0 <= top_p <= 1):
            raise ValueError(f"'top_p' must be between {0} and {1}. Got: {top_p}")

    # top_n is the top n significant features
    if top_n is not None:
        max_n = len(feat_df.columns)-1
        if not (1 <= top_n <= max_n):
            raise ValueError(f"'top_n' must be between {1} and no. of features {max_n}. Got: {top_n}")

    # get the two unique class values
    unique_classes = feat_df[y_var].unique()
    class1_value = unique_classes[0]
    class2_value = unique_classes[1]

    # split the data for each of the two class values
    class1_data = feat_df[feat_df[y_var]==class1_value]
    class2_data = feat_df[feat_df[y_var]==class2_value]

    # list to stoe each feature and its k-s test stat p-value
    ks_tup_list = []

    for col in feat_df.columns:
        # get the feature for each of the classes
        x = class1_data[col]
        y = class2_data[col]

        # calculate the k-s test p-value, store the feature and p-value
        ks_tup_list.append((col,stats.ks_2samp(x, y)[1]))

    # sort the list in descending order of importance of features, lower p-value means more importance
    ks_sorted = sort_tuple(ks_tup_list)
    if top_p is not None:
        top_tuples = [tup for tup in ks_sorted if tup[1] <= top_p]
    elif top_n is not None:
        top_tuples = ks_sorted[:top_n+1]
    else:
        top_tuples = ks_sorted
    best_features = list(list(zip(*top_tuples))[0])
    if y_var in best_features:
        best_features.remove(y_var)
    return best_features



def select_ks_features(df, x_cols, y_var, top_n = None, top_p = None):
    """
    Wrapper function to select KS test-based features with input validation.

    This function checks that inputs are valid and calls the feature selection
    pipeline to compute the most important features based on KS test p-values.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing the features and target.
    x_cols : list of str
        Names of the feature columns to consider.
    y_var : str
        Name of the binary classification target variable.
    top_n : int, optional
        Number of top features to return (mutually exclusive with `top_p`).
    top_p : float, optional
        Maximum p-value threshold for feature selection (mutually exclusive with `top_n`).

    Returns
    -------
    list of str
        A list of feature names selected based on the KS test.

    Raises
    ------
    AssertionError
        If inputs are invalid or not well-typed.
    ValueError
        If both `top_n` and `top_p` are provided.
    """
    assert isinstance(x_cols, list)

    assert y_var in df.columns, f"target variable '{y_var}' does not exist in the dataframe"
    assert len(df[y_var].unique()) == 2, f"the target variable '{y_var}' has more than 2 distinct values"

    for col in x_cols:
        assert col in df.columns, f"feature variable '{col}' does not exist in the dataframe"
        assert df[col].apply(lambda x: isinstance(x, (int, float))).all(), \
            f"Not all values in '{col}' are int or float, please use dummy variables if the variable is categorical"

    if top_n is not None and top_p is not None:
        raise ValueError("Only one of 'top_p' or 'top_n' should be provided, not both.")



    feat_df = df[x_cols+[y_var]]

    best_features = ks_sorted_features(feat_df,y_var,top_p,top_n)

    return best_features
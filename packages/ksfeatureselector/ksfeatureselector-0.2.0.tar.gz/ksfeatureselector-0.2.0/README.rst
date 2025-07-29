KSFeatureSelector
=================

``KSFeatureSelector`` is a robust and flexible Python package designed for selecting the most discriminatory features in both **binary and multi-class classification problems** using the Kolmogorov-Smirnov (K-S) test. It provides advanced options for handling multi-class scenarios and aggregating p-values.

Features
--------

- Uses the K-S test to rank features by their ability to separate classes.
- Handles target variables with more than two categories (up to 10 classes internally).
- Flexible Comparison Strategies:
    -  `pairwise`: Performs K-S tests between every unique pair of classes.
    -  `one-vs-rest`: Compares each class against all other classes combined.
- Multiple P-Value Aggregation Methods:
    -  `fisher`: Uses Fisher's combined probability test (default, generally recommended).
    -  `min`: Takes the minimum p-value from all comparisons for a feature.
    -  `max`: Takes the maximum p-value from all comparisons for a feature.
-  Scikit-learn Style API: Offers a class-based interface (`KSFeatureSelector` with `fit`, `transform`) for seamless integration into machine learning pipelines.
-  Convenience Function: Provides a simple `select_ks_features` wrapper for quick, one-off feature selection.
-  Robust Validation & Warnings: Includes comprehensive input validation and issues `UserWarning` for data quality issues, such as categories with too few observations or insufficient samples for K-S tests.
-  Pure Python: Built using `pandas`, `scipy`, and `numpy`.

Installation
------------

.. code-block:: bash

   pip install ksfeatureselector

For local installation:

.. code-block:: bash

   pip install -e .

Usage
-----

.. code-block:: python

   from ksfeatureselector import select_ks_features

   significant_features = select_ks_features(
       df, x_cols, y_var,
       top_p=0.01,
       aggregation_method='one-vs-rest',
       p_value_aggregation_method='min'
   )
   print(f"Significant features (one-vs-rest, min p-value <= 0.01): {significant_features}")

   # Example 3: Select top 3 features using 'pairwise' comparison
   # and 'max' p-value aggregation
   top_3_features_max_agg = select_ks_features(
       df, x_cols, y_var,
       top_n=3,
       aggregation_method='pairwise',
       p_value_aggregation_method='max'
   )
   print(f"Top 3 features (pairwise, max p-value): {top_3_features_max_agg}")

Arguments
---------

- **df** (``pd.DataFrame``):  
  The input DataFrame containing feature columns and the binary target column.

- **x_cols** (``List[str]``):  
  A list of column names in `df` representing the features you want to evaluate.

- **y_var** (``str``):  
  The name of the column in `df` representing the binary target variable (0/1 or similar).

- **top_p** (``float``, optional):  
  If provided, only features with a K-S test p-value less than `top_p` will be selected.

- **top_n** (``int``, optional):  
  If provided, the top `n` features with the lowest p-values will be selected.

  .. note::

     You can use either ``top_p`` or ``top_n``, or both. If both are given, the function will apply ``top_p`` first,
     and then take the top ``n`` from that filtered list.
    

License
-------

MIT License

Author
------

V Subrahmanya Raghu Ram Kishore Parupudi
Email: pvsrrkishore@gmail.com



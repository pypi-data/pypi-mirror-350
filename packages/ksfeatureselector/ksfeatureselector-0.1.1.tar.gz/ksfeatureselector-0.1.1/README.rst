KSFeatureSelector
=================

**KSFeatureSelector** is a lightweight Python package for selecting the most discriminatory features 
in a binary classification problem using the Kolmogorov–Smirnov (K-S) test.

Features
--------

- Uses the K-S test to rank features by their ability to separate classes.
- Supports filtering features by:
  - A maximum p-value threshold.
  - A fixed number of top features.
- Numpy-style docstrings and validations.
- Pure Python using `pandas` and `scipy`.

Installation
------------

From PyPI:

.. code-block:: bash

   pip install ksfeatureselector

Local installation:

.. code-block:: bash

   pip install .

Usage
-----

.. code-block:: python

   from ksfeatureselector import select_ks_features

   x_cols = ['feature1', 'feature2', 'feature3']
   y_var = 'target'

   # Select top features based on p-value or top-n count
   select_ks_features(df, x_cols, y_var, top_p=0.05)
   # or
   select_ks_features(df, x_cols, y_var, top_n=5)


Arguments
---------

- **df** (`pd.DataFrame`):  
  The input DataFrame containing feature columns and a binary target column.

- **x_cols** (`List[str]`):  
  List of column names in `df` to be considered as features.

- **y_var** (`str`):  
  The name of the target column in `df`. Must be binary (e.g., 0/1 or True/False).

- **top_p** (`float`, optional):  
  Select features whose K-S test p-value is less than this threshold. Use this for statistical significance filtering.

- **top_n** (`int`, optional):  
  Select the top N features with the smallest p-values, ranked by their ability to distinguish between the two classes.

Returns
-------

- **List[str]**:  
  A list of selected feature names based on the K-S test ranking.

License
-------

MIT License

Author
------

V Subrahmanya Raghu Ram Kishore Parupudi  
Email: pvsrrkishore@gmail.com

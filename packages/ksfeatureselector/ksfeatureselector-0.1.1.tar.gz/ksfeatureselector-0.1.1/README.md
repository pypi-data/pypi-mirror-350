## KSFeatureSelector

`KSFeatureSelector` is a lightweight Python package for selecting the most discriminatory features 
in a binary classification problem using the Kolmogorov–Smirnov (K-S) test.

## Features

- Uses the K-S test to rank features by their ability to separate classes.
- Supports filtering features by:
  - A maximum p-value threshold.
  - A fixed number of top features.
- Easy-to-read, numpy-style docstrings and validations.
- Pure Python + `pandas` + `scipy`.

## Installation

- bash
    pip install ksfeatureselector

- local
    pip install .

## Usage

    from ksfeatureselector import select_ks_features

    # Your DataFrame `df` should contain numerical features and a binary target column
    x_cols = ['feature1', 'feature2', 'feature3']
    y_var = 'target'

    # Select top features based on p-value or top-n count
    select_ks_features(df, x_cols, y_var, top_p=0.05)
    # or
    select_ks_features(df, x_cols, y_var, top_n=5)

## License
    - MIT License

## Author
    -- V Subrahmanya Raghu Ram Kishore Parupudi
    -- email: pvsrrkishore@gmail.com





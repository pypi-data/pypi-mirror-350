import pytest
import pandas as pd
import numpy as np
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ksfeatureselector.core import KSFeatureSelector, sort_tuple, select_ks_features

# Sample data generation
def create_test_df():
    np.random.seed(42)
    df = pd.DataFrame({
        'feature1': np.random.normal(0, 1, 100),
        'feature2': np.random.normal(1, 1, 100),
        'feature3': np.random.normal(2, 1, 100),
        'target': np.random.choice([0, 1], size=100)
    })
    return df

def test_sort_tuple():
    tuples = [('a', 0.2), ('b', 0.1), ('c', 0.3)]
    sorted_tuples = sort_tuple(tuples.copy())
    assert sorted_tuples == [('b', 0.1), ('a', 0.2), ('c', 0.3)]

    sorted_tuples_reverse = sort_tuple(tuples.copy(), reverse=True)
    assert sorted_tuples_reverse == [('c', 0.3), ('a', 0.2), ('b', 0.1)]

def test_invalid_sort_tuple():
    with pytest.raises(AssertionError):
        sort_tuple('not a list')

    with pytest.raises(AssertionError):
        sort_tuple([(1, 0.5)])

    with pytest.raises(AssertionError):
        sort_tuple([('a', -0.1)])

def test_fit_transform_pairwise():
    df = create_test_df()
    selector = KSFeatureSelector(aggregation_method='pairwise', p_value_aggregation_method='fisher')
    selector.fit(df, ['feature1', 'feature2', 'feature3'], 'target')
    features = selector.transform(top_n=2)
    assert isinstance(features, list)
    assert len(features) == 2

def test_fit_transform_one_vs_rest():
    df = create_test_df()
    selector = KSFeatureSelector(aggregation_method='one-vs-rest', p_value_aggregation_method='min')
    selector.fit(df, ['feature1', 'feature2', 'feature3'], 'target')
    features = selector.transform(top_p=0.9)
    assert isinstance(features, list)


def test_invalid_transform_before_fit():
    selector = KSFeatureSelector()
    with pytest.raises(ValueError):
        selector.transform(top_n=2)


def test_get_feature_p_values():
    df = create_test_df()
    selector = KSFeatureSelector()
    selector.fit(df, ['feature1', 'feature2'], 'target')
    p_vals = selector.get_feature_p_values()
    assert isinstance(p_vals, list)
    assert all(isinstance(t, tuple) and len(t) == 2 for t in p_vals)

def test_select_ks_features_wrapper():
    df = create_test_df()
    features = select_ks_features(df, ['feature1', 'feature2', 'feature3'], 'target', top_n=2)
    assert isinstance(features, list)
    assert len(features) == 2


def test_invalid_inputs():
    df = create_test_df()
    df['target'] = 'a'  # Make target constant (invalid)
    selector = KSFeatureSelector()
    with pytest.raises(AssertionError):
        selector.fit(df, ['feature1'], 'target')
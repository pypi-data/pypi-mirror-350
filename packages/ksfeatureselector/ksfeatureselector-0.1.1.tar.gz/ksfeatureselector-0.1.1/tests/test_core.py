import pytest
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ksfeatureselector.core import select_ks_features, sort_tuple

def test_sort_tuple_basic():
    input_data = [('a', 0.3), ('b', 0.1), ('c', 0.5)]
    sorted_data = sort_tuple(input_data.copy())
    assert sorted_data == [('b', 0.1), ('a', 0.3), ('c', 0.5)]

def test_sort_tuple_reverse():
    input_data = [('a', 0.3), ('b', 0.1), ('c', 0.5)]
    sorted_data = sort_tuple(input_data.copy(), rev=True)
    assert sorted_data == [('c', 0.5), ('a', 0.3), ('b', 0.1)]

def test_select_ks_feat_basic():
    df = pd.DataFrame({
        'f1': [1, 2, 3, 4, 3, 6],
        'f2': [6, 5, 4, 3, 2, 1],
        'event': [0, 0, 0, 1, 1, 1]
    })
    result = select_ks_features(df, ['f1', 'f2'], 'event', top_n=1)
    assert isinstance(result, list)
    assert len(result) == 1

    result = select_ks_features(df, ['f1', 'f2'], 'event', top_p=0.4)
    assert isinstance(result, list)
    assert len(result) == 1
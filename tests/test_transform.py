import pytest
import sys
import os
import pandas as pd
from unittest.mock import patch
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.transform import transform

sample_products = [
    {
        "title": "T-shirt 1",
        "price": "50",
        "rating": "4.5",
        "colors": "3 Colors",
        "size": "M",
        "gender": "Women"
    },
    {
        "title": "T-shirt 2",
        "price": "30",
        "rating": "Not Rated",
        "colors": "2 Colors",
        "size": "L",
        "gender": "Men"
    },
    {
        "title": "Unknown Product",
        "price": "",
        "rating": "Invalid Rating",
        "colors": "0 Colors",
        "size": "XL",
        "gender": "Unisex"
    }
]


@patch("utils.transform.logging")
def test_transform(mock_logging):
    
    result_df = transform(sample_products)

    
    assert isinstance(result_df, pd.DataFrame)
    
    
    assert len(result_df) == 1  

    
    transformed_product = result_df.iloc[0]
    assert transformed_product["Title"] == "T-shirt 1"
    assert transformed_product["Price"] == 50 * 16000
    assert transformed_product["Rating"] == 4.5
    assert transformed_product["Colors"] == 3
    assert transformed_product["Size"] == "M"
    assert transformed_product["Gender"] == "Women"
    
    
    mock_logging.warning.assert_any_call("Skipping product at index 1: Invalid data detected.")
    mock_logging.warning.assert_any_call("Skipping product at index 2: Invalid data detected.")
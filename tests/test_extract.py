import sys
import os
from unittest.mock import patch, Mock
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.extract import extract_products

@patch("utils.extract.requests.get")
def test_extract_products(mock_get):
    # Dummy HTML untuk page pertama (ada produk)
    dummy_html_page1 = '''
    <html>
        <body>
            <div class="collection-card">
                <h3 class="product-title">T-shirt 2</h3>
                <span class="price">$102.15</span>
                <p>Rating: ⭐ 3.9 / 5</p>
                <p>3 Colors</p>
                <p>Size: M</p>
                <p>Gender: Women</p>
            </div>
        </body>
    </html>
    '''

    # Dummy HTML untuk page kedua (kosong)
    dummy_html_page2 = '''
    <html>
        <body>
            <p>No products here</p>
        </body>
    </html>
    '''

    
    mock_get.side_effect = [
        Mock(status_code=200, text=dummy_html_page1),
        Mock(status_code=200, text=dummy_html_page2)
    ]

    expected_output = [{
        "title": "T-shirt 2",
        "price": "102.15",
        "rating": "3.9",
        "colors": "3",
        "size": "M",
        "gender": "Women"
    }]

    results = extract_products()

    assert isinstance(results, list)
    assert len(results) == 1
    assert results == expected_output

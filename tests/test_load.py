import sys
import os
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.load import load_to_csv, load_to_gsheet, load_to_postgres

@pytest.fixture
def sample_df():
    return pd.DataFrame([{
        "Title": "T-shirt",
        "Price": 100000,
        "Rating": 4.5,
        "Colors": 3,
        "Size": "M",
        "Gender": "Unisex",
        "Timestamp": "2025-04-24 10:00:00"
    }])

def test_load_to_csv_creates_file(sample_df):
    test_filename = "test_products.csv"
    load_to_csv(sample_df, test_filename)

    assert os.path.exists(test_filename)
    df_loaded = pd.read_csv(test_filename)
    assert df_loaded.equals(sample_df)

    os.remove(test_filename)

@patch("utils.load.ServiceAccountCredentials")
@patch("utils.load.gspread")
def test_load_to_gsheet_mocked(mock_gspread, mock_creds, sample_df):
    mock_client = MagicMock()
    mock_spreadsheet = MagicMock()
    mock_worksheet = MagicMock()

    mock_gspread.authorize.return_value = mock_client
    mock_client.create.return_value = mock_spreadsheet
    mock_spreadsheet.get_worksheet.return_value = mock_worksheet
    mock_spreadsheet.sheet1 = mock_worksheet

    load_to_gsheet(sample_df)

    mock_gspread.authorize.assert_called_once()
    mock_client.create.assert_called_once_with("ETL Products")
    mock_worksheet.update.assert_called_once()

@patch("utils.load.psycopg2.connect")
def test_load_to_postgres_mocked(mock_connect, sample_df):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    load_to_postgres(sample_df)

    mock_connect.assert_called_once()
    mock_cursor.execute.assert_called()  # at least called once
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

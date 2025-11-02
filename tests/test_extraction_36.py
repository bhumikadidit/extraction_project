import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from table_tools.pdf_extractor.extraction_36 import load_and_clean_table, save_table

@pytest.fixture
def sample_df():
    return pd.DataFrame([['Province', 'Girls', 'Boys'], ['Data1', 1, 2]])

def test_load_and_clean_table(sample_df):
    with patch('camelot.read_pdf') as mock_read:
        mock_table = MagicMock()
        mock_table.df = sample_df
        mock_read.return_value = [mock_table]
        result = load_and_clean_table("fake.pdf")
        assert 'Province' in result.columns

def test_save_table(sample_df, tmp_path):
    output_file = tmp_path / "test.csv"
    save_table(sample_df, str(output_file))
    assert output_file.exists()
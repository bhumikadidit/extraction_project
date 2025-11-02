import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from table_tools.pdf_extractor.extraction_35 import load_pdf_table, clean_table, save_table

@pytest.fixture
def sample_df():
    return pd.DataFrame([['A', 'B', 'C', 'D'], [1, 2, 3, 4], ['', '', '', '']])

def test_load_pdf_table_success(sample_df):
    with patch('camelot.read_pdf') as mock_read:
        mock_table = MagicMock()
        mock_table.df = sample_df
        mock_read.return_value = [mock_table]
        result = load_pdf_table("fake.pdf")
        assert result.equals(sample_df)

def test_load_pdf_table_no_tables():
    with patch('camelot.read_pdf', return_value=[]):
        with pytest.raises(ValueError):
            load_pdf_table("fake.pdf")

def test_clean_table(sample_df):
    result = clean_table(sample_df)
    assert len(result) == 1  # Only valid row

def test_clean_table_no_valid_rows():
    df = pd.DataFrame([['', '', '', '']])
    with pytest.raises(ValueError):
        clean_table(df)

def test_save_table(sample_df, tmp_path):
    output_file = tmp_path / "test.csv"
    save_table(sample_df, str(output_file))
    assert output_file.exists()
import pytest
from unittest.mock import MagicMock,patch
from table_tools.pdf_extractor.tabula_extraction import download_pdf, extract_tables_to_csv

def test_download_pdf(tmp_path):
    fake_url = "http://fake.com/pdf.pdf"
    local_path = tmp_path / "test.pdf"
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.content = b"fake pdf"
        mock_get.return_value = mock_response
        download_pdf(fake_url, str(local_path))
        assert local_path.exists()

def test_extract_tables_to_csv(tmp_path):
    pdf_path = tmp_path / "test.pdf"
    pdf_path.write_text("fake")
    output_csv = tmp_path / "test.csv"
    with patch('tabula.convert_into') as mock_convert:
        extract_tables_to_csv(str(pdf_path), str(output_csv))
        mock_convert.assert_called_once()
import pytest
import os
import pandas as pd
from table_tools.webscraper.pokhara_scraper import scrape_news
from table_tools.pdf_extractor.extraction_35 import load_pdf_table, clean_table
import tempfile
import requests

def test_scrape_news_real_data():
    """Check if scrape_news processed real data from the website."""
    news_data = scrape_news()
    
    # Ensure we got data
    assert len(news_data) > 0, "No news data scraped"
    
    # Check first item for real content (not defaults)
    title, date = news_data[0]
    assert title != 'No title', "Title is default, not real"
    assert date != 'No date', "Date is default, not real"
    
def test_pdf_extractor_real_data():
    # Download or generate the PDF freshly
    pdf_url = "https://example.com/Flash 1 Report 2081 (2024)_hzq1zgz.pdf"  
    response = requests.get(pdf_url)
    assert response.status_code == 200, "Failed to download PDF"
    
    # Save to a temporary or unique path to avoid conflicts
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(response.content)
        pdf_path = temp_file.name

    assert os.path.exists(pdf_path), "PDF file not found"
    
    # Load and clean
    raw_df = load_pdf_table(pdf_path, page="35")
    cleaned_df = clean_table(raw_df)
    
    # Ensure we got data
    assert not cleaned_df.empty, "No table data extracted"
    
    # Check for real content (not all empty)
    assert cleaned_df.shape[0] > 0, "No rows in cleaned table"
    assert cleaned_df.shape[1] >= 4, "Not enough columns"
    
    # Check first row has some non-empty cells
    first_row = cleaned_df.iloc[0]
    has_data = any(str(cell).strip() for cell in first_row)
    assert has_data, "First row has no real data"

    # Clean up after the test
    os.unlink(pdf_path)

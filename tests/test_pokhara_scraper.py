import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from table_tools.webscraper.pokhara_scraper import scrape_news, scrape_notices_last_2years, save_to_csv

@pytest.fixture
def fake_html():
    """Fixture for sample HTML to reuse in tests."""
    return '<div class="views-row"><span property="dc:title" content="Test Title"></span><span class="date">2023-01-01</span><div class="content">Test Content</div><a href="test-link"></a></div>'


def test_scrape_news(fake_html):
    """Test scraping news items from HTML."""
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.text = fake_html
        mock_get.return_value = mock_response
        result = scrape_news()
        # Check that we got one item
        assert len(result) == 1
        # Check the title (first element in the list)
        assert result[0][0] == "Test Title"
        # Check other fields (date, content, link)
        assert result[0][1] == "2023-01-01"
        assert result[0][2] == "Test Content"
        assert result[0][3] == "test-link"

def test_scrape_news_error():
    """Test error handling when request fails."""
    with patch('requests.get', side_effect=Exception("Network error")):
        with pytest.raises(RuntimeError, match="Error scraping news"):
            scrape_news()

def test_scrape_notices_last_2years():
    """Test scraping notices from last 2 years."""
    # Updated fake HTML: Full HTML document to match scraper expectations, with a more recent date to ensure it's within 2 years
    fake_html = '<html><body><div class="node-article"><h2><a>Test Notice</a></h2><span property="dc:date dc:created">Thu, 10/01/2024 - 12:00</span></div></body></html>'
    with patch('requests.Session.get') as mock_get:
        mock_response = MagicMock()
        mock_response.content = fake_html.encode('utf-8')  # Set to bytes to match response.content
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        result = scrape_notices_last_2years(max_pages=1)  # Limit to 1 page for test
        # Should find the notice since date is within 2 years
        assert len(result) == 1
        assert result[0]['Title'] == "Test Notice"
        assert result[0]['Date'] == datetime(2024, 10, 1)

def test_scrape_notices_no_more_pages():
    """Test stopping when no more pages."""
    with patch('requests.Session.get') as mock_get:
        mock_response = MagicMock()
        mock_response.content = '<html></html>'  # No rows
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        result = scrape_notices_last_2years(max_pages=1)
        assert len(result) == 0


def test_save_scraped_data_to_csv(tmp_path, fake_html):
    """Test if scraped data is saved to CSV."""
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.text = fake_html
        mock_get.return_value = mock_response
        
        # Scrape data
        scraped_data = scrape_news()
        
        # Save to CSV
        output_file = tmp_path / "news_data.csv"
        headers = ['Title', 'Date', 'Content', 'Link']
        save_to_csv(scraped_data, str(output_file), headers)
        
        # Check if file was saved
        assert output_file.exists()
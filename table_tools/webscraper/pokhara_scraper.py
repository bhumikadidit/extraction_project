import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import csv 

def scrape_pokhara_news(url="https://pokharamun.gov.np/news-notices"):
    """Scrape general news from Pokhara municipality"""
    # Fetch the webpage
    response = requests.get(url)
    response.encoding = 'utf-8'  # Handle Nepali characters

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all news items (adjust selector based on actual HTML)
    news_items = soup.find_all('div', class_='views-row')

    # Prepare data list
    news_data = []

    # Extract information from each news item
    for item in news_items:
        try:
            # Extract title
            title_span = item.find('span', property='dc:title')
            title = title_span['content'] if title_span else 'No title'
        
            # Extract date (adjust selector based on actual HTML)
            date_span = item.find('span', class_='date')
            date = date_span.text.strip() if date_span else 'No date'
        
            # Extract content (adjust selector based on actual HTML)
            content_div = item.find('div', class_='content')
            content = content_div.text.strip() if content_div else 'No content'
        
            # Extract link
            link_tag = item.find('a')
            link = link_tag['href'] if link_tag else 'No link'
        
            # Add to our data list
            news_data.append([title, date, content, link])
        
        except Exception as e:
            print(f"Error processing item: {e}")
            continue

    # Save to CSV file
    with open('news_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['Title', 'Date', 'Content', 'Link'])
        # Write data
        writer.writerows(news_data)

    print(f"Successfully scraped {len(news_data)} news items")
    print("Data saved to news_data.csv")

    # Display first few items
    print("\nFirst 3 items:")
    for i, (title, date, content, link) in enumerate(news_data[:3]):
        print(f"\n{i+1}. {title}")
        print(f"   Date: {date}")
        print(f"   Content: {content[:50]}...")
        print(f"   Link: {link}") 

        pass






def scrape_pokhara_notices_last_2years(base_url="https://pokharamun.gov.np/news-notices", max_pages=100):
    """Scrape notices from last 2 years"""
    MAX_PAGES = 100  # Stop if no more pages
    DELAY = 1  # Seconds between requests
    OUTPUT_FILE = "pokhara_mun_notices_last_2yrs.csv"

    def parse_date(date_str):
        """Parse date like 'Thu, 09/27/2018 - 15:44' to 'YYYY-MM-DD'."""
        if not date_str:
            return None
        try:
            # Extract MM/DD/YYYY part
            date_part = date_str.split(',')[1].strip().split(' - ')[0].strip()
            parsed = datetime.strptime(date_part, '%m/%d/%Y')
            return parsed
        except (ValueError, IndexError):
            return None

    def scrape_notices():
        all_notices = []
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})

        for page in range(MAX_PAGES):
            url = f"{base_url}?page={page}"
            print(f"Scraping page {page + 1}...")

            try:
                response = session.get(url, timeout=30)
                response.raise_for_status()
                response.encoding = 'utf-8'  # UTF-8 for Nepali
                soup = BeautifulSoup(response.content, 'lxml')

                # Find notice rows (class: node-article)
                rows = soup.find_all('div', class_='node-article')
                if not rows:
                    print("No more notices. Stopping.")
                    break

                for row in rows:
                    # Title: Primary from h2 a (visible text); fallback to dc:title content
                    title = None
                    title_elem = row.find('h2')
                    if title_elem:
                        title_link = title_elem.find('a')
                        if title_link:
                            title = title_link.text.strip()  # Direct text (handles Nepali)
                    # if not title:
                    #     # Fallback: dc:title content (hidden RDF meta)
                    #     dc_title = row.find('span', {'property': 'dc:title'})
                    #     if dc_title:
                    #         title = dc_title.get('content', '').strip()

                    # Date: From dc:date dc:created span
                    date_elem = row.find('span', {'property': 'dc:date dc:created'})
                    date_str = date_elem.text.strip() if date_elem else None
                    pub_date = parse_date(date_str)

                    # Only add if title and valid date
                    if title and pub_date:
                        all_notices.append({'Title': title, 'Date': pub_date})

                print(f"Page {page + 1}: Found {len(rows)} rows, added {len(all_notices) - (len(all_notices) - len(rows))} notices so far.")
            except requests.RequestException as e:
                print(f"Error on page {page + 1}: {e}. Skipping.")
                break

            time.sleep(DELAY)

        return all_notices

    def filter_last_two_years(notices):
        """Filter to notices from past 2 years."""
        cutoff = datetime.now() - timedelta(days=730)  # 2 years approx.
        filtered = []
        for notice in notices:
            pub_date = notice['Date']
            if pub_date >= cutoff:
                filtered.append(notice)
        return filtered

    def save_to_csv(notices, filename):
        """Save to UTF-8 CSV."""
        if notices:
            df = pd.DataFrame(notices)
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"Saved {len(notices)} notices to {filename}")
        else:
            print("No notices in last 2 years.")

    if __name__ == "__main__":
        # Scrape
        all_notices = scrape_notices()
        print(f"Total scraped: {len(all_notices)}")

        # Filter to last 2 years
        filtered_notices = filter_last_two_years(all_notices)
        print(f"Filtered (last 2 years): {len(filtered_notices)}")

        # Save
        save_to_csv(filtered_notices, OUTPUT_FILE)
        pass





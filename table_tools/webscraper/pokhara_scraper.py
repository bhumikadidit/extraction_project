import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import csv

def scrape_news(url="https://pokharamun.gov.np/news-notices"):
    """Scrape news items."""
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = soup.find_all('div', class_='views-row')
        news_data = []
        for item in news_items:
            title = item.find('span', property='dc:title')
            title = title['content'] if title else 'No title'
            date = item.find('span', class_='date')
            date = date.text.strip() if date else 'No date'
            content = item.find('div', class_='content')
            content = content.text.strip() if content else 'No content'
            link = item.find('a')
            link = link['href'] if link else 'No link'
            news_data.append([title, date, content, link])
        return news_data
    except Exception as e:
        raise RuntimeError(f"Error scraping news: {e}")

def scrape_notices_last_2years(base_url="https://pokharamun.gov.np/news-notices", max_pages=100):
    """Scrape notices from last 2 years."""
    cutoff = datetime.now() - timedelta(days=730)
    all_notices = []
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    
    for page in range(max_pages):
        url = f"{base_url}?page={page}"
        try:
            response = session.get(url, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser')
            rows = soup.find_all('div', class_='node-article')
            if not rows:
                break
            for row in rows:
                title_elem = row.find('h2')
                title = title_elem.find('a').text.strip() if title_elem and title_elem.find('a') else None
                date_elem = row.find('span', {'property': 'dc:date dc:created'})
                date_str = date_elem.text.strip() if date_elem else None
                if date_str:
                    try:
                        date_part = date_str.split(',')[1].strip().split(' - ')[0].strip()
                        pub_date = datetime.strptime(date_part, '%m/%d/%Y')
                        if pub_date >= cutoff and title:
                            all_notices.append({'Title': title, 'Date': pub_date})
                    except ValueError:
                        continue
            time.sleep(1)
        except requests.RequestException:
            break
    return all_notices

def save_to_csv(data, filename, headers):
    """Save data to CSV."""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)

def main():
    # Scrape news
    news_data = scrape_news()
    save_to_csv(news_data, 'news_data.csv', ['Title', 'Date', 'Content', 'Link'])
    print(f"Scraped {len(news_data)} news items.")
    
    # Scrape notices
    notices = scrape_notices_last_2years()
    df = pd.DataFrame(notices)
    df.to_csv("pokhara_mun_notices_last_2yrs.csv", index=False, encoding='utf-8')
    print(f"Saved {len(notices)} notices.")

if __name__ == "__main__":
    main()
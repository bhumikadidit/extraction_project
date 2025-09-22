import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime, timedelta
import re
from urllib.parse import urljoin
import os

class MunicipalityScraperBS:
    def __init__(self, base_url="https://pokharamun.gov.np"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.data = []
    
    def get_page_url(self, page_num):
        """Generate URL for specific page number"""
        if page_num == 0:
            return f"{self.base_url}/news-notices"
        else:
            return f"{self.base_url}/news-notices?page={page_num}"
    
    def parse_date(self, date_string):
        """Parse date from various formats in the website"""
        try:
            # Remove "Submitted on: " prefix if present
            date_string = date_string.replace("Submitted on: ", "").strip()
            
            # Try multiple date formats
            formats = [
                "%a, %m/%d/%Y - %H:%M",  # Wed, 02/14/2018 - 10:15
                "%a, %m/%d/%Y - %H:%M",  # Thu, 02/22/2018 - 14:33
                "%Y-%m-%d"  # Fallback format
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_string, fmt)
                except ValueError:
                    continue
            
            # If none work, return current date
            return datetime.now()
        except:
            return datetime.now()
    
    def is_within_last_2_years(self, date_obj):
        """Check if date is within last 2 years"""
        two_years_ago = datetime.now() - timedelta(days=730)
        return date_obj >= two_years_ago
    
    def extract_notices_from_page(self, soup, page_url):
        """Extract all notices from a single page"""
        notices = []
        
        # Find all notice nodes
        notice_nodes = soup.find_all('div', class_=lambda x: x and 'node node-article node-teaser' in x)
        
        for node in notice_nodes:
            try:
                # Extract title
                title_elem = node.find('h2').find('a')
                title = title_elem.get_text(strip=True) if title_elem else "No Title"
                notice_url = urljoin(self.base_url, title_elem['href']) if title_elem else ""
                
                # Extract date
                date_elem = node.find('span', property='dc:date dc:created')
                date_text = date_elem.get_text(strip=True) if date_elem else ""
                published_date = self.parse_date(date_text)
                
                
                notice_data = {
                    'title': title,
                    'published_date': published_date,
                }
                
                notices.append(notice_data)
                
            except Exception as e:
                print(f"Error parsing notice: {e}")
                continue
        
        return notices
    
    def scrape_pages(self, max_pages=50):
        """Scrape multiple pages until we have 2 years of data or reach max pages"""
        all_notices = []
        
        for page_num in range(max_pages):
            try:
                url = self.get_page_url(page_num)
                print(f"Scraping page {page_num + 1}: {url}")
                
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                notices = self.extract_notices_from_page(soup, url)
                
                if not notices:
                    print("No notices found on page, stopping.")
                    break
                
                # Check if we've reached notices older than 2 years
                oldest_notice_date = min([notice['published_date'] for notice in notices])
                if not self.is_within_last_2_years(oldest_notice_date):
                    print("Reached notices older than 2 years, stopping.")
                    # Only keep notices from last 2 years
                    notices = [notice for notice in notices if self.is_within_last_2_years(notice['published_date'])]
                    all_notices.extend(notices)
                    break
                
                all_notices.extend(notices)
                print(f"Found {len(notices)} notices on page {page_num + 1}")
                
                # Check if there's a next page
                next_link = soup.find('li', class_='pager-next')
                if not next_link:
                    print("No more pages available.")
                    break
                
                time.sleep(1)  # Be respectful to the server
                
            except requests.RequestException as e:
                print(f"Error fetching page {page_num}: {e}")
                break
            except Exception as e:
                print(f"Error processing page {page_num}: {e}")
                break
        
        return all_notices
    
    def save_to_csv(self, notices, filename="municipality_notices.csv"):
        """Save notices to CSV file"""
        if not notices:
            print("No notices to save.")
            return
        
        # Flatten data for CSV
        flat_data = []
        for notice in notices:
            flat_notice = {
                'title': notice['title'],
                'published_date': notice['published_date'].strftime('%Y-%m-%d %H:%M:%S'),
            }
            
            
            flat_data.append(flat_notice)
        
        df = pd.DataFrame(flat_data)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Saved {len(notices)} notices to {filename}")
    
    def run(self):
        """Main method to run the scraper"""
        print("Starting municipality notices scraping...")
        notices = self.scrape_pages()
        
        if notices:
            # Sort by date (newest first)
            notices.sort(key=lambda x: x['published_date'], reverse=True)
            
            # Filter for last 2 years
            two_years_ago = datetime.now() - timedelta(days=730)
            recent_notices = [notice for notice in notices if notice['published_date'] >= two_years_ago]
            
            print(f"Total notices found: {len(notices)}")
            print(f"Notices from last 2 years: {len(recent_notices)}")
            
            # Save to CSV
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"pokhara_municipality_notices_{timestamp}.csv"
            self.save_to_csv(recent_notices, filename)
            
            return recent_notices
        else:
            print("No notices were scraped.")
            return []

# Usage
if __name__ == "__main__":
    scraper = MunicipalityScraperBS()
    notices = scraper.run()
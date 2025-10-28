#!/usr/bin/env python3
"""
Simple script to run Pokhara municipality web scraping.
Run this to scrape news and notices from the website.
"""

import sys
import os
import pandas as pd

# Add parent directory to Python path to import our tools
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from table_tools.webscraper.pokhara_scraper import (
    scrape_pokhara_news, 
    scrape_pokhara_notices_last_2years
)

def main():
    print("=== Pokhara Municipality Web Scraper ===")
    
    # Create output folder if it doesn't exist
    os.makedirs('data/processed/web_data', exist_ok=True)
    
    try:
        # Step 1: Scrape general news
        print("\n1. Scraping news from Pokhara municipality...")
        news_data = scrape_pokhara_news()
        
        # Save news data
        if news_data:
            df_news = pd.DataFrame(news_data, columns=['Title', 'Date', 'Content', 'Link'])
            df_news.to_csv('data/processed/web_data/news_data.csv', index=False, encoding='utf-8')
            print(f"Saved {len(news_data)} news items")
        
        # Step 2: Scrape notices from last 2 years
        print("\n2. Scraping notices from last 2 years...")
        notices_data = scrape_pokhara_notices_last_2years(max_pages=5)  # Limit pages for testing
        
        # Save notices data
        if notices_data:
            df_notices = pd.DataFrame(notices_data)
            df_notices.to_csv('data/processed/web_data/pokhara_mun_notices_last_2yrs.csv', 
                            index=False, encoding='utf-8')
            print(f"Saved {len(notices_data)} notices")
        
        # Show summary
        print("\n=== Summary ===")
        print(f"News items: {len(news_data) if news_data else 0}")
        print(f"Notices: {len(notices_data) if notices_data else 0}")
        print(f"Files saved in: data/processed/web_data/")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Check your internet connection")

if __name__ == "__main__":
    main()
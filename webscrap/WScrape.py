import requests
from bs4 import BeautifulSoup
import csv

# Set the URL of the news page
url = "https://pokharamun.gov.np/news-notices"

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
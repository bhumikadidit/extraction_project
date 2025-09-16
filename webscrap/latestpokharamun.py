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

# Prepare data list - only title and date
news_data = []

# Find all div elements with id starting with "node-"
node_divs = soup.find_all('div', id=lambda x: x and x.startswith('node-'))

# Function to safely print text with Unicode characters
def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        # If printing fails, encode with replacement
        safe_text = text.encode('utf-8', errors='replace').decode('utf-8')
        print(safe_text)

# Extract information from each node div
for div in node_divs:
    try:
        # Extract title from span with property "dc:title"
        title_span = div.find('span', property='dc:title')
        if not title_span:
            continue  # Skip if no title span found
            
        title = title_span.get('content', '').strip()
        if not title:
            continue  # Skip if title is empty
            
        # Extract date from the meta submitted section
        date_span = div.find('span', property='dc:date')
        if date_span:
            date = date_span.get('content', '').strip()
        else:
            # Alternative: look for date in text
            submitted_div = div.find('div', class_='meta submitted')
            if submitted_div:
                date_text = submitted_div.get_text()
                date = date_text.replace('Submitted on:', '').replace('"', '').strip()
            else:
                date = 'Date not found'
        
        # Add to our data list (only title and date)
        news_data.append([title, date])
        
        safe_print(f"Found: {title} | {date}")
        
    except Exception as e:
        safe_print(f"Error processing item: {str(e)}")
        continue

# Save to CSV file (this should work fine as we're using UTF-8 encoding)
with open('news_titles.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(['Title', 'Date'])
    # Write data
    writer.writerows(news_data)

safe_print(f"\nSuccessfully scraped {len(news_data)} news items")
safe_print("Data saved to news_titles.csv")

# Display all items using safe print
safe_print("\nAll scraped titles:")
for i, (title, date) in enumerate(news_data):
    safe_print(f"{i+1}. {title} | {date}")
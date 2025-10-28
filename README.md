Extraction Project
https://img.shields.io/badge/Python-3.7+-blue.svg
https://img.shields.io/badge/License-MIT-green.svg
https://img.shields.io/badge/Status-Active-brightgreen.svg

A Python project for web scraping Pokhara municipality data and extracting tables from PDF educational reports.

Project Overview
This project provides tools to:

Web Scrape news and notices from Pokhara Municipality website

Extract Tables from PDF educational reports (Flash Report 2081)

Organize Data in a structured format for analysis

Quick Start
Prerequisites
Python 3.7 or higher

pip (Python package manager)

Installation
Clone the repository

bash
git clone <your-repository-url>
cd extraction_project
Install dependencies

bash
pip install -r requirements.txt
Run the scripts

bash
# Run web scraping
python scripts/run_webscraping.py

# Run PDF extraction
python scripts/run_pdf_extraction.py
 Project Structure
text
extraction_project/
│
├──  LICENSE                    # MIT License
├──  requirements.txt           # Python dependencies
├──  .gitignore                 # Git ignore rules
├──  README.md                  # This file
│
├──  table_tools/               # Main package
│   ├── __init__.py
│   ├── webscraper/               # Web scraping module
│   │   ├── __init__.py
│   │   └── pokhara_scraper.py    # Pokhara municipality scraper
│   └── pdf_extractor/            # PDF extraction module
│       ├── __init__.py
│       ├── extraction_35.py      # Page 35 specific extraction
│       ├── extraction_36.py      # Page 36 specific extraction
│       └── tabula_extractor.py   # General PDF extraction
│
├──  scripts/                   # Execution scripts
│   ├── run_webscraping.py        # Run web scraping
│   └── run_pdf_extraction.py     # Run PDF extraction
│
└──  data/                      # Data organization
    ├── processed/                # Cleaned and processed data
    │   ├── web_data/             # Scraped web data
    │   └── extracted_tables/     # Extracted PDF tables
    ├── raw/                      # Original source files
    └── temp/                     # Temporary processing files


 Usage
Web Scraping
Extract news and notices from Pokhara Municipality:

bash
python scripts/run_webscraping.py
Output files:

data/processed/web_data/news_data.csv - General news

data/processed/web_data/pokhara_mun_notices_last_2yrs.csv - Recent notices

PDF Table Extraction
Extract tables from educational PDF reports:

bash
python scripts/run_pdf_extraction.py
Output files:

data/processed/extracted_tables/all_tables_raw.csv - All tables

data/processed/extracted_tables/extracted_table_35.csv - Page 35 tables

data/processed/extracted_tables/extracted_table_36.csv - Page 36 tables

Data Sources
Web Data
Pokhara Municipality: https://pokharamun.gov.np/news-notices

Data Types: News articles, public notices, announcements

Frequency: Regularly updated

PDF Reports
Flash Report 2081 (2024): Educational statistics report

Content: ECED data, enrollment statistics, educational indicators

Pages: Multi-page PDF with structured tables

Technical Details
Dependencies
beautifulsoup4 - HTML parsing for web scraping

requests - HTTP requests

pandas - Data manipulation and analysis

tabula-py - PDF table extraction

camelot-py - Alternative PDF extraction

Key Features
- Modular and reusable code structure

- Error handling and progress tracking

- UTF-8 encoding for Nepali text support

- Organized data output

- Simple command-line interface

Use Cases
Government Monitoring: Track municipality announcements and educational statistics

Research Analysis: Analyze educational trends and enrollment data

Data Journalism: Extract structured data for reporting

Academic Research: Study educational development indicators

Legal & Ethical Considerations
This project scrapes publicly available data

Respects website robots.txt and terms of service

Includes delays between requests to avoid server overload

Intended for educational and research purposes
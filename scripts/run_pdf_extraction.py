#!/usr/bin/env python3
"""
Simple script to extract tables from PDF files.
Run this to extract tables from the Flash Report PDF.
"""

import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from table_tools.pdf_extractor.tabula_extraction import extract_all_tables
from table_tools.pdf_extractor.extraction_35 import extract_page_35_tables
from table_tools.pdf_extractor.extraction_36 import extract_page_36_tables

def main():
    print("=== PDF Table Extractor ===")
    
    # Create output folders
    os.makedirs('data/processed/extracted_tables', exist_ok=True)
    
    # PDF file path
    pdf_path = "data/raw/Flash 1 Report 2081 (2024)_hzq1zgz.pdf"
    
    # Check if PDF exists
    if not os.path.exists(pdf_path):
        print(f"PDF file not found: {pdf_path}")
        print("Please make sure the PDF is in data/raw/ folder")
        return
    
    print(f"Using PDF: {os.path.basename(pdf_path)}")
    
    try:
        # Step 1: Extract all tables
        print("\n1. Extracting all tables from PDF...")
        extract_all_tables(pdf_path, "data/processed/extracted_tables")
        
        # Step 2: Extract specific pages
        print("\n2. Extracting tables from specific pages...")
        
        # Page 35 - ECED Learning Materials
        print("  Extracting page 35 (ECED Learning Materials)...")
        result_35 = extract_page_35_tables(pdf_path)
        if result_35:
            print(" Page 35 extraction completed")
        
        # Page 36 - Grade 1 Enrollment
        print("  Extracting page 36 (Grade 1 Enrollment)...")
        result_36 = extract_page_36_tables(pdf_path)
        if result_36:
            print("  Page 36 extraction completed")
        
        # Show results
        print("\n=== Extraction Complete ===")
        print("Generated files in data/processed/extracted_tables/:")
        
        # List all CSV files created
        output_files = [f for f in os.listdir('data/processed/extracted_tables') 
                       if f.endswith('.csv')]
        
        for file in output_files:
            file_path = os.path.join('data/processed/extracted_tables', file)
            file_size = os.path.getsize(file_path)
            print(f"  {file} ({file_size} bytes)")
            
    except Exception as e:
        print(f"Error during extraction: {e}")
        print("Make sure tabula-py is installed: pip install tabula-py")

if __name__ == "__main__":
    main()
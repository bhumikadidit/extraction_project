import tabula
import pandas as pd
import requests

def download_pdf(url, local_path):
    """Download PDF from URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(local_path, 'wb') as f:
            f.write(response.content)
    except requests.RequestException as e:
        raise RuntimeError(f"Error downloading PDF: {e}")

def extract_tables_to_csv(pdf_path, output_csv, pages='all'):
    """Extract tables from PDF to CSV."""
    try:
        tabula.convert_into(pdf_path, output_csv, output_format="csv", pages=pages)
    except Exception as e:
        raise RuntimeError(f"Error extracting tables: {e}")

def main(pdf_url="https://giwmscdnone.gov.np/media/pdf_upload/Flash%201%20Report%202081%20(2024)_hzq1zgz.pdf", 
         local_pdf="./../../data/raw/downloaded_file.pdf", 
         output_csv="./../../data/processed/extracted_tables/all_tables_raw.csv"):
    print("Downloading PDF...")
    download_pdf(pdf_url, local_pdf)
    print("Extracting tables...")
    extract_tables_to_csv(local_pdf, output_csv)
    print("Success! Tables saved.")

if __name__ == "__main__":
    main()
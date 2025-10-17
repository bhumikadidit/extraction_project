import tabula
import pandas as pd
import requests

# PDF URL
pdf_url = "https://giwmscdnone.gov.np/media/pdf_upload/Flash%201%20Report%202081%20(2024)_hzq1zgz.pdf"
local_pdf_path = "downloaded_file.pdf"

try:
    print("Downloading PDF...")
    # Download and save PDF locally
    response = requests.get(pdf_url)
    with open(local_pdf_path, 'wb') as f:
        f.write(response.content)
    
    print("Extracting tables...")
    
    # Use tabula on the local file
    tabula.convert_into(local_pdf_path, "all_tables.csv", output_format="csv", pages='all')
    
    print("Success! Tables saved to 'all_tables.csv'")
    
except Exception as e:
    print(f"Error: {e}")
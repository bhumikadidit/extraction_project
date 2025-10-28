import camelot
import pandas as pd

# Extract with Camelot
pdf_path = "data/raw/Flash 1 Report 2081 (2024)_hzq1zgz.pdf"
tables = camelot.read_pdf(pdf_path, pages="36", flavor='lattice')

# Get the table
df = tables[0].df
print(f"Raw table: {df.shape[1]} cols, {df.shape[0]} rows")

# Remove empty rows and columns
df_clean = df.dropna(how='all').dropna(axis=1, how='all')

# Find header rows
header_rows = []
for i in range(min(3, len(df_clean))):
    row_text = ' '.join(str(cell) for cell in df_clean.iloc[i])
    if any(keyword in row_text.lower() for keyword in ['girls', 'boys', 'total', 'enrolment', 'percent']):
        header_rows.append(i)

# If we found at least 2 header rows (main + sub headers)
if len(header_rows) >= 2:
    main_header_row = df_clean.iloc[header_rows[0]]
    sub_header_row = df_clean.iloc[header_rows[1]]
    
    # Create combined headers
    combined_headers = ['Province']  # First column is Province
    
    # Define the main header groups and their spans
    main_headers = [
        'New enrolment in Grade 1',
        'New enrolment in Grade 1 with ECED Experiences', 
        'Percent of Grade 1 students with ECED experience'
    ]
    
    # Each main header spans 3 sub-headers (Girls, Boys, Total)
    sub_headers_list = ['Girls', 'Boys', 'Total']
    
    # Create combined headers for each group
    header_index = 1  # Start from second column (after Province)
    for main_header in main_headers:
        for sub_header in sub_headers_list:
            if header_index < len(sub_header_row):
                combined_headers.append(f"{main_header}>{sub_header}")
                header_index += 1
    
    # Remove header rows from data and set new headers
    data_rows = df_clean.drop(header_rows)
    data_rows.columns = combined_headers
    final_df = data_rows
else:
    final_df = df_clean

# Save to CSV
final_df.to_csv("extracted_table_36.csv", index=False, encoding='utf-8')
print(f"Saved: extracted_table_36.csv")
print(final_df)
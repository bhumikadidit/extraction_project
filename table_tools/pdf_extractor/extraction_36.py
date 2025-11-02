import camelot
import pandas as pd

def load_and_clean_table(pdf_path, page="36"):
    """Load and clean table with headers."""
    try:
        tables = camelot.read_pdf(pdf_path, pages=page, flavor='lattice')
        df = tables[0].df
        df_clean = df.dropna(how='all').dropna(axis=1, how='all')
        
        # Find and combine headers
        header_rows = []
        for i in range(min(3, len(df_clean))):
            row_text = ' '.join(str(cell) for cell in df_clean.iloc[i])
            if any(keyword in row_text.lower() for keyword in ['girls', 'boys', 'total', 'enrolment', 'percent']):
                header_rows.append(i)
        
        if len(header_rows) >= 2:
            main_header_row = df_clean.iloc[header_rows[0]]
            sub_header_row = df_clean.iloc[header_rows[1]]
            combined_headers = ['Province']
            main_headers = [
                'New enrolment in Grade 1',
                'New enrolment in Grade 1 with ECED Experiences', 
                'Percent of Grade 1 students with ECED experience'
            ]
            sub_headers_list = ['Girls', 'Boys', 'Total']
            header_index = 1
            for main_header in main_headers:
                for sub_header in sub_headers_list:
                    if header_index < len(sub_header_row):
                        combined_headers.append(f"{main_header}>{sub_header}")
                        header_index += 1
            data_rows = df_clean.drop(header_rows)
            data_rows.columns = combined_headers
            return data_rows
        return df_clean
    except Exception as e:
        raise RuntimeError(f"Error processing table: {e}")

def save_table(df, output_file):
    """Save to CSV."""
    df.to_csv(output_file, index=False, encoding='utf-8')

def main(pdf_path="data/raw/Flash 1 Report 2081 (2024)_hzq1zgz.pdf", output_file="extracted_table_36.csv"):
    final_df = load_and_clean_table(pdf_path)
    print(f"Raw table: {final_df.shape[1]} cols, {final_df.shape[0]} rows")
    save_table(final_df, output_file)
    print(f"Saved: {output_file}")
    print(final_df)

if __name__ == "__main__":
    main()
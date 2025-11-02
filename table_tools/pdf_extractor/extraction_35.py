import camelot
import pandas as pd

def load_pdf_table(pdf_path, page="35"):
    """Load a table from a PDF using Camelot."""
    try:
        tables = camelot.read_pdf(pdf_path, pages=page, flavor='lattice')
        if len(tables) == 0:
            raise ValueError("No tables found in PDF.")
        return tables[0].df
    except Exception as e:
        raise RuntimeError(f"Error loading PDF: {e}")

def clean_table(df, expected_columns=4):
    """Clean the table by removing empties and filtering rows."""
    df_clean = df.dropna(how='all').dropna(axis=1, how='all')
    valid_rows = []
    for i in range(len(df_clean)):
        row = df_clean.iloc[i]
        filled_cells = sum(1 for cell in row if str(cell).strip() != '')
        if filled_cells >= expected_columns:
            valid_rows.append(row)
    if not valid_rows:
        raise ValueError("No valid rows after cleaning.")
    final_df = pd.DataFrame(valid_rows)
    # Use first row as header if valid
    if sum(1 for cell in final_df.iloc[0] if str(cell).strip() != '') >= expected_columns:
        header = final_df.iloc[0]
        data = final_df[1:]
        data.columns = header
        final_df = data
    return final_df

def save_table(df, output_file):
    """Save the DataFrame to CSV."""
    df.to_csv(output_file, index=False, encoding='utf-8')

def main(pdf_path="data/raw/Flash 1 Report 2081 (2024)_hzq1zgz.pdf", output_file="extracted_table_36.csv"):
    df = load_pdf_table(pdf_path)
    print(f"Raw table: {df.shape[1]} columns, {df.shape[0]} rows")
    final_df = clean_table(df)
    print(f"Final data: {final_df.shape[1]} cols, {final_df.shape[0]} rows")
    save_table(final_df, output_file)
    print(f"Saved: {output_file}")
    print(final_df.head())

if __name__ == "__main__":
    main()
import camelot
import pandas as pd

def main():
# STEP 1: Load with Camelot 
    pdf_path = "data/raw/Flash 1 Report 2081 (2024)_hzq1zgz.pdf"
    print("1. Loading PDF with Camelot...")
    tables = camelot.read_pdf(pdf_path, pages="36", flavor='lattice')

    if len(tables) == 0:
        print(" No tables found! Try different pages.")
        exit()

    table = tables[0]
    df = table.df

    print(f" Raw table: {df.shape[1]} columns, {df.shape[0]} rows")

    # STEP 2: Basic cleaning
    print("\n2. Basic cleaning...")

    # Remove completely empty rows and columns
    df_clean = df.dropna(how='all').dropna(axis=1, how='all')
    print(f"   After removing empty: {df_clean.shape[1]} cols, {df_clean.shape[0]} rows")

    # STEP 3: Set expected columns
    expected_columns = 4
    # STEP 4: Discard rows that don't match column requirement
    print(f"   Keeping only rows with {expected_columns}+ data cells...")

    valid_rows = []
    for i in range(len(df_clean)):
        row = df_clean.iloc[i]
    
        # Count non-empty cells in this row
        filled_cells = sum(1 for cell in row if str(cell).strip() != '')
    
        if filled_cells >= expected_columns:
            valid_rows.append(row)
            print(f"  Row {i}: {filled_cells} filled cells - KEEP")
        else:
            print(f"  Row {i}: {filled_cells} filled cells - DISCARD")

    # Create final dataframe
    if valid_rows:
        final_df = pd.DataFrame(valid_rows)
    
        # Use first row as header if it has good data
        if sum(1 for cell in final_df.iloc[0] if str(cell).strip() != '') >= expected_columns:
            print("\n   Using first row as header...")
            header = final_df.iloc[0]
            data = final_df[1:]
            data.columns = header
            final_df = data
    
        print(f"\n Final data: {final_df.shape[1]} cols, {final_df.shape[0]} rows")
    
        # STEP 5: Save results
        output_file = "extracted_table_36.csv"
        final_df.to_csv(output_file, index=False, encoding='utf-8')
        print(f" Saved: {output_file}")
    
        print("\n Final data preview:")
        print(final_df.head())
    
    else:
        print(" No rows matched the column requirement!")




if __name__ == "__main__":
    main()
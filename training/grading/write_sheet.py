import gspread
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
# Authenticate with the JSON key file
gc = gspread.service_account(filename=os.getenv("KEY_FILE_PATH"))

spreadsheet = gc.open_by_url(os.getenv("SHEET_URL"))

worksheet = spreadsheet.worksheet('Sheet5') # Input sheet name

def get_column_index(worksheet, column_name):
    header = worksheet.row_values(1)
    if column_name in header:
        return header.index(column_name) + 1  # Add 1 to convert 0-based index to 1-based index
    else:
        raise ValueError(f"Column '{column_name}' not found in the sheet")

# Column name
column_name = "CLASS12 (H/W)" 

data = [100, 90, 80, 50, 0, 0, 15, 70, 80, 90, 100, 100, 100, 100, 100, 90, 90, 0]

# Get the column index based on the column name
column_index = get_column_index(worksheet, column_name)
start_row = 2

# Update the column with data starting from the desired row
for i, value in enumerate(data):
    
    cell = worksheet.cell(start_row + i, column_index)
    worksheet.update_cell(cell.row, cell.col, value)

print("Successfully added!")

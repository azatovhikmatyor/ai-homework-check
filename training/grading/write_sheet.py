import gspread
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
# Authenticate with the JSON key file
gc = gspread.service_account(filename=os.getenv("KEY_FILE_PATH"))

spreadsheet = gc.open_by_url(os.getenv("SHEET_URL"))

worksheet = spreadsheet.worksheet('Sheet5')

def get_column_index(worksheet, column_name):
    header = worksheet.row_values(1)
    if column_name in header:
        return header.index(column_name) + 1  # Add 1 to convert 0-based index to 1-based index
    else:
        raise ValueError(f"Column '{column_name}' not found in the sheet")

# Function to find the row containing the specific name in a column
def find_row(worksheet, name, search_column_index):
    column_data = worksheet.col_values(search_column_index)  # Get all values in the column
    for row_index, cell_value in enumerate(column_data):
        if cell_value == name:
            return row_index + 1  # Add 1 to convert 0-based index to 1-based index
    raise ValueError(f"Name '{name}' not found in the column")

# Inputs
name_to_search = "Samandar"  
column_name_to_write = "CLASS12 (H/W)" 
value_to_write = 30  # Replace with the value to write

# Get the column index for the column name
target_column_index = get_column_index(worksheet, column_name_to_write)

# Get the column index where the name resides (e.g., "Name" column)
search_column_index = get_column_index(worksheet, "First Name")  

# # Find the row containing the name
target_row = find_row(worksheet, name_to_search, search_column_index)

worksheet.update_cell(target_row, target_column_index, value_to_write)

print("Successfully added!")

import gspread
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
# Authenticate with the JSON key file
gc = gspread.service_account(filename=os.getenv("KEY_FILE_PATH"))

# Open the Google Sheet by name or URL
spreadsheet = gc.open_by_url(os.getenv("SHEET_URL")) 

# Select the worksheet
worksheet = spreadsheet.worksheet('Git')

# Get all values from the sheet
data = worksheet.get_all_values()

# df = pd.DataFrame(data[1:], columns=data[0])
# print(df)
# df.to_csv("output.csv", index=False)

# print("Data successfully saved to output.csv")

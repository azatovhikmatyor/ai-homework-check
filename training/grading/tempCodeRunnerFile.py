
spreadsheet = gc.open_by_url(os.getenv("SHEET_URL"))

worksheet = spreadsheet.worksheet('Sheet5')

new_row = ["Value 1", "Value 2", "Value 3"]

worksheet.append_row(new_row)

print("Row successfully added!")

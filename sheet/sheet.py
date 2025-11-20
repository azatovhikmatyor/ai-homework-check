import gspread
import pandas as pd

from .base import Student
from utils import logger


class SpreadSheet:
    READ_TAB = "Single student"
    UPDATE_TAB = "Python scores" 

    def __init__(self, gs_keys_path: str, sheet_url: str, lesson_num: str):
        self.gc = gspread.service_account(filename=gs_keys_path)
        self.spreadsheet = self.gc.open_by_url(sheet_url)
        self.cl_name = 'SCORE' + lesson_num

        git_data = self.spreadsheet.worksheet(self.READ_TAB).get_all_values()
        self.read_tab_df = pd.DataFrame(git_data[1:], columns=git_data[0])
        self.read_tab_df = self.read_tab_df[
            (self.read_tab_df['Github link'].notna()) & (self.read_tab_df['Github link'] != '') &
            (self.read_tab_df['Chat Id'].notna()) & (self.read_tab_df['Chat Id'] != '')
        ]

        grades_table = self.spreadsheet.worksheet(self.UPDATE_TAB).get_all_values()
        self.update_tab_df = pd.DataFrame(grades_table[1:], columns=grades_table[0])

        if self.cl_name in self.update_tab_df.columns:
            self.update_tab_df[self.cl_name] = pd.to_numeric(self.update_tab_df[self.cl_name], errors='coerce').fillna(0).astype(int)
        

    def update_cell(self, id_number, score):
        df = self.update_tab_df

        if id_number not in df['ID'].values:
            raise ValueError(f"ID {id_number} not found in the DataFrame.")
        
        if self.cl_name not in df.columns:
            raise ValueError(f"Column '{self.cl_name}' not found in the DataFrame.")
        
        # Locate the row and check the existing value
        row_index = df.loc[df['ID'] == id_number].index[0]
        df.at[row_index, self.cl_name] = score
        
        return df
    
    def _get_column_letter(self, n):
        """Convert a column index (1-based) to a column letter."""
        result = ""
        while n > 0:
            n -= 1
            result = chr(n % 26 + 65) + result
            n //= 26
        return result
    
    def write_data_to_sheet(self, column_name):
        df = self.update_tab_df
        worksheet = self.spreadsheet.worksheet(self.UPDATE_TAB)

        # Check if the column exists in the DataFrame
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")
        
        # Extract the column to be updated
        col_index = df.columns.get_loc(column_name) + 1  # Convert to 1-based index (Google Sheets uses 1-based indexing)
        df[column_name] = pd.to_numeric(df[column_name], errors='coerce').fillna(0).astype(int)
        column_data = df[column_name].tolist()
        
        # Add the header (column name) and values
        column_letter = self._get_column_letter(col_index)  # Use helper function for proper column letters
        range_start = f"{column_letter}1"  # E.g., "C1" for the 3rd column
        range_end = f"{column_letter}{len(column_data) + 1}"  # E.g., "C{n}" for n rows
        range_to_update = f"{range_start}:{range_end}"
        
        # Debugging: Print the range
        print(f"Updating range: {range_to_update}")
        
        # Update the range in the sheet
        worksheet.update(range_to_update, [[column_name]] + [[value] for value in column_data])

        

    @property
    def students(self) -> list[Student]:
        df = self.update_tab_df
        student_list = []

        for _, row in self.read_tab_df.iterrows():
            # Check if the row exists in the DataFrame
            matched_rows = df.loc[df['ID'] == row['ID']]

            if not matched_rows.empty:
                row_index = matched_rows.index[0]
                current_value = df.at[row_index, self.cl_name]

                if current_value == '' or str(current_value) == '0':
                    print(row['ID'], row['First Name'], row['Last Name'])
                    student_list.append(
                        Student(
                            id=row['ID'],
                            fname=row['First Name'],
                            lname=row['Last Name'],
                            repo=row['Github link'],
                            chat_id=row['Chat Id'],
                        )
                    )
            else:
                print(f"ID {row['ID']} not found in the grades table.")

        return student_list



    def mark(self, student: Student, score: int) -> None:
        st_id = student.id

        self.update_cell(st_id, score)
        logger.info(f'{student} are given {score}')


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    load_dotenv(dotenv_path='.env')

    gs_keys_path = 'gs-keys.json'
    sheet_url = os.getenv('SHEET_URL')
    s1 = SpreadSheet(gs_keys_path, sheet_url, "2")
    
    for student in s1.students:
        s1.mark(student=student, score=50)

    s1.update_tab_df.to_excel("grade.xlsx", index=False)
    s1.write_data_to_sheet("SCORE2")




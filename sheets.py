import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets.readonly', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    return client.open("api_project").sheet1

def display_menu():
    print("\nOptions:")
    print("1. View all records")
    print("2. View a specific row")
    print("3. View a specific column")
    print("4. View a specific cell")
    print("5. Insert a new row")
    print("6. Update a row")
    print("7. Delete a row")
    print("0. Exit")

def view_all_records(sheet):
    data = sheet.get_all_records()
    pprint(data)

def view_specific_row(sheet, row_number):
    row = sheet.row_values(row_number)
    pprint(row)

def view_specific_column(sheet, col_number):
    col = sheet.col_values(col_number)
    pprint(col)

def view_specific_cell(sheet, row_number, col_number):
    cell_value = sheet.cell(row_number, col_number).value
    pprint(cell_value)

def insert_new_row(sheet):
    index = int(input("Enter the index where you want to insert the new row: "))
    values = input("Enter new row values separated by commas: ").split(',')
    sheet.insert_row(values, index)

def update_row(sheet):
    index = int(input("Enter the index of the row you want to update: "))
    values = input("Enter updated row values separated by commas: ").split(',')
    sheet.delete_row(index)
    sheet.insert_row(values, index)

def delete_row(sheet, row_number):
    sheet.delete_row(row_number)

def main():
    sheet = authenticate_google_sheets()

    while True:
        display_menu()
        choice = input("Enter your choice (0 to exit): ")

        if choice == '0':
            print("Exiting...")
            break
        elif choice == '1':
            view_all_records(sheet)
        elif choice == '2':
            row_number = int(input("Enter the row number to view: "))
            view_specific_row(sheet, row_number)
        elif choice == '3':
            col_number = int(input("Enter the column number to view: "))
            view_specific_column(sheet, col_number)
        elif choice == '4':
            row_number = int(input("Enter the row number: "))
            col_number = int(input("Enter the column number: "))
            view_specific_cell(sheet, row_number, col_number)
        elif choice == '5':
            insert_new_row(sheet)
            print("Row inserted successfully.")
        elif choice == '6':
            update_row(sheet)
            print("Row updated successfully.")
        elif choice == '7':
            row_number = int(input("Enter the row number to delete: "))
            delete_row(sheet, row_number)
            print("Row deleted successfully.")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

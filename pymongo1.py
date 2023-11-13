import pymongo
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

# Connect to MongoDB
conn_string = "mongodb+srv://fhmshahryer:5QmYnUN17c1d3RcZ@cluster0.soaa8or.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(conn_string)
myDB = client["test_db"]
collection_name = "my_table"
my_collection = myDB[collection_name]

def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets.readonly', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    return client.open("api_project").sheet1


def display_menu():
    print("\nOptions:")
    print("1. View all documents")
    print("2. View a document by name")
    print("3. Insert a new document")
    print("4. Update a document by name")
    print("5. Delete a document by name")
    print("6. Delete all documents")
    print("7. Copy all data from sheet and store in MongoDB")
    print("8. Copy specific row from sheet and store in MongoDB")
    print("0. Exit")


def view_all_documents():
    documents = list(my_collection.find())
    if not documents:
        print("No documents found.")
    else:
        print("All Documents:")
        for doc in documents:
            print(f"Name: {doc['name']}, Age: {doc['age']}, City: {doc['city']}")
        print()


def view_document_by_name(name):
    document = my_collection.find_one({"name": name})
    if document:
        print(f"Document with name '{name}':")
        print(f"Name: {document['name']}, Age: {document['age']}, City: {document['city']}")
    else:
        print(f"No document found with name '{name}'")


def insert_new_document():
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    city = input("Enter city: ")

    new_document = {
        "name": name,
        "age": age,
        "city": city
    }

    result = my_collection.insert_one(new_document)
    print("Document inserted with ID:", result.inserted_id)


def update_document_by_name(name):
    update_data = {}
    age = int(input("Enter new age: "))
    city = input("Enter new city: ")

    if age:
        update_data["age"] = age
    if city:
        update_data["city"] = city

    result = my_collection.update_one({"name": name}, {"$set": update_data})

    print("Matched Count:", result.matched_count)
    print("Modified Count:", result.modified_count)


def delete_document_by_name(name):
    result = my_collection.delete_one({"name": name})
    print("Deleted Count:", result.deleted_count)


def delete_all_documents():
    result = my_collection.delete_many({})
    print("Deleted Count:", result.deleted_count)


def copy_all_data_from_sheet(sheet):
    data = sheet.get_all_records()
    my_collection.insert_many(data)
    print("All data copied from sheet and stored in MongoDB.")


def copy_specific_row_from_sheet(sheet, row_name):
    try:
        cell = sheet.find(row_name)
        row_data = sheet.row_values(cell.row)
    except gspread.exceptions.CellNotFound:
        row_data = None

    if row_data:
        my_collection.insert_one(dict(zip(sheet.row_values(1), row_data)))
        print(f"Row '{row_name}' copied from sheet and stored in MongoDB.")
    else:
        print(f"Row '{row_name}' not found in the sheet.")



def main():
    while True:
        display_menu()
        choice = input("Enter your choice (0 to exit): ")

        if choice == '0':
            print("Exiting...")
            break
        elif choice == '1':
            view_all_documents()
        elif choice == '2':
            name = input("Enter the name to view: ")
            view_document_by_name(name)
        elif choice == '3':
            insert_new_document()
        elif choice == '4':
            name = input("Enter the name to update: ")
            update_document_by_name(name)
        elif choice == '5':
            name = input("Enter the name to delete: ")
            delete_document_by_name(name)
        elif choice == '6':
            confirm = input("Are you sure you want to delete all documents? (y/n): ").lower()
            if confirm == 'y':
                delete_all_documents()
                print("All documents deleted.")
            else:
                print("Operation canceled.")
        elif choice == '7':
            sheet = authenticate_google_sheets()
            copy_all_data_from_sheet(sheet)
        elif choice == '8':
            sheet = authenticate_google_sheets()
            row_identifier = input("Enter the name to copy: ")
            copy_specific_row_from_sheet(sheet, row_identifier)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
from tkinter import *
import sqlite3

LMS = sqlite3.connect('Library_Management_System.db')
cursor = LMS.cursor()

create_Borrower_sql = "CREATE TABLE IF NOT EXISTS BORROWER (Name VARCHAR(255) NOT NULL, Address VARCHAR(255) NOT NULL, Phone VARCHAR(20) NOT NULL)"
cursor.execute(create_Borrower_sql)
create_Borrower_sql = "CREATE TABLE IF NOT EXISTS PUBLISHER ( Publisher_Name VARCHAR(255) PRIMARY KEY NOT NULL, Phone VARCHAR(20), Address VARCHAR(255))"
cursor.execute(create_Borrower_sql)
create_Borrower_sql = "CREATE TABLE IF NOT EXISTS LIBRARY_BRANCH ( Branch_Id INTEGER PRIMARY KEY, Branch_Name VARCHAR(255) NOT NULL, Branch_Address VARCHAR(255) NOT NULL)"
cursor.execute(create_Borrower_sql)
create_Borrower_sql = "CREATE TABLE IF NOT EXISTS BOOK ( Book_Id INTEGER PRIMARY KEY, Title VARCHAR(255) NOT NULL, Publisher_Name VARCHAR(255) NOT NULL, FOREIGN KEY (Publisher_Name) REFERENCES PUBLISHER(Publisher_Name))"
cursor.execute(create_Borrower_sql)
create_Borrower_sql = "CREATE TABLE IF NOT EXISTS BOOK_LOANS ( Book_Id INTEGER NOT NULL, Branch_Id INTEGER NOT NULL, Card_No INTEGER NOT NULL, Date_Out DATE NOT NULL, Due_Date DATE NOT NULL, Returned_date DATE, PRIMARY KEY (Book_Id, Branch_Id, Card_No), FOREIGN KEY (Book_Id) REFERENCES BOOK(Book_Id), FOREIGN KEY (Branch_Id) REFERENCES LIBRARY_BRANCH(Branch_Id), FOREIGN KEY (Card_No) REFERENCES BORROWER(Card_No) )"
cursor.execute(create_Borrower_sql)
create_Borrower_sql = "CREATE TABLE IF NOT EXISTS BOOK_COPIES ( Book_Id INTEGER NOT NULL, Branch_Id INTEGER NOT NULL, No_Of_Copies INTEGER NOT NULL, PRIMARY KEY (Book_Id, Branch_Id), FOREIGN KEY (Book_Id) REFERENCES BOOK(Book_Id), FOREIGN KEY (Branch_Id) REFERENCES LIBRARY_BRANCH(Branch_Id) )"
cursor.execute(create_Borrower_sql)
create_Borrower_sql = "CREATE TABLE IF NOT EXISTS BOOK_AUTHORS ( Book_Id INTEGER NOT NULL, Author_Name VARCHAR(255) NOT NULL, PRIMARY KEY (Book_Id, Author_Name), FOREIGN KEY (Book_Id) REFERENCES BOOK(Book_Id) )"
cursor.execute(create_Borrower_sql)

LMS.commit()
LMS.close()

#TK window
root = Tk()
root.title('Library Management System')
root.geometry("400x400")

#testing adding a new borrower (CardNo not implemented yet)
def submit():
    submit_LMS = sqlite3.connect('Library_Management_System.db')
    submit_cursor = submit_LMS.cursor()
    submit_cursor.execute("INSERT INTO BORROWER VALUES (:Name, :Address, :Phone)",
        {
            'Name': B_Name.get(),
            'Address': B_Address.get(),
            'Phone': B_Phone.get(),
        })
    submit_LMS.commit()
    submit_LMS.close()

#textboxes
B_Name = Entry(root, width = 30)
B_Name.grid(row = 0, column = 1, padx = 20)
B_Name_Label = Label(root, text = 'Name: ')
B_Name_Label.grid(row = 0, column = 0)

B_Address = Entry(root, width = 30)
B_Address.grid(row = 1, column = 1)
B_Address_Label = Label(root, text = 'Address: ')
B_Address_Label.grid(row = 1, column = 0)

B_Phone = Entry(root, width = 30)
B_Phone.grid(row = 2, column = 1)
B_Phone_Label = Label(root, text = 'Phone: ')
B_Phone_Label.grid(row = 2, column = 0)

#Submit Button
submit_button = Button(root, text = 'Submit', command = submit)
submit_button.grid(row = 3, column = 0, columnspan = 2, pady = 10, padx = 10)

#Execute
root.mainloop()
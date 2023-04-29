from tkinter import *
import sqlite3
import random

LMS = sqlite3.connect('Library_Management_System.db')

root = Tk()
root.title('Library Management System')
root.geometry("400x400")

def generate_card_number():
    return random.randint(100000, 999999)

def checkout_book():
    checkout_window = Toplevel(root)
    checkout_window.title('Checkout Book')

    book_id_label = Label(checkout_window, text = 'Book ID:')
    book_id_label.grid(row = 0, column = 0)
    book_id_input = Entry(checkout_window)
    book_id_input.grid(row = 0, column = 1)


    branch_id_label = Label(checkout_window, text = 'Branch ID')
    branch_id_label.grid(row = 1, column = 0)
    branch_id_input = Entry(checkout_window)
    branch_id_input.grid(row = 1, column = 1)

    card_no_label = Label(checkout_window, text = 'Card Number:')
    card_no_label.grid(row = 2, column = 0)
    card_no_input = Entry(checkout_window)
    card_no_input.grid(row = 2, column = 1)


    def checkout():
        ck_cur = LMS.cursor()
        ck_cur.execute("insert into book_loans (Book_Id, Branch_Id, Card_No, Date_Out, Due_Date, Returned_date) values (?, ?, ?, date('now'), date('now', '+1 month'), NULL)", (book_id_input.get(), branch_id_input.get(), card_no_input.get()))
        ck_cur.execute("update book_copies set No_of_copies = No_of_copies - 1 where Book_Id = ? and Branch_Id = ?", (book_id_input.get(), branch_id_input.get()))
        LMS.commit()

        ck_cur.execute("select No_of_copies from book_copies where Book_Id = ? and Branch_Id = ?", (book_id_input.get(), branch_id_input.get()))
        copy_num = ck_cur.fetchone()[0]
        copies_label = Label(checkout_window, text = 'Number of Copies Left: {}'.format(copy_num))
        copies_label.grid(row = 4, column = 0, columnspan = 2)

    checkout_button = Button(checkout_window, text = 'Checkout', command = checkout)
    checkout_button.grid(row = 3, column = 0, columnspan = 2)

def add_borrower():
    add_borrower_window = Toplevel(root)
    add_borrower_window.title('Add Borrower')

    name_label = Label(add_borrower_window, text = 'Name:')
    name_label.grid(row = 0, column = 0)
    name_input = Entry(add_borrower_window)
    name_input.grid(row = 0, column = 1)

    address_label = Label(add_borrower_window, text = 'Address:')
    address_label.grid(row = 1, column = 0)
    address_input = Entry(add_borrower_window)
    address_input.grid(row = 1, column = 1)


    phone_label = Label(add_borrower_window, text = 'Phone:')
    phone_label.grid(row = 2, column = 0)
    phone_input = Entry(add_borrower_window)
    phone_input.grid(row = 2, column = 1)

    def add_borrower_submit():
        br_cur = LMS.cursor()
        br_cur.execute("insert into borrower (Name, Address, Phone) values (?, ?, ?)", (name_input.get(), address_input.get(), phone_input.get()))
        LMS.commit()

        card_no = generate_card_number()
        while br_cur.execute("select exists (select * from borrower where Card_No = ?)", (card_no,)).fetchone()[0]:
            card_no = generate_card_number()


        card_no_label = Label(add_borrower_window, text = 'Card Number: {}'.format(card_no))
        card_no_label.grid(row = 4, column = 0, columnspan = 2)
        
        br_cur.execute("update borrower set Card_no = ? where Name = ? and Address = ? and Phone = ?", (card_no, name_input.get(), address_input.get(), phone_input.get()))
        LMS.commit()

    add_borrower_button = Button(add_borrower_window, text = 'Add Borrower', command = add_borrower_submit)
    add_borrower_button.grid(row = 3, column = 0, columnspan = 2)

def add_book():
    add_book_window = Toplevel(root)
    add_book_window.title('Add Book')
    add_book_window.geometry('300x200')

    book_title_label = Label(add_book_window, text = 'Title:')
    book_title_label.grid(row = 0, column = 0)
    book_title_input = Entry(add_book_window)
    book_title_input.grid(row = 0, column = 1)

    publisher_label = Label(add_book_window, text = 'Publisher:')
    publisher_label.grid(row = 1, column = 0)
    publisher_input = Entry(add_book_window)
    publisher_input.grid(row = 1, column = 1)


    author_label = Label(add_book_window, text = 'Author:')
    author_label.grid(row = 2, column = 0)
    author_input = Entry(add_book_window)
    author_input.grid(row = 2, column = 1)

    def add_book_submit():
        ab_cur = LMS.cursor()

        publisher_name = publisher_input.get()
        ab_cur.execute("select * from publisher where Publisher_Name = ?", (publisher_name,))

        publisher_row = ab_cur.fetchone()

        if not publisher_row:
            return

        book_title = book_title_input.get()
        publisher_name = publisher_input.get()
        ab_cur.execute("insert into book (Title, Publisher_Name) values (?, ?)", (book_title, publisher_name))
        book_id = ab_cur.lastrowid


        # insert author into BOOK_AUTHORS table
        author_name = author_input.get()
        ab_cur.execute("insert into book_authors (Book_Id, Author_Name) values (?, ?)", (book_id, author_name))

        # insert copies into BOOK_COPIES table for all branches
        ab_cur.execute("select * from library_branch")
        branches = ab_cur.fetchall()

        for branch in branches:
            branch_id = branch[0]
            ab_cur.execute("insert into book_copies (Book_Id, Branch_Id, No_Of_Copies) values (?, ?, ?)", (book_id, branch_id, 5))

        LMS.commit()


    add_book_button = Button(add_book_window, text = 'Add Book', command = add_book_submit)
    add_book_button.grid(row = 3, column = 0, columnspan = 2)


def get_copies_loaned():
    add_book_window = Toplevel(root)
    add_book_window.title('Show Copies')
    add_book_window.geometry('400x400')

    book_title_label = Label(add_book_window, text = 'Book Title:')
    book_title_label.grid(row = 0, column = 0)
    book_title_input = Entry(add_book_window, width = 30)
    book_title_input.grid(row = 0, column = 1)

    def get_copies_submit(): 
        cl_cur = LMS.cursor()

        book_title = book_title_input.get()
        cl_cur.execute("select library_branch.Branch_Id, library_branch.Branch_Name, COUNT(book_loans.Book_Id) as Copies_Loaned_Out from book_loans join library_branch on book_loans.Branch_Id = library_branch.Branch_Id where book_loans.Book_Id in (select Book_Id from book where Title = ?) group by library_branch.Branch_Id", (book_title,))
        results = cl_cur.fetchall()

        # create a new window to display results
        results_window = Toplevel(root)
        results_window.title('Results')
        results_window.geometry("400x400")

        # create a label to display the results
        results_label = Label(results_window, text = "Copies Loaned Out per Branch for " + book_title + ":\n\nBranch ID\tBranch Name\tCopies Loaned Out\n")
        for result in results:
            results_label["text"] += str(result[0]) + "\t\t" + result[1] + "\t\t" + str(result[2]) + "\n"
        results_label.pack()

    get_loan_button = Button(add_book_window, text = 'Get Copies Loaned', command = get_copies_submit)
    get_loan_button.grid(row = 3, column = 0, columnspan = 2)



add_book_button = Button(root, text = 'Add Book', command = add_book)
add_book_button.pack()

add_borrower_button = Button(root, text = 'Add Borrower', command = add_borrower)
add_borrower_button.pack()

checkout_button = Button(root, text = 'Checkout Book', command = checkout_book)
checkout_button.pack()

get_copies_button = Button(root, text = "Get Copies Loaned", command=get_copies_loaned)
get_copies_button.pack()

root.mainloop()
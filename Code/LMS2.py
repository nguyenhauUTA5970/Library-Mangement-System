from tkinter import *
from tkinter.ttk import *
import sqlite3
import random

# Connecting with the database
LMS = sqlite3.connect('Library_Management_System.db')

# Creating the Main Menu
root = Tk()
root.title('Library Management System')
root.geometry("400x400")
root.configure(background='#F8F8F8')

# Function to generate random card number
def generate_card_number():
    return random.randint(100000, 999999)

# Function to checkout out a book
def checkout_book():

    # Creating a new window for the checkout function
    checkout_window = Toplevel(root)
    checkout_window.title('Checkout Book')
    checkout_window.geometry("400x200")
    checkout_window.configure(background='#F8F8F8')

    # Creating labels AND input fields
    book_id_label = Label(checkout_window, text='Book ID:', background='#F8F8F8')
    book_id_label.grid(row=0, column=0, padx=10, pady=10)
    book_id_input = Entry(checkout_window)
    book_id_input.grid(row=0, column=1, padx=10, pady=10)


    branch_id_label = Label(checkout_window, text='Branch ID:', background='#F8F8F8')
    branch_id_label.grid(row=1, column=0, padx=10, pady=10)
    branch_id_input = Entry(checkout_window)
    branch_id_input.grid(row=1, column=1, padx=10, pady=10)

    card_no_label = Label(checkout_window, text='Card Number:', background='#F8F8F8')
    card_no_label.grid(row=2, column=0, padx=10, pady=10)
    card_no_input = Entry(checkout_window)
    card_no_input.grid(row=2, column=1, padx=10, pady=10)

    # Function to handle the checkout button click
    def checkout():
        ck_cur = LMS.cursor()
        ck_cur.execute("INSERT INTO BOOK_LOANS (Book_Id, Branch_Id, Card_No, Date_Out, Due_Date, Returned_date) VALUES (?, ?, ?, date('now'), date('now', '+1 month'), NULL)", (book_id_input.get(), branch_id_input.get(), card_no_input.get()))
        ck_cur.execute("UPDATE BOOK_COPIES set No_of_copies = No_of_copies - 1 WHERE Book_Id = ? AND Branch_Id = ?", (book_id_input.get(), branch_id_input.get()))
        LMS.commit()

        ck_cur.execute("SELECT No_of_copies FROM BOOK_COPIES WHERE Book_Id = ? AND Branch_Id = ?", (book_id_input.get(), branch_id_input.get()))
        copy_num = ck_cur.fetchone()[0]
        copies_label = Label(checkout_window, text='Number of Copies Left: {}'.format(copy_num), background='#F8F8F8')
        copies_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    checkout_button = Button(checkout_window, text='Checkout', command=checkout)
    checkout_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    checkout_button.configure(style='TButton', foreground='#FFFFFF', background='#2196F3', font=('Arial', 12))

def add_borrower():
    add_borrower_window = Toplevel(root)
    add_borrower_window.title('Add Borrower')
    add_borrower_window.geometry('400x200')
    add_borrower_window.configure(background='#F8F

from tkinter import *
import sqlite3

LMS = sqlite3.connect('proj2p3.db')
cursor = LMS.cursor()

LMS.commit()
LMS.close()

#TK window
root = Tk()
root.title('Library Management System')
root.geometry("400x400")

def checkout():
    chwindow = Toplevel(root)
    chwindow.geometry("200x200")

    bq = sqlite3.connect('proj2p3.db')
    bq_cur = bq.cursor()
    bq_cur.execute("select title, book_id from book")
    records = bq_cur.fetchall()
    records = [record[0] for record in records]

    clicked = StringVar()
    drop = OptionMenu( chwindow , clicked , *records )
    drop.grid(row = 2, column = 0, columnspan = 2, pady = 10, padx = 10)

    

    def submitc():
        bq_cur.execute("select book_id from book where title = ?", (clicked.get(),))
        biq = (bq_cur.fetchall()[0][0])

        bq_cur.execute("select no_of_copies from book_copies where book_id = ?", (biq,))
        copynum = (bq_cur.fetchall()[0][0])
        if(copynum < 1):
            print("no books, -->needs to go on gui")
            return
        
        bq_cur.execute("select branch_id from book_copies where book_id = ?", (biq,))
        brid = (bq_cur.fetchall()[0][0])

        cardno = 989899
        
        bq_cur.execute("insert into book_loans (book_id, branch_id, card_no, Date_out, Due_date, Returned_date, Late) values (?, ?, ?, date('now'), date('now', '+1 month'), NULL, 0)", (biq, brid, cardno, ))
        bq_cur.execute("update book_copies set No_of_copies = No_of_copies where + 1 book_id = ?", (biq,))

        bq.commit()

        bq_cur.execute("select no_of_copies from book_copies where book_id = ?", (biq,))
        copynum = (bq_cur.fetchall()[0][0])

        label = Label(chwindow, text="books left {}".format(copynum))
        label.grid(row=5, column=0, columnspan=2, pady=10, padx=10)



    #Submit Button
    Submit_button = Button(chwindow, text = 'Checkout', command = submitc )
    Submit_button.grid(row = 0, column = 0, columnspan = 2, pady = 10, padx = 10)


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

#checkout test Button
Checkout_button = Button(root, text = 'Checkout', command = checkout)
Checkout_button.grid(row = 4, column = 0, columnspan = 2, pady = 10, padx = 10)

#Execute
root.mainloop()
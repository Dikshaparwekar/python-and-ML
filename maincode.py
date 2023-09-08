from tkinter import *
import mysql.connector
from PIL import *
from tkinter import messagebox


# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Diksha123@",
    database="library"
)
cursor = conn.cursor()

# Create a table for books
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS books 
       (id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        author VARCHAR(255),
        status VARCHAR(255))'''
)

# Create a table for users
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS users 
       (id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255),
        password VARCHAR(255))'''
)

# Function to validate login
def validateLogin():
    username = usernameEntry.get()
    password = userpasswordEntry.get()

    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    if user:
        showMainPage()
    else:
        messagebox.showerror("Invalid User", "Invalid User")

# Function to register a new user
def registerUser():
    username = usernameEntry.get()
    password = userpasswordEntry.get()

    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()

    if user:
          messagebox.showinfo("Username", "Username already exists")
    else:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        messagebox.showinfo("Register User", "User Registered Succesfully")

# Function to show the main page after successful login
def showMainPage():
    window1.destroy()

    # Window for main page
    window2 = Tk()
    window2.geometry("800x600")
    window2.title('Library status System')
    window2.config(bg="#fff2cc")

    bg =PhotoImage(file="Img1.png")

    #label
    mylabel = Label(window2,image =bg)
    mylabel.place(x=0,y=0,relwidth =1,relheight=1)

    # Rest of the code for the main page...
    def requestBook():
        title = bookTitleEntry.get()
        author = bookAuthorEntry.get()

        cursor.execute("INSERT INTO books (title, author, status) VALUES (%s, %s, %s)", (title, author, "Requested"))
        conn.commit()

        messagebox.showinfo("Request book", "Book reuested Successfully")

    # Function to issue a book
    def issueBook():
        book_id = bookIDEntry.get()

        cursor.execute("UPDATE books SET status=%s WHERE id=%s", ("Issued", book_id))
        conn.commit()

        messagebox.showinfo("Issue Book", "Book issued Successfully")

    # Function to return a book
    def returnBook():
        book_id = bookIDEntry.get()

        cursor.execute("UPDATE books SET status=%s WHERE id=%s", ("Available", book_id))
        conn.commit()

        messagebox.showinfo("Return book", "Book returned Successfully")

    # Function to view the book list
    def viewBookList():
        cursor.execute("SELECT * FROM books")
        book_list = cursor.fetchall()

        bookListbox.delete(0, END)

        for book in book_list:
            bookListbox.insert(END, f"ID: {book[0]} | Title: {book[1]} | Author: {book[2]} | Status: {book[3]}")
    
    def exitGUI():
        window2.destroy()

    # Labels, Entries, and Buttons for main page
    bookTitleLabel = Label(window2, text="Book Title", font=('Times', 20, "bold italic"))
    bookTitleLabel.place(x=920, y=70)
    bookTitleEntry = Entry(window2, font=('Times', 20, "bold italic"))
    bookTitleEntry.place(x=1120, y=70)

    bookAuthorLabel = Label(window2, text="Book Author", font=('Times', 20, "bold italic"))
    bookAuthorLabel.place(x=920, y=170)
    bookAuthorEntry = Entry(window2, font=('Times', 20, "bold italic"))
    bookAuthorEntry.place(x=1120, y=170)

    requestButton = Button(window2, text="Request Book", font=('Times', 20, "bold italic"), command=requestBook)
    requestButton.place(x=1150, y=270)

    bookIDLabel = Label(window2, text="Book ID", font=('Times', 20, "bold italic"))
    bookIDLabel.place(x=920, y=500)
    bookIDEntry = Entry(window2, font=('Times', 20, "bold italic"))
    bookIDEntry.place(x=1120, y=500)

    issueButton = Button(window2, text="Issue Book", font=('Times', 20, "bold italic"), command=issueBook)
    issueButton.place(x=1220, y=600)

    returnButton = Button(window2, text="Return Book", font=('Times', 20, "bold italic"), command=returnBook)
    returnButton.place(x=920, y=600)

    viewButton = Button(window2, text="View Book List", font=('Times', 20, "bold italic"), command=viewBookList)
    viewButton.place(x=250, y=700)

    resultlabel2 = Label(window2)
    resultlabel2.grid(row=6, column=0)

    bookListbox = Listbox(window2, width=70, height=30, font=('Times', 12,"bold italic"))
    bookListbox.place(x=50, y=50)

    exitButton = Button(window2, text="Exit", font=('Times', 20, "bold italic"), command=exitGUI)
    exitButton.place(x=1430, y=750)
    

    # Main loop for the main page
    window2.mainloop()

# Window for login page
window1 = Tk()
window1.geometry("400x600")
window1.title('Log in page for library manager')
window1.config(bg="#fff2cc")

# Load the image

bg =PhotoImage(file="Img3.png")

#label
mylabel = Label(window1,image =bg)
mylabel.place(x=0,y=0,relwidth =1,relheight=1)

welcomelabel = Label(window1,text="Library Status", 
font=('Times', 40, "bold italic"), fg='black', bg='white')
welcomelabel.place(x=700, y=200)

# Labels, Entries, and Buttons for login page
usernamelabel = Label(window1, text="Username", font=('Times', 20, "bold italic"))
usernamelabel.place(x=570, y=370)
usernameEntry = Entry(window1, font=('Times', 20, "bold italic"))
usernameEntry.place(x=720, y=370)
# usernamelabel.config(bg='#ff6b6b')

userpasswordlabel = Label(window1, text="Password", font=('Times', 20, "bold italic"))
userpasswordlabel.place(x=570, y=450)
userpasswordEntry = Entry(window1, font=('Times', 20, "bold italic"),show="*")
userpasswordEntry.place(x=720, y=450)
# userpasswordlabel.config(bg='#ff6b6b')

loginButton = Button(window1, text="Login", font=('Times', 20, "bold italic"), command=validateLogin)
loginButton.place(x=800, y=520)

registerButton = Button(window1, text="Register", font=('Times', 20, "bold italic"), command=registerUser)
registerButton.place(x=790, y=600)

resultlabel = Label(window1)
resultlabel.grid(row=6, column=0)

# Main loop for the login page
window1.mainloop()

# Close the database connection
conn.close()

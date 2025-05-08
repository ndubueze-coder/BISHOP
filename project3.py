import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import csv, os, hashlib
from datetime import datetime

# File paths
USERS_FILE = 'users.csv'
BOOKS_FILE = 'books.csv'
LOG_FILE = 'log.csv'
BORROWED_FILE = 'borrowed_books.csv'

ROLES = ['Admin', 'Librarian', 'Member']

# Initial file setup
for file, headers in [
    (USERS_FILE, ['Username', 'Password', 'Role']),
    (BOOKS_FILE, ['Book ID', 'Title', 'Author', 'Available']),
    (LOG_FILE, ['Username', 'Action']),
    (BORROWED_FILE, ['Username', 'Book Title', 'Date Borrowed'])
]:
    if not os.path.exists(file):
        with open(file, 'w', newline='') as f:
            csv.writer(f).writerow(headers)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    with open(USERS_FILE, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Username'] == username and row['Password'] == hash_password(password):
                return row['Role']
    return None

def log_action(username, action):
    with open(LOG_FILE, 'a', newline='') as f:
        csv.writer(f).writerow([username, action])

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("800x600")
        self.user = None
        self.role = None
        self.container = None
        self.container2 = None
        self.login_screen()

    def set_background(self, image_path, frame_bg='#BA55D3'):
        self.clear()
        image = Image.open(image_path).resize((900, 900))
        self.bg_img = ImageTk.PhotoImage(image)

        self.bg_label = tk.Label(self.root, image=self.bg_img)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.container = tk.Frame(self.root, bg=frame_bg, bd=0, highlightthickness=0)
        self.container.place(relx=0.5, rely=0.5, anchor="center", height= 370, width= 370)

    def login_screen(self):
        self.set_background("bg.jpg")
        tk.Label(self.container, text="Library Login", font=('Arial bold', 40), bg='#BA55D3', fg="white", width=260).pack(pady=5)
        tk.Label(self.container, text="Username:", font= ("Arial ", 24), width= 260).pack()
        self.username_entry = tk.Entry(self.container, width=260, font=24)
        self.username_entry.pack()
        tk.Label(self.container, text="Password:", font=('Arial ', 24), width=370).pack(pady=(10,0))
        self.password_entry = tk.Entry(self.container, width= 260, font=24, show='*')
        self.password_entry.pack()
        tk.Button(self.container, text="Login", bg="#1E90FF",width=10, font=('Arial bold', 18),fg='white', command=self.login).pack(pady=(15,5))
        tk.Button(self.container, text="Register", bg="#9400D3", width=12, font=('Arial bold', 18), fg='white', command=self.register_screen).pack(pady=(15,5))

    def register_screen(self):
        self.set_background("bg.jpg")
        tk.Label(self.container, text="Register", font=('Arial bold', 36), bg='#afaffa').pack(pady=10)
        labels = ['Username', 'Password']
        self.entries = {}
        for label in labels:
            tk.Label(self.container, text=f"{label}:", bg="white", font=('Arial bold', 15), width=370).pack(pady=(5, 0))
            self.entries[label] = tk.Entry(self.container, width=370, show='*' if label == 'Password' else None)
            self.entries[label].pack()
        tk.Label(self.container, text="Role", font=('Arial bold', 15), width=370).pack(pady=5)
        self.role_var = tk.StringVar(value='Member')
        tk.OptionMenu(self.container, self.role_var, *ROLES).pack()
        tk.Button(self.container, text="Register", font=('Arial bold', 15), bg="#af00ff",  fg='white',command=self.register).pack(pady=10)
        tk.Button(self.container, text="Back", font=('Arial bold', 15), bg="#aaf0ff", fg='white', command=self.login_screen).pack()

    def register(self):
        with open(USERS_FILE, 'a', newline='') as f:
            csv.writer(f).writerow([
                self.entries['Username'].get(),
                hash_password(self.entries['Password'].get()),
                self.role_var.get()
            ])
        messagebox.showinfo("Success", "Registration complete")
        self.login_screen()

    def login(self):
            username = self.username_entry.get()
            password = self.password_entry.get()
            role = authenticate(username, password)
            if role:
                self.user = username
                self.role = role
                self.password = password
                log_action(username,"Logged in")
                self.dashboard()
            else:
                messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        with open(USERS_FILE, 'a', newline='') as f:
            csv.writer(f).writerow([
                self.entries['Username'].get(),
                hash_password(self.entries['Password'].get()), self.role_var.get()
            ])
        messagebox.showinfo("Success", "Registration complete")
        self.login_screen()

    def dashboard(self):
        self.set_background("bg.jpg",  frame_bg='white')
        tk.Label(self.container, text=f"{self.role} Dashboard - {self.user}", font=('Arial', 16), bg='white').pack(pady=10)

        if self.role in ['Admin', 'Librarian']:
            tk.Button(self.container, text="Add Book", command=self.add_book,bg="#af00ff", fg='white', font=('Arial bold', 15),).pack()
            tk.Button(self.container, text="Display Books", command=self.view_books,bg="#af00ff", fg='white', font=('Arial bold', 15)).pack()
            tk.Button(self.container, text="lend Book", command=self.borrow_book,bg="#af00ff",  fg='white',font=('Arial bold', 15)).pack()
            tk.Button(self.container, text="Return Book", command=self.return_book,bg="#af00ff", fg='white', font=('Arial bold', 15)).pack()
            tk.Button(self.container, text="Remove Book", command=self.remove_book,bg="#af00ff", fg='white', font=('Arial bold', 15)).pack()
            tk.Button(self.container, text="view lending log", command=self.view_lending_log,bg="#af00ff", fg='white', font=('Arial bold', 15)).pack()
        

        else:
            tk.Button(self.container, text="Display Books", command=self.view_books,bg="#af00ff", fg='white', font=('Arial bold', 15)).pack()
            tk.Button(self.container, text="lend Book", command=self.borrow_book, bg="#af00ff",  fg='white',font=('Arial bold', 15)).pack()
            tk.Button(self.container, text="Return Book", command=self.return_book,bg="#af00ff",  fg='white',font=('Arial bold', 15)).pack()

        tk.Button(self.container, text="Logout", command=self.login_screen,bg="#af00ff", fg='white', font=('Arial bold', 15)).pack()

    def add_book(self):
        self.set_background("bg.jpg")
        tk.Label(self.container, text="Add Book", font=('Arial', 16), bg='lightblue').pack()
        title = tk.Entry(self.container)
        author = tk.Entry(self.container)
        for label, entry in [("Title", title), ("Author", author)]:
            tk.Label(self.container, text=label).pack()
            entry.pack()

        def save():
            book_id = str(hash(title.get() + author.get()))[-6:]
            with open(BOOKS_FILE, 'a', newline='') as f:
                csv.writer(f).writerow([book_id, title.get(), author.get(), 'Yes'])
            messagebox.showinfo("Success", "Book added successfully")
            self.dashboard()

        tk.Button(self.container, text="Save", command=save).pack(pady=10)
        tk.Button(self.container, text="Back", command=self.dashboard,bg="#af00ff", fg='white', font=('Arial bold', 15)).pack(pady=10)

    def view_books(self):
        book_window = tk.Toplevel(self.root)
        book_window.title("Books")
        tree = ttk.Treeview(book_window, columns=("Book ID", "Title", "Author", "Available"), show="headings")
        tree.heading("Book ID", text="Book ID")
        tree.heading("Title", text="Title")
        tree.heading("Author", text="Author")
        tree.heading("Available", text="Available")
        tree.pack(fill="both", expand=True)
        with open(BOOKS_FILE, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                tree.insert("", "end", values=(row['Book ID'], row['Title'], row['Author'], row['Available']))


    def view_lending_log(self):
        log_window = tk.Toplevel(self.root)
        log_window.title("Lending Log")
        tk.Label(log_window, text="Borrowed Books").pack()
        with open(BORROWED_FILE, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                tk.Label(log_window, text=f"{row['Book Title']} by {row['Username']} borrowed on {row['Date Borrowed']}").pack()


    
    def borrow_book(self):
        self.set_background("bg.jpg")
        tk.Label(self.container, text="lend Book", font=('Arial', 16), bg='lightblue').pack()
        book_id = tk.Entry(self.container)
        tk.Label(self.container, text="Enter Book ID").pack()
        book_id.pack()

        def borrow():
            rows, borrowed = [], False
            with open(BOOKS_FILE, newline='') as f:
                for row in csv.reader(f):
                    if row[0] == book_id.get() and row[3] == 'Yes':
                        row[3] = 'No'
                        borrowed = True
                    rows.append(row)
            with open(BOOKS_FILE, 'w', newline='') as f:
                csv.writer(f).writerows(rows)
            if borrowed:
                with open(BORROWED_FILE, 'a', newline='') as bf:
                    csv.writer(bf).writerow([self.user, book_id.get(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
                messagebox.showinfo("Success", "Book borrowed")
            else:
                messagebox.showerror("Error", "Book not available")
            self.dashboard()

        tk.Button(self.container, text="lend", command=borrow).pack(pady=10)
        tk.Button(self.container, text="Back", command=self.dashboard,bg="#af00ff", fg='white', font=('Arial bold', 15)).pack(pady=10)

    def return_book(self):
        self.set_background("bg.jpg")
        tk.Label(self.container, text="Return Book", font=('Arial', 16), bg='lightblue').pack()
        book_id = tk.Entry(self.container)
        tk.Label(self.container, text="Enter Book ID").pack()
        book_id.pack()

        def ret():
            rows, returned = [], False
            with open(BOOKS_FILE, newline='') as f:
                for row in csv.reader(f):
                    if row[0] == book_id.get() and row[3] == 'No':
                        row[3] = 'Yes'
                        returned = True
                    rows.append(row)
            with open(BOOKS_FILE, 'w', newline='') as f:
                csv.writer(f).writerows(rows)
            if returned:
                messagebox.showinfo("Returned", "Book returned")
            else:
                messagebox.showerror("Error", "Book was not borrowed")
            self.dashboard()

        tk.Button(self.container, text="Return", command=ret).pack(pady=10)
        tk.Button(self.container, text="Back", command=self.dashboard,bg="#af00ff", fg='white', font=('Arial bold', 15)).pack(pady=10)

    def remove_book(self):
        self.set_background("bg.jpg")
        tk.Label(self.container, text="Remove Book", font=('Arial', 16), bg='lightyellow').pack(pady=10)
        tk.Label(self.container, text="Enter Book ID or Title").pack()
        book_id_or_title = tk.Entry(self.container)
        book_id_or_title.pack()
    
        def remove_book_by_id_or_title():
            book_id_or_title_value = book_id_or_title.get()
            books = []
            found = False
            with open(BOOKS_FILE, newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['Book ID'] != book_id_or_title_value and row['Title'].lower() != book_id_or_title_value.lower():
                        books.append(row)
                    else:
                        found = True
            if found:
                with open(BOOKS_FILE, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=['Book ID', 'Title', 'Author', 'Available'])
                    writer.writeheader()
                    writer.writerows(books)
                messagebox.showinfo("Success", "Book removed successfully")
            else:
                messagebox.showerror("Error", "Book not found")
            self.dashboard()
        
        tk.Button(self.container, text="Remove Book", command=remove_book_by_id_or_title).pack(pady=10)
        tk.Button(self.container, text="Back", command=self.dashboard).pack(pady=10)


    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
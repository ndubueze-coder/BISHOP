# import tkinter as tk 
# from tkinter import ttk, messagebox 
# import csv, os, hashlib
# from datetime import datetime


# USERS_FILE = 'users.csv' 
# BOOKS_FILE = 'books.csv' 
# LOG_FILE = 'log.csv'

# ROLES = ['Admin', 'Librarian', 'Member']

# if not os.path.exists(USERS_FILE): 
#     with open(USERS_FILE, 'w', newline='') as f:
#          writer = csv.writer(f) 
#          writer.writerow(['Full Name', 'Email', 'Phone', 'Username', 'Password', 'Role'])

# if not os.path.exists(BOOKS_FILE): 
#     with open(BOOKS_FILE, 'w', newline='') as f:
#          writer = csv.writer(f) 
#          writer.writerow(['Book ID', 'Title', 'Author', 'Available'])

# if not os.path.exists(LOG_FILE): 
#     with open(LOG_FILE, 'w', newline='') as f: 
#         writer = csv.writer(f) 
#         writer.writerow(['Username', 'Action'])

# def hash_password(password): 
#     return hashlib.sha256(password.encode()).hexdigest()

# def authenticate(username, password): 
#     with open(USERS_FILE, newline='') as f: 
#         reader = csv.DictReader(f) 
#         for row in reader: 
#           if row['Username'] == username and row['Password'] == hash_password(password): return row['Role'] 
#     return None

# def log_action(username, action): 
#     with open(LOG_FILE, 'a', newline='') as f: 
#         writer = csv.writer(f) 
#         writer.writerow([username, action])

# class LibraryApp: 
#     def __init__(self, root): 
#         self.root = root 
#         self.root.title("Group 3 Library Management System") 
#         self.user = None 
#         self.login_screen()

#     def login_screen(self):
#         self.clear()
#         tk.Label(self.root, text="Login", font=('Arial', 16)).pack(pady=10)
#         tk.Label(self.root, text="Username").pack()
#         self.username_entry = tk.Entry(self.root)
#         self.username_entry.pack()
#         tk.Label(self.root, text="Password").pack()
#         self.password_entry = tk.Entry(self.root, show='*')
#         self.password_entry.pack()
#         tk.Button(self.root, text="Login", command=self.login).pack(pady=10)
#         tk.Button(self.root, text="Register", command=self.register_screen).pack()

#     def register_screen(self):
#        self.clear()
#        tk.Label(self.root, text="Register", font=('Arial', 16)).pack(pady=10)
#        self.fullname = tk.Entry(self.root)
#        self.email = tk.Entry(self.root)
#        self.phone = tk.Entry(self.root)
#        self.username = tk.Entry(self.root)
#        self.password = tk.Entry(self.root, show='*')
#        for label in ['Full Name', 'Email', 'Phone', 'Username', 'Password']:
#          tk.Label(self.root, text=label).pack()
#          if label == 'Full Name': self.fullname.pack()
#          if label == 'Email': self.email.pack()
#          if label == 'Phone': self.phone.pack()
#          if label == 'Username': self.username.pack()
#          if label == 'Password': self.password.pack()
#        tk.Label(self.root, text="Role (admin/librarian/member)").pack()
#        self.role = tk.StringVar(value='Member')
#        tk.OptionMenu(self.root, self.role, *ROLES).pack()
#        tk.Button(self.root, text="Register", command=self.register).pack(pady=10)
#        tk.Button(self.root, text="Back", command=self.login_screen).pack()

#     def login(self):
#        username = self.username_entry.get()
#        password = self.password_entry.get()
#        role = authenticate(username, password)
#        if role:
#          self.user = username
#          log_action(username, "Logged in")
#          if role == 'Admin': self.admin_dashboard()
#          elif role == 'Librarian': self.librarian_dashboard()
#          else: self.member_dashboard()
#        else:
#          messagebox.showerror("Error", "Invalid credentials")

#     def register(self):
#        with open(USERS_FILE, 'a', newline='') as f:
#            writer = csv.writer(f)
#            writer.writerow([
#            self.fullname.get(), self.email.get(), self.phone.get(),
#            self.username.get(), hash_password(self.password.get()), self.role.get()])
#        messagebox.showinfo("Success", "Registration complete")
#        self.login_screen()

#     def admin_dashboard(self):
#        self.clear()
#        tk.Label(self.root, text=f"Admin Dashboard - {self.user}", font=('Arial', 16)).pack()
#        tk.Button(self.root, text="View Logs", command=self.view_logs).pack()
#        tk.Button(self.root, text="Logout", command=self.login_screen).pack(pady=10)

#     def librarian_dashboard(self):
#       self.clear()
#       tk.Label(self.root, text=f"Librarian Dashboard - {self.user}", font=('Arial', 16)).pack()
#       tk.Button(self.root, text="Add Book", command=self.add_book).pack()
#       tk.Button(self.root, text="Issue Book", command=self.issue_book).pack()
#       tk.Button(self.root, text="Return Book", command=self.return_book).pack()
#       tk.Button(self.root, text="Logout", command=self.login_screen).pack(pady=10)

#     def member_dashboard(self):
#       self.clear()
#       tk.Label(self.root, text=f"Member Dashboard - {self.user}", font=('Arial', 16)).pack()
#       tk.Button(self.root, text="View Available Books", command=self.view_books).pack()
#       tk.Button(self.root, text="Request Book", command=self.request_book).pack()
#       tk.Button(self.root, text="Borrow Book", command=self.Borrow_Books).pack()
#       tk.Button(self.root, text="Logout", command=self.login_screen).pack(pady=10)
      

#     def view_logs(self):
#        self.clear()
#        tk.Label(self.root, text="Logs", font=('Arial', 16)).pack()
#        with open(LOG_FILE, newline='') as f:
#         reader = csv.reader(f)
#         for row in reader:
#             tk.Label(self.root, text=' | '.join(row)).pack()
#        tk.Button(self.root, text="Back", command=self.admin_dashboard).pack()

#     def add_book(self):
#        self.clear()
#        tk.Label(self.root, text="Add Book", font=('Arial', 16)).pack()
#        title = tk.Entry(self.root)
#        author = tk.Entry(self.root)
#        tk.Label(self.root, text="Title").pack()
#        title.pack()
#        tk.Label(self.root, text="Author").pack()
#        author.pack()
#        def save():
#         book_id = str(hash(title.get() + author.get()))[-6:]
#         with open(BOOKS_FILE, 'a', newline='') as f:
#             csv.writer(f).writerow([book_id, title.get(), author.get(), 'Yes'])
#         messagebox.showinfo("Added", "Book added successfully")
#         self.librarian_dashboard()
#         tk.Button(self.root, text="Save", command=save).pack(pady=10)

#     def issue_book(self):
#        self.clear()
#        tk.Label(self.root, text="Issue Book", font=('Arial', 16)).pack()
#        book_id = tk.Entry(self.root)
#        tk.Label(self.root, text="Enter Book ID to Issue").pack()
#        book_id.pack()
#        def issue():
#         rows = []
#         issued = False
#         with open(BOOKS_FILE, newline='') as f:
#             reader = csv.reader(f)
#             for row in reader:
#                 if row[0] == book_id.get() and row[3] == 'Yes':
#                     row[3] = 'No'
#                     issued = True
#                 rows.append(row)
#         with open(BOOKS_FILE, 'w', newline='') as f:
#             csv.writer(f).writerows(rows)
#         if issued:
#             messagebox.showinfo("Issued", "Book issued")
#         else:
#             messagebox.showerror("Unavailable", "Book not found or already issued")
#         self.librarian_dashboard()
#         tk.Button(self.root, text="Issue", command=issue).pack(pady=10)

#     def return_book(self):
#        self.clear()
#        tk.Label(self.root, text="Return Book", font=('Arial', 16)).pack()
#        book_id = tk.Entry(self.root)
#        tk.Label(self.root, text="Enter Book ID to Return").pack()
#        book_id.pack()
#        def ret():
#         rows = []
#         returned = False
#         with open(BOOKS_FILE, newline='') as f:
#             reader = csv.reader(f)
#             for row in reader:
#                 if row[0] == book_id.get() and row[3] == 'No':
#                     row[3] = 'Yes'
#                     returned = True
#                 rows.append(row)
#         with open(BOOKS_FILE, 'w', newline='') as f:
#             csv.writer(f).writerows(rows)
#         if returned:
#             messagebox.showinfo("Returned", "Book returned")
#         else:
#             messagebox.showerror("Error", "Invalid book ID or already available")
#         self.librarian_dashboard()
#         tk.Button(self.root, text="Return", command=ret).pack(pady=10)

#     def view_books(self):
#         self.clear()
#         tk.Label(self.root, text="Available Books", font=('Arial', 16)).pack()
#         with open(BOOKS_FILE, newline='') as f:
#             reader = csv.DictReader(f)
#         for row in reader:
#             if row['Available'] == 'Yes':
#                 tk.Label(self.root, text=f"{row['Book ID']} - {row['Title']} by {row['Author']}").pack()
#         tk.Button(self.root, text="Back", command=self.member_dashboard).pack()

#     def request_book(self):
#        self.clear()
#        tk.Label(self.root, text="Request Book", font=('Arial', 16)).pack()
#        request_title = tk.Entry(self.root)
#        tk.Label(self.root, text="Enter Book Title to Request").pack()
#        request_title.pack()
#        def submit():
#         log_action(self.user, f"Requested book: {request_title.get()}")
#         messagebox.showinfo("Requested", "Your request has been noted")
#         self.member_dashboard()
#         tk.Button(self.root, text="Submit Request", command=submit).pack(pady=10)


#     def Borrow_Books(self, member_username, book_title):
#         books = []
#         found = False
#         with open('books.csv', 'r', newline='') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 if row['Title'].lower() == book_title.lower() and int(row['Quantity']) > 0:
#                     row['Quantity'] = str(int(row['Quantity']) - 1)
#                 found = True
#                 borrowed_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                 with open('borrowed_books.csv', 'a', newline='') as bf:
#                     writer = csv.writer(bf)
#                     writer.writerow([member_username, book_title, borrowed_date])
#                 books.append(row)
#         if not found:
#            return f"Book '{book_title}' is not available or out of stock."

#         with open('books.csv', 'w', newline='') as file:
#            writer = csv.DictWriter(file, fieldnames=['Title', 'Author', 'Quantity'])
#            writer.writeheader()
#            writer.writerows(books)
#            return f"Book '{book_title}' successfully borrowed by {member_username}."


#     def clear(self):
#         for widget in self.root.winfo_children():
#             widget.destroy()

# if __name__ == '__main__':
#      root = tk.Tk() 
#      app = LibraryApp(root)
#      root.mainloop()
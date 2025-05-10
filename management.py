# import tkinter as tk
# from tkinter import messagebox

# # Dummy book database (in-mermory)
# books = []
# def add_book():
#     title = title_entry.get()
#     author = author_entry.get()
#     year = year_entry.get()

#     if title and author and year:
#         books.append((title, author, year))
#         update_listbox()
#         clear_entries()
#     else:
#         messagebox.showwarning("Input Error, All fields are required!")

# def delete_book():
#     select = listbox.curselection()
#     if select:
#         books,pop(select[0])
#         update_listbox()
#     else:
#         messagebox.showwarning("selection Error", "No book selected!")

# def update_listbox():
#     listbox.delete(0, tk.END)
#     for idx, book in enumerate(books):
#         listbox.insert(tk.END, f"{idx+1}. {book[0]} by {book[1]} ({book[2]})")

# def clear_entries():
#     title_entry.delete(0, tk.END)
#     author_entry.delete(0, tk.END)
#     year_entry.delete(0, tk.END)

# # Main window
# root = tk.Tk()
# root.title("Library Management System")

# # Labels
# tk.Label(root, text="Title").grid(row=0, column=0, padx=10, pady=5)
# tk.Label(root, text="Author").grid(row=1, column=0,padx=10, pady=5)
# tk.Label(root, text="Year").grid(row=2, column=0, padx=10, pady=5)

# # Entry fields
# title_entry = tk.Entry(root)
# title_entry.grid(row=0, column=1, padx=10, pady=5)

# author_entry = tk.Entry(root)
# author_entry.grid(row=1, column=1, padx=10, pady=5)

# year_entry = tk.Entry(root)
# year_entry.grid(row=2, column=1, padx=10, pady=5)

# # Buttons
# tk.Button(root, text="Delete Book", command=add_book).grid(row=3, column=0, pady=10)
# tk.Button(root, text="Delete Book", command=delete_book).grid(row=3, column=1, pady=10)

# # Listbox 
# listbox = tk.Listbox(root, width=50)
# listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# # run the app 
# root.mainloop()



# import tkinter as tk
# from tkinter import messagebox

# # predefined credentials (you can modify or expand this)
# user = {
#   'admin':'1234',
#   'user':'password'
# }

# # sample library data 
# library = []

# # functions
# def verify_login():
#     username = username_entry.get()
#     password = password_entry.get()
#     if username in users and user[username] == password:
#         login_window.destroy()
#         open_library_window()
#     else:
#         messagebox.showerror("Login Failed", "Invalid username or password.")

# def add_book():
#     title = title_entry.get()
#     author = author_entry.get()
#     if title and author:
#         library.append({'title':title, 'author':author})
#         update_book_list()
#         title_entry.delete(0, tk.END)
#         author_entry.delete(0, tk.END)
#     else:
#         messagebox.showwarning("input Error", "Entry both title and author.")

# def delete_book():
#     selected = book_listbox.curselection()
#     if selected:
#         index = selected[0]
#         del library[index]
#         update_book_list()
#     else:
#         messagebox.showwarning("selection Error" "Select to delete.")

# def update_book_list():
#     book_listbox.delete(0, tk.END)
#     for book in library:
#         book_listbox.insert(tk.END, f"{book['title']} by {book['author']}")

# # GUI for library management 
# def open_library_window():
#     global title_entry, author_entry, book_listbox

#     root = tk.Tk()
#     root.title("Library Management system")

#     tk.Label(root, text="Book Title").grid(row=0, column=1, padx=5)
#     title_entry = tk.Entry(root)
#     title_entry.grid(row=0, column=1, padx=10., pady=5)

#     tk.Label(root, text="Author").grid(row=1, column=0, padx=10, pady=5)
#     author_entry = entry =tk.Entry(root)
#     author_entry.grid(row=1, column=1, padx=10, pady=5)

#     tk.Button(root, text="Add Book", command=add_book).grid(row=2, column=0, columnspan=2, pady=10, )
#     tk.Button(root, text="Delete Selected", command=delete_book).grid(row=3, columnspan=2, pady=5)

#     book_listbox = tk.Listbox(root, width=50)
#     book_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

#     root.mainloop()

#     # Login Window 
#     login_window = tk.Tk()
#     login_window.title("Login")

#     tk.Label(login_window, text="Username:").grid(row=0, column=0, padx=10, pady=5)

#     tk.Label(login_window, text="password:").grid(row=1, column=0, padx=10, pady=5)
#     password_entry = tk.Entry(login_window, show='*')
#     password_entry.grid(row=1, column=1, padx=10, pady=5)

#     tk.Button(login_window, text="Login", command=verify_login ).grid(row=2, column=0, columnspan=2, pady=10,)
    
#     login_window.mainloop()



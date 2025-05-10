# # def main():
# #     print("Library Management System")
# # if __name__ == "__main__":
# #     main()



# import tkinter as tk
# from tkinter import messagebox, ttk

# # sample book list 
# books = []

# # # add book list 
# def add_book():
#     title = title_entry.get()
#     author = author_entry.get()
#     if title and author:
#         books.append({'title': title, 'author': author})
#         messagebox.showinfo("success", "Book added successfully!")
#         title_entry.delete(0, tk.END)
#         author_entry.delete(0, tk.END)
#         view_books()
#     else:
#         messagebox.showwarning("input Error", "please enter both title and author.")
# # view all books
# def view_books():
#     for i in tree.get_childdren():
#         tree.delete(i)
#         for index, book in enumerate(books):
#             tree.insert('', 'end', iid=index, values=(book['title'], book['author']))
# # Delete selected book
# def delete_book():
#     select_item = tree.selection()
#     if select_item:
#         index = int(select_item[0])
#         del books[index]
#         view_books()
#         messagebox.showinfo("success", "Book deleted.")
#     else:
#         messagebox.showwarning("selection Error", "No book selected.")

# create main window
# root = tk.Tk()
# root.title("Library Management System")
# root.geometry("600x400")

# # input frame
# input_frame = tk.Frame(root)
# input_frame.pack(pady=10)

# tk.Label(input_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5)
# title_entry = tk.Entry(input_frame)
# title_entry.grid(row=0, column=1, padx=5, pady=5)

# tk.Label(input_frame, text="Author:").grid(row=1, column=0, padx=5, pady=5)
# author_entry = tk.Entry(input_frame)
# author_entry.grid(row=1, column=1, padx=5, pady=5)

# tk.Button(input_frame, text="Add Book", command=add_book).grid(row=2, column=0, columnspan=2, pady=10)

# # Treeview for displaying books
# tree = ttk.Treeview(root, columns=('Title', 'Author'), show='headings')
# tree.heading('Title', text='Title')
# tree.heading('Author', text='Author')
# tree.pack(pady=10, fill='x')

# tk.Button(root, text="Delete Selected Book", command=delete_book).pack(pady=10)

# # start app
# root.mainloop




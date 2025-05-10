# import re



# # def valid_input(expressinon):
# #     pattern = r'^\s*[\d\s\+\-\*/\(\)]+\s*$'
# #     if re.match(pattern, expression):
# #        print("pattern conrrect")
# #     else:
# #      print("invalid input!")

# # valid_input("obi is a b
# # r"^ \s $"

# # print("hello world, \nhello class")

# # import re
# # def valid_input(expression):...

# # # valid_date("obi is a boy")

# # def valid_date(date):
# #     pattern = r"^\s[\d/\d/\d]+$"
# #     if re.match(pattern, date):
# #         print("correct format")
# #     else:
# #         print("incorrct format")

# # def check_date():
# #     date = input("enter date: ")
# #     valid_date(date)

# # check_date()

# # create a function for multiplication

# # def multiply(num1, num2):
#     # return num1 * num2


# # # create a function to divide
# # def divide(num1, num2):
# #     return num1 / num2

# # # create a function to add
# # def addition(num1, num3):
# #     return num1 + num2

# # # create a function to subtract
# # def subtration(num1, num2):
# #     return num1 - num2

# def calc():
#  while True:
#      print("welcome to my caculator")
#      print("1. addiction",          
#           "\n2. subtraction",
#            "\n3. division",
#            "\n4. multiplication", "\n")
#      choice = input("please choose an operation(1-4):")
#      num1 = int(input("first number: "))
#      num1 = int(input("second number:"))
#      if choice == "1":
#           print(addition(num1, num2))
#      elif choice == "2":
#           print(subtraction(num1, num2))
#      elif choice == "3":
#           print(divide(num1, num2))
#      elif choice == "4":
#           print(multiply(num1, num2))
#      else:
#           print("invalid choice")
#      response = input("perform another operation?(yes/no):").lower()
#      if response == "no":
#         break
# calc()

# import tkinter as tk

# root = tk.Tk()


# root.title("WELCOME TO MY GUI")
# root.iconbitmap("WIN_20250304_05_43_21_Pro.ico")
# root.geometry("250x150")

# Frame1 = tk.Frame(root)
# Frame1.grid()
# name = tk.Label(Frame1, text="enter your name")
# name.pack(side= "left", padx= 25, expand= True )

# name_entry = tk.Entry(Frame1)
# name_entry.pack(side = "right", padx=(0,25),expand= True)

# Frame2 = tk.Frame(root)
# Frame2.grid()
# password = tk.Label(Frame2, text= "enter your password")
# password.grid(row=0, column=0)

# password_entry = tk.Entry(Frame2)
# password_entry.grid(row = 0, column = 1)

# root.mainloop()




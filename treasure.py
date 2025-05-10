# import qrcode
# data = input("enter the data you want to code:")
# dest = input(
#     "enter the full path destination of where you want your qrcde to be sat"
# )
# qr_name = input("enter the name to save the image:")
# dest = dest.replace("\\", "/")
# dest = dest + "/" + qr_name + ".png"
# img = qrcode.make(data)
# img.save(dest)
# print("success! you can check the folder for the QR code")


# import pandas as pd
# data = ['Steve', '35', 'Male', '3.5']
# series = pd.Series(data, index=['Name', 'Age', 'Gender', 'Rating'])
# print(series)


# # defining class
# class Smartphone:
#    # constructor    
#    def __init__(self, device, brand):
#       self.device = device
#       self.brand = brand
   
#    # method of the class
#    def description(self):
#       return f"{self.device} of {self.brand} supports Android 14"

# # creating object of the class
# # phoneObj = Smartphone("Smartphone", "Samsung")
# # print(phoneObj.description()) 
# phone_obj = Smartphone('smartphone', 'samsung')
# print(phone_obj)

# # creating a class my fullname
# class Name:
#     def __init__(self, first_name, middle_name, last_name):
#         self.f_name = first_name
#         self.m_name = middle_name
#         self.l_name = last_name
#     def Fullname(self):
#         return print(f"my name is {self.f_name} {self.m_name} {self.l_name}")
# # my_fullname("king," "diligent" "samuel")
# Fullname = Name("king", "diligent", "samuel")
# Fullname.Fullname()

################
    
# class class_name:
#     x = 'data enginerring'
# course = class_name()
# print(course.x)


# class car:
#     def __init__(self, make, model, year):
#         self.make = make
#         self.model = model
#         self.year = year
#     def display_info(self):
#         return print(f"{self.make} {self.model} {self.year}")
# car_detail = car("toyota", "avellon", "2025")
# car_detail.display_info()


# class book:
#     def __init__(self, tittle, author,pages):
#         self.tittle =tittle
#         self.author = author
#         self.pages = pages
#     def is_long(self):
#         return self.pages > 300
# E_book = book("data engineering", "king bishop diligent",100)
# print(E_book.is_long())









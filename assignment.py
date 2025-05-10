# import os
############### read the first n lines ################



# import matplotlib.pyplot as plt
# # create a new figure
# fig = plt. figure()


# # add a plot or subplot to figure
# plt.plot([1, 2, 3, ], [4, 5, 6])
# plt.show()


# # create a plot 
# plt.plot([1, 2, 3, 4], [10, 20, 25,30])

# # customizing axis limits and labels
# plt.xlim(0, 5)
# plt.ylim(0, 35)
# plt.xlabel('x-axis')
# plt.ylabel('y-axis')
# plt.show()




# import tkinter as tk

# root = tk.Tk()

# root.mainloop()


# import matplotlib.pyplot as plt
# create a figure and an axis (subplot)
# fig, ax = plt.subplots()

# plot a line (artist)
# line = ax.plot([1, 2, 3], [4, 5,6], label='line')[0]

# modify line properties

# # data
# x = [1, 2, 3, 4, 5]
# y = [2, 4, 6, 8, 10]

# # create a figure
# plt.figure(figsize=(8, 6), dpi=100)

# # add a line plot to the figure
# plt.plot(x, y, label='line plot')

# # customize the plot
# plt.title('figure with line plot')
# plt.xlabel('x-axis')
# plt.ylabel('y-axis')
# plt.legend()

# # display the figure
# plt.show()

# import matplotlib.pyplot as plt
# print(plt.style.available) #prints available styles

# import matplotlib.pyplot as plt
# using a specific style
# plt.style.use('seaborn-darkgrid')


# # create a sample plot 
# plt.plot([1, 2, 3, 4,], [10, 15, 25, 30])
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.title('Sample plot')


# # Example data 
# x = [1, 2, 3]
# y1 = [2, 4, 6]
# y2 = [1, 3, 5]
# y3 = [3, 6, 9]

# # ploting the data 
# line1, = plt.plot(x, y1)
# line2, = plt.plot(x, y2)
# line3, = plt.plot(x, y3)

# # calling legend with explicitly list artists and labels 
# plt.legend([line1, line2, line3], ['Label 1', 'Label 2', 'Label 3'])

# # show the plot 
# plt.show()
# # print('successfully placed a legend on the axes...')

# import matplotlib.pyplot as plt

# x = [1, 2, 3, 4, 5]
# y1 = [10, 15, 7, 12,8]
# y2 = [8, 12, 6, 10, 15]

# plt.plot(x, y1, label='line 1')
# plt.plot(x, y2, label='line 2', linestyle='--', marker='o')
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.title('Multiple Lines with Legend')
# plt.legend()
# plt.show()



# categories = ['categories A', 'category B', 'category C']
# values = [15, 24,30]

# plt.bar(categories, values, color='skyblue')
# plt.xlabel('values')
# plt.title('Basic Vertical Bar Graph')
# plt.show()




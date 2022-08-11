import tkinter as tk


window = tk.Tk()
window.title("Inventory Manager, By Karthik Raman")
window.geometry("500x300+10+20")
greetings = tk.Label(text="Inventory Management System")
greetings.pack(side=tk.TOP)

option = tk.IntVar()
option.set(1)

tk.Radiobutton(window, text="1) To List All Tables",variable=option,value=1).pack(side=tk.TOP,ipady=5,anchor=tk.W)
tk.Radiobutton(window, text="2) To List the values of Table",variable=option,value=2).pack(side=tk.TOP,ipady=5,anchor=tk.W)
tk.Radiobutton(window, text="3) To Add Value to a Table",variable=option,value=3).pack(side=tk.TOP,ipady=5,anchor=tk.W)
tk.Radiobutton(window, text="4) To Create a Table",variable=option,value=4).pack(side=tk.TOP,ipady=5,anchor=tk.W)
tk.Radiobutton(window, text="5) To Delete a Table",variable=option,value=5).pack(side=tk.TOP,ipady=5,anchor=tk.W)
tk.Radiobutton(window, text="6) Delete Value in a Table",variable=option,value=6).pack(side=tk.TOP,ipady=5,anchor=tk.W)
tk.Radiobutton(window, text="7) Stop",variable=option,value=7).pack(side=tk.TOP,ipady=5,anchor=tk.W)

greetings.pack()


window.mainloop()

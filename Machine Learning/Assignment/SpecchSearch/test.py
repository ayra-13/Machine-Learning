import tkinter as tk

root = tk.Tk()
root.geometry("800*500")
root.title("Testing")    # naming

label = tk.Label(root, text= "Text here" )
label.pack()


root.mainloop()
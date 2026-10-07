from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Searching and Sorting Algorithms")
root.geometry("400x300")
frm = ttk.Frame(root, relief=ttk.Style(SOLID), borderwidth=5)
frm.pack(fill="both", expand=True, padx=10, pady=10)


name = ttk.Label(frm , text="Searching and Sorting Algorithms")


root.mainloop()

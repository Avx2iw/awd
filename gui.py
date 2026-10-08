from search import search
from sort import sorts
import tkinter as tk

root = tk.Tk()
root.title("Searching and Sorting Algorithms")
root.geometry("800x700")
frm = tk.Canvas(root, bg="grey", width=800, height=700)
frm.pack(fill="both", expand=True)

name = tk.Label(frm , text="Searching and Sorting Algorithms", font=("aerial", 30), background="red")

root.mainloop()

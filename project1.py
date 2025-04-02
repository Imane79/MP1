import tkinter as tk  # tkinter is Python’s built-in GUI library.
from tkinter import ttk, filedialog, messagebox
# ttk gives us modern widgets like Combobox, filedialog allows file selection (e.g., for Excel import)
# messagebox will be used for warnings/errors/success.
import pandas as pd  # pandas is for reading Excel and exporting .xls.
import random  # random is for the "Randomize" feature.
import json  # is for exporting to .json format.

# We define a class HealthyPlannerApp that will encapsulate all logic and UI components.


class HealthyPlannerApp:
    def __init__(self, root):
        # __init__ is the constructor — it runs when the app starts.
        # root is the main Tk() window passed into the class when it is initialized.
        self.root = root
        self.root.title("Healthy Lifestyle Planner")
        # Store the passed root window in self.root so it’s accessible everywhere in the class.
        # Set the window title that appears in the window's title bar.
        self.data = {}
        self.selected_title = tk.StringVar(value="Sports")
        # self.data: Will hold the Excel data after it’s loaded (Sports, Food Plans, etc.).
        # self.selected_title: A Tkinter StringVar bound to the Combobox (initially set to "Sports").
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        for j in range(5):
            self.root.grid_columnconfigure(j, weight=1)
        # This ensures all rows (0–5) and columns (0–4) can grow/stretch proportionally when resizing.
        #  weight=1 means each row/column shares space equall
        self.import_button = tk.Button(
            root, text="Import Excel File", command=self.import_excel)
        self.import_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        # This button lets users load their healthy plan Excel file (like data.xlsx).
        # It’s placed in row 0, column 0, with padding.
        # command=self.import_excel: when clicked, it will call the method self.import_excel() (we'll implement it soon).

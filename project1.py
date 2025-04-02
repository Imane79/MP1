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

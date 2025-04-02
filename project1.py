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
        # Setup root window
        self.root = root
        self.root.title("Healthy Lifestyle Planner")

        # State
        self.data = {}
        self.selected_title = tk.StringVar(value="Sports")

        # Grid layout config
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        for j in range(5):
            self.root.grid_columnconfigure(j, weight=1)

        # Import Button
        self.import_button = tk.Button(
            root, text="Import Excel File", command=self.import_excel)
        self.import_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Title Combobox
        self.title_combobox = ttk.Combobox(
            root, textvariable=self.selected_title, state="readonly")
        self.title_combobox['values'] = ("Sports", "Food Plans", "Activities")
        self.title_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.title_combobox.bind(
            "<<ComboboxSelected>>", lambda e: self.update_left_listbox())

        # Left Listbox
        self.left_listbox = tk.Listbox(root, height=10)
        self.left_listbox.grid(row=1, column=0, rowspan=3,
                               padx=5, pady=5, sticky="nsew")

        # Buttons (center)
        self.add_button = tk.Button(root, text="Add", command=self.add_item)
        self.add_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.delete_button = tk.Button(
            root, text="Delete", command=self.remove_item)
        self.delete_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.randomize_button = tk.Button(
            root, text="Randomize", command=self.randomize_selection)
        self.randomize_button.grid(
            row=3, column=1, padx=5, pady=5, sticky="ew")

        # Right Listbox
        self.right_listbox = tk.Listbox(root, height=10)
        self.right_listbox.grid(
            row=1, column=2, rowspan=3, padx=5, pady=5, sticky="nsew")

        # Text Widget for output
        self.text_output = tk.Text(root, height=10, wrap="word")
        self.text_output.grid(row=1, column=3, rowspan=3,
                              columnspan=2, padx=5, pady=5, sticky="nsew")

        # Export Section
        tk.Label(root, text="Week Number:").grid(row=4, column=0, sticky="e")
        self.week_entry = tk.Entry(root)
        self.week_entry.grid(row=4, column=1, sticky="ew")

        tk.Label(root, text="Export Format:").grid(row=4, column=2, sticky="e")
        self.export_format = ttk.Combobox(
            root, values=["txt", "json", "xls"], state="readonly")
        self.export_format.set("txt")
        self.export_format.grid(row=4, column=3, sticky="ew")

        self.export_button = tk.Button(
            root, text="Export", command=self.export_plan)
        self.export_button.grid(row=4, column=4, padx=5, pady=5, sticky="ew")


def import_excel(self):
    try:
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel Files", "*.xlsx *.xls")]
        )
        if not file_path:
            return  # User cancelled

        # Read Excel file using pandas
        df = pd.read_excel(file_path)

        # Validate required columns
        required_columns = {"Sports", "Food Plans", "Activities"}
        if not required_columns.issubset(df.columns):
            messagebox.showerror(
                "Invalid Format", "Excel file must contain 'Sports', 'Food Plans', and 'Activities' columns.")
            return

        # Store data in self.data dictionary
        self.data = {
            "Sports": df["Sports"].dropna().tolist(),
            "Food Plans": df["Food Plans"].dropna().tolist(),
            "Activities": df["Activities"].dropna().tolist()
        }

        messagebox.showinfo("Success", "Excel data imported successfully!")
        self.update_left_listbox()

    except Exception as e:
        messagebox.showerror(
            "Error", f"Failed to import Excel file:\n{str(e)}")


# Entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = HealthyPlannerApp(root)
    root.mainloop()

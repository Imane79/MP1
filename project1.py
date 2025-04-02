import tkinter as tk  # tkinter is Python’s built-in GUI library.
from tkinter import ttk, filedialog, messagebox
import pandas as pd  # pandas is for reading Excel and exporting .xls.
import random  # random is for the "Randomize" feature.
import json  # is for exporting to .json format.


class HealthyPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Healthy Lifestyle Planner")

        # State
        self.data = {}
        self.selected_title = tk.StringVar(value="Sports")

        self.selected_items = {
            "Sports": [],
            "Food Plans": [],
            "Activities": []
        }

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

            df = pd.read_excel(file_path)

            required_columns = {"Sports", "Food Plans", "Activities"}
            if not required_columns.issubset(df.columns):
                messagebox.showerror(
                    "Invalid Format", "Excel file must contain 'Sports', 'Food Plans', and 'Activities' columns.")
                return

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

    def update_left_listbox(self):
        title = self.selected_title.get()
        items = self.data.get(title, [])

        self.left_listbox.delete(0, tk.END)

        for item in items:
            self.left_listbox.insert(tk.END, item)

        # Reset right listbox for new category
        self.right_listbox.delete(0, tk.END)
        for item in self.selected_items[title]:
            self.right_listbox.insert(tk.END, item)

    def add_item(self):
        title = self.selected_title.get()
        selected = self.left_listbox.curselection()

        if not selected:
            messagebox.showwarning(
                "No Selection", "Please select an item to add.")
            return

        item = self.left_listbox.get(selected[0])

        if len(self.selected_items[title]) >= 7:
            messagebox.showwarning(
                "Limit Reached", f"You can only select 7 items for {title}.")
            return

        if item in self.selected_items[title]:
            messagebox.showinfo(
                "Already Added", f"{item} is already selected.")
            return

        self.selected_items[title].append(item)

        self.right_listbox.delete(0, tk.END)
        for i in self.selected_items[title]:
            self.right_listbox.insert(tk.END, i)

    def remove_item(self):
        print("Remove item logic goes here.")

    def randomize_selection(self):
        print("Random selection logic goes here.")

    def export_plan(self):
        week_number = self.week_entry.get().strip()
        if not week_number.isdigit():
            messagebox.showerror(
                "Invalid Input", "Please enter a valid week number.")
            return
        for category, items in self.selected_items.items():
            if len(items) != 7:
                messagebox.showwarning(
                    "Incomplete Plan", f"{category} must have exactly 7 items.")
                return

        plan = {
            "Week": int(week_number),
            "Sports": self.selected_items["Sports"],
            "Food Plans": self.selected_items["Food Plans"],
            "Activities": self.selected_items["Activities"]
        }

        filetype = self.export_format.get()
        filename = f"HealthyLifeStyleForWeek{week_number}.{filetype}"
        try:
            if filetype == "txt":
                with open(filename, "w") as f:
                    for key, values in plan.items():
                        if isinstance(values, list):
                            f.write(f"{key}:\n")
                            for v in values:
                                f.write(f"- {v}\n")
                            f.write("\n")
                        else:
                            f.write(f"{key}: {values}\n\n")
            elif filetype == "json":
                with open(filename, "w") as f:
                    json.dump(plan, f, indent=4)
            elif filetype == "xls":
                df = pd.DataFrame(
                    dict([(k, pd.Series(v)) for k, v in plan.items() if isinstance(v, list)]))
                df.to_excel(filename, index=False)

            messagebox.showinfo(
                "Exported", f"Plan exported successfully as {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export plan:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = HealthyPlannerApp(root)
    root.mainloop()

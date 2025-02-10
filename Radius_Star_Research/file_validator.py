import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt

def process_file(input_filepath):
    try:
        with open(input_filepath, 'r') as infile:
            lines = infile.readlines()

        if len(lines) < 4:
            raise ValueError("Input file has less than 4 lines.")

        return [line.strip().split() for line in lines]  # Split by whitespace for tabular data

    except Exception as e:
        messagebox.showerror("File Error", f"An error occurred: {e}")
        return None

class FileValidatorApp:
    def __init__(self, root, file_data, process_callback, parent_app_class):
        self.process_callback = process_callback
        self.root = root
        self.file_data = file_data
        self.entries = []
        self.error_labels = []
        self.entry_frames = []
        self.parent_app_class = parent_app_class

        self.create_second_page()

    def create_second_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        gamma_label = tk.Label(self.root, text="Gamma:")
        gamma_label.grid(row=0, column=0, padx=10, pady=5, sticky='e')

        self.gamma_var = tk.StringVar(value="relativistic")
        gamma_frame = tk.Frame(self.root)
        gamma_frame.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        gamma_rel = tk.Radiobutton(gamma_frame, text="Relativistic", variable=self.gamma_var, value="relativistic")
        gamma_new = tk.Radiobutton(gamma_frame, text="Newtonian", variable=self.gamma_var, value="newtonian")
        gamma_rel.pack(side="left")
        gamma_new.pack(side="left")

        self.create_input_row("Starting pressure (row, col):", 1)
        self.create_input_row("Starting energy density (row, col):", 2)

        # Button frame for horizontal alignment
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=7, column=1, padx=10, pady=10, sticky='w')

        go_back_button = tk.Button(button_frame, text="Go Back", command=self.go_back)
        go_back_button.pack(side="left", padx=5)

        submit_button = tk.Button(button_frame, text="Submit", command=self.process_second_page_inputs)
        submit_button.pack(side="left", padx=5)

        instructions_button = tk.Button(button_frame, text="Instructions", command=self.show_instructions)
        instructions_button.pack(side="left", padx=5)

    def create_input_row(self, label_text, row):
        label = tk.Label(self.root, text=label_text)
        label.grid(row=row, column=0, padx=10, pady=5, sticky='e')

        frame = tk.Frame(self.root)
        frame.grid(row=row, column=1, padx=10, pady=5, sticky='w')

        row_var = tk.StringVar()
        col_var = tk.StringVar()

        row_entry = tk.Entry(frame, textvariable=row_var, width=5)
        row_entry.pack(side='left')
        col_entry = tk.Entry(frame, textvariable=col_var, width=5)
        col_entry.pack(side='left', padx=(5, 0))

        self.entries.append((row_entry, col_entry))

        error_label = tk.Label(self.root, text="", fg="red")
        error_label.grid(row=row + 1, column=1, padx=10, pady=5, sticky='w')
        self.error_labels.append(error_label)

    def show_instructions(self):
        instructions_window = tk.Toplevel(self.root)
        instructions_window.title("Instructions")

        instructions_text = (
            "Instructions:\n\n"
            "1. Select 'Relativistic' to set gamma to 4/3 or 'Newtonian' to set gamma to 5/3.\n"
            "2. Input the row and column indices for the starting pressure and energy density.\n"
            "3. Ensure the indices are within the range of the imported file data.\n"
            "4. The input columns cannot be greater than two because that will lead to a division by zero in the gamma equation.\n"
            "5. The input rows cannot be less than one because that will lead to an invalid input in the program.\n"
            "6. After entering the values, click 'Submit' to process the inputs.\n"
            "7. Use the 'Go Back' button to return to the previous screen.\n"
            "8. Ensure the file has at least 4 lines of data."
        )

        tk.Label(instructions_window, text=instructions_text, justify="left", padx=10, pady=10).pack()
        tk.Button(instructions_window, text="Close", command=instructions_window.destroy).pack(pady=10)

    def go_back(self):
        self.root.destroy()
        root = tk.Tk()
        self.parent_app_class(root, process_callback=self.process_callback)

    def highlight_invalid_entries(self):
        invalid_inputs = False
        for entry_pair, error_label in zip(self.entries, self.error_labels):
            for entry in entry_pair:
                try:
                    value = int(entry.get())  # Try to convert to int to check validity
                    error_label.config(text="")
                    entry.configure(highlightbackground="black", highlightcolor="black", highlightthickness=1)
                except ValueError:
                    error_label.config(text="Invalid input", fg="red")
                    entry.configure(highlightbackground="red", highlightcolor="red", highlightthickness=1)
                    invalid_inputs = True
        return invalid_inputs

    def process_second_page_inputs(self):
        gamma = 4/3 if self.gamma_var.get() == "relativistic" else 5.0 / 3.0

        if self.highlight_invalid_entries():
            return

        starting_indices = []
        for entry_pair in self.entries:
            row = int(entry_pair[0].get())
            col = int(entry_pair[1].get())
            starting_indices.append((row, col))

        if len(starting_indices) != 2:
            messagebox.showerror("Input Error", "Please provide indices for both pressure and energy density.")
            return

        row_pressure, col_pressure = starting_indices[0]
        row_energy_density, col_energy_density = starting_indices[1]

        try:
            p0 = float(self.file_data[row_pressure][col_pressure])
            rho0 = float(self.file_data[row_energy_density][col_energy_density])
        except (IndexError, ValueError):
            messagebox.showerror("Input Error", "Invalid indices or data format in file.")
            return

        # Prepare inputs dictionary
        inputs = {
            'gamma': gamma,
            'radius': 1000,  # default radius
            'k': 1e-5,  # default k value
            'p0': p0,
            'rho0': rho0
        }

        # Call the main process with these inputs
        self.process_callback(inputs)

if __name__ == "__main__":
    root = tk.Tk()
    sample_data = process_file("sample_data.txt")  # Replace with a valid file path
    app = FileValidatorApp(root, sample_data, process_callback=lambda inputs: print(f"Processed inputs: {inputs}"), parent_app_class=InputValidatorApp)
    root.mainloop()

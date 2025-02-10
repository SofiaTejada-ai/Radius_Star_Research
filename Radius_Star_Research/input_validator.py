import tkinter as tk
from tkinter import filedialog, messagebox
import re
from file_validator import process_file, FileValidatorApp  # Import correctly

class InputValidatorApp:
    def __init__(self, root, process_callback):
        self.process_callback = process_callback
        self.root = root
        self.root.title("Input Validator")
        self.entries = []
        self.error_labels = []
        self.entry_frames = []

        self.create_main_page()

    def create_main_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.entries = []
        self.error_labels = []
        self.entry_frames = []

        # Title
        self.title_label = tk.Label(self.root, text="Welcome to Neutron Star Graphs", font=("Helvetica", 16))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Input fields
        self.create_input_row("Enter gamma (must be greater than 0)", 1)
        self.create_input_row("Enter radius (must be greater than 0)", 2)
        self.create_input_row("Enter starting pressure (must be greater than 0)", 3)
        self.create_input_row("Enter polytropic index K (must be greater than 0)", 4)

        # Submit button
        self.submit_button = tk.Button(self.root, text="Submit", command=self.validate_inputs)
        self.submit_button.grid(row=10, column=1, pady=10)

        # Clear button
        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_inputs)
        self.clear_button.grid(row=10, column=0, pady=10)

        # File input
        self.file_input_label = tk.Label(self.root, text="Or input file here")
        self.file_input_label.grid(row=12, column=0, padx=10, pady=(20, 5), sticky='e')

        self.file_input_button = tk.Button(self.root, text="Import file", command=self.load_file)
        self.file_input_button.grid(row=12, column=1, padx=10, pady=(20, 5), sticky='w')

    def create_input_row(self, label_text, row):
        label = tk.Label(self.root, text=label_text)
        label.grid(row=row * 2, column=0, padx=10, pady=5, sticky='e')

        frame = tk.Frame(self.root, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        frame.grid(row=row * 2, column=1, padx=10, pady=5, sticky='w')
        entry = tk.Entry(frame, width=30)
        entry.pack()

        error_label = tk.Label(self.root, text="", fg="red")
        error_label.grid(row=row * 2 + 1, column=1, padx=10, pady=(0, 5), sticky='w')

        self.entries.append(entry)
        self.error_labels.append(error_label)
        self.entry_frames.append(frame)

    def validate_inputs(self):
        valid = True
        self.clear_errors()

        # Regular expression for a valid mathematical expression
        valid_expression = re.compile(r'^[0-9.+\-*/\s()e]*$')

        for i, entry in enumerate(self.entries):
            input_text = entry.get()
            if not valid_expression.match(input_text):
                self.set_error(i, "Invalid input. Please insert a valid number expression greater than 0.")
                valid = False
                continue
            try:
                value = float(eval(input_text))
                if value <= 0:
                    self.set_error(i, "Invalid input. Please insert a number greater than 0.")
                    valid = False
            except (ValueError, SyntaxError):
                self.set_error(i, "Invalid input. Please insert a valid number expression greater than 0.")
                valid = False

        if valid:
            inputs = {
                'gamma': float(eval(self.entries[0].get())),
                'radius': float(eval(self.entries[1].get())),
                'p0': float(eval(self.entries[2].get())),
                'k': float(eval(self.entries[3].get()))
            }
            self.process_callback(inputs)

    def clear_errors(self):
        for frame in self.entry_frames:
            frame.config(highlightbackground="black", highlightcolor="black")
        for label in self.error_labels:
            label.config(text="")

    def set_error(self, index, message):
        self.entry_frames[index].config(highlightbackground="red", highlightcolor="red")
        self.error_labels[index].config(text=message)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            file_data = process_file(file_path)
            if file_data:
                self.root.destroy()  # Destroy current window before opening new one
                FileValidatorApp(tk.Tk(), file_data, self.process_callback, InputValidatorApp)
            else:
                messagebox.showerror("File Error", "Failed to process the file. Please ensure it has the correct format.")

    def clear_inputs(self):
        for entry in self.entries:
            entry.delete(0, tk.END)
        self.clear_errors()

# Example usage if running standalone:
if __name__ == "__main__":
    root = tk.Tk()
    app = InputValidatorApp(root, process_callback=lambda inputs: print(f"Processed inputs: {inputs}"))
    root.mainloop()



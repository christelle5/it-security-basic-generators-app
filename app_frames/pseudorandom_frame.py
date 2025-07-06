import tkinter as tk
import time
from tkinter import ttk, messagebox, scrolledtext

from app_frames.main_frame import MainFrame
from app_methods.pseudorandom_generator import Generator
from app_methods.loadconfig import LoadConfig


class SequenceGeneratorFrame(tk.Frame):

    generated_sequence = None
    generated_params = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.label_m = ttk.Label(self, text="Modulus, m: ")
        self.label_a = ttk.Label(self, text="Multiplier, a: ")
        self.label_c = ttk.Label(self, text="Increment, c: ")
        self.label_x0 = ttk.Label(self, text="Initial value, x0: ")
        self.label_k = ttk.Label(self, text="Number of values: ")

        self.entry_m = ttk.Entry(self)
        self.entry_a = ttk.Entry(self)
        self.entry_c = ttk.Entry(self)
        self.entry_x0 = ttk.Entry(self)
        self.entry_k = ttk.Entry(self)

        self.numbers = None
        self.period = None

        self.generate_button = ttk.Button(self, text="Generate", command=self.generate_sequence)
        self.save_button = ttk.Button(self, text="Save to File", command=self.save_to_file)
        self.load_config_button = ttk.Button(self, text="Load Configuration", command=self.load_configuration)
        self.back_button = ttk.Button(self, text="Back to Main Menu", command=lambda: self.controller.show_frame(MainFrame))

        self.period_label = ttk.Label(self, text="")
        self.sequence_text = scrolledtext.ScrolledText(self, height=20, width=40, exportselection=1)

        self.label_m.grid(column=0, row=0, sticky="w", padx=10, pady=5)
        self.label_a.grid(column=0, row=1, sticky="w", padx=10, pady=5)
        self.label_c.grid(column=0, row=2, sticky="w", padx=10, pady=5)
        self.label_x0.grid(column=0, row=3, sticky="w", padx=10, pady=5)
        self.label_k.grid(column=0, row=4, sticky="w", padx=10, pady=5)

        self.entry_m.grid(column=1, row=0, padx=10, pady=5)
        self.entry_a.grid(column=1, row=1, padx=10, pady=5)
        self.entry_c.grid(column=1, row=2, padx=10, pady=5)
        self.entry_x0.grid(column=1, row=3, padx=10, pady=5)
        self.entry_k.grid(column=1, row=4, padx=10, pady=5)

        self.back_button.grid(column=2, row=0, padx=10, pady=5)
        self.load_config_button.grid(column=2, row=1, padx=5, pady=5)
        self.generate_button.grid(column=2, row=2, padx=10, pady=5)
        self.save_button.grid(column=2, row=3, padx=10, pady=5)

        self.period_label.grid(column=0, row=6, padx=5, pady=10, columnspan=2, sticky=tk.W)
        self.sequence_text.grid(column=0, row=7, columnspan=6, rowspan=3, sticky='nsew')
        self.columnconfigure(5, weight=1)
        self.rowconfigure(7, weight=1)
        self.sequence_text.config(state="disabled")

        # self.bind("<Configure>", self.on_window_resize)

    def load_configuration(self):
        config = LoadConfig.load_configuration("../config1.json", config_type="pseudorandom")
        if not config.get("error"):
            self.update_ui_with_config(config.get("configuration"))
        else:
            self.update_ui_with_config(config.get("configuration"))
            messagebox.showerror("Error", str(config.get("error")))

    def update_ui_with_config(self, config):
        self.entry_m.delete(0, tk.END)
        self.entry_a.delete(0, tk.END)
        self.entry_c.delete(0, tk.END)
        self.entry_x0.delete(0, tk.END)
        self.entry_m.insert(0, str(config["modulus"]))
        self.entry_a.insert(0, str(config["multiplier"]))
        self.entry_c.insert(0, str(config["increment"]))
        self.entry_x0.insert(0, str(config["initial_value"]))

    def generate_sequence(self):
        try:
            m = int(self.entry_m.get())
            a = int(self.entry_a.get())
            c = int(self.entry_c.get())
            x0 = int(self.entry_x0.get())
            k = int(self.entry_k.get())
        except ValueError:
            messagebox.showerror("Error", "Please, enter valid integer values for all fields.")
            return
        if k < 0:
            messagebox.showerror("Error", "Number of values (k) must be greater than or equal to 0. Please, try again.")
            return
        if a > 100000:
            messagebox.showerror("Error", "Multiplier (a) must be less than or equal to 10^5. Please, try again.")
            return
        if m > 10000000:
            messagebox.showerror("Error", "Modulus (m) must be less than or equal to 10^7. Please, try again.")
            return
        if k > 8000:
            messagebox.showerror("Error", "Number of values (k) must be less than or equal to 8000. Please, try again.")
            return
        if m <= 0:
            messagebox.showerror("Error", "Modulus (m) must be greater than 0. Please, try again.")
            return

        generator = Generator(m, a, c, x0, k)
        result = generator.generate()

        self.generated_sequence = result.get("sequence")
        self.generated_params = {
            "m": m,
            "a": a,
            "c": c,
            "x0": x0,
            "k": k,
            "period": result.get("period")
        }

        self.numbers = result.get("sequence")
        self.period = result.get("period")
        self.period_label.config(text="Period of the generation function: " + str(result.get("period")))
        self.sequence_text.config(state="normal")
        self.sequence_text.delete("1.0", "end")
        self.sequence_text.insert("end", ', '.join(map(str, result.get("sequence"))))
        self.sequence_text.config(state="disabled")

    def save_to_file(self):

        if self.generated_sequence is None or self.generated_params is None:
            messagebox.showwarning("Warning", "Please, generate the sequence by pressing button 'Generate' before "
                                              "saving.")
            return

        try:
            m = self.generated_params["m"]
            a = self.generated_params["a"]
            c = self.generated_params["c"]
            x0 = self.generated_params["x0"]
            k = self.generated_params["k"]
            sequence_to_display = self.generated_sequence
            p = self.generated_params["period"]

            current_time = time.localtime()
            time_str = time.strftime("%d-%m-%Y_%H-%M-%S", current_time)
            filename = f"result_pseudorandom_{time_str}.txt"

            with open(filename, "w", encoding="utf-8") as fo:
                fo.write("Modulus, m: " + str(m) + '\n')
                fo.write("Multiplier, a: " + str(a) + '\n')
                fo.write("Increment, c: " + str(c) + '\n')
                fo.write("Initial value, x0: " + str(x0) + '\n')
                fo.write("Number of values: " + str(k) + '\n')
                fo.write("Period of the generation function: " + str(p) + '\n')
                fo.write("Original sequence:\n")
                fo.write(', '.join(map(str, sequence_to_display)))

            messagebox.showinfo("Success", "Data successfully saved to " + filename)

            # Чистимо згенеровану послідовність та її параметри після збереження у файл
            self.generated_sequence = None
            self.generated_params = None

        except Exception as e:
            messagebox.showerror("Error", "Please, enter valid integer values for all fields.")

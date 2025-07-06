import tkinter as tk
import os
from tkinter import ttk, messagebox, scrolledtext

from app_frames.main_frame import MainFrame
from app_methods.md5_generator import MD5


class MD5FrameCheck(tk.Frame):

    def __init__(self, parent, controller):
        from app_frames.md5_frame_text import MD5FrameText
        from app_frames.md5_frame_file import MD5FrameFile
        tk.Frame.__init__(self, parent)

        self.result_hash = None
        self.input_filename = None

        self.controller = controller
        self.label_input_data = ttk.Label(self, text="Name of the file: ")
        self.entry_input_data = ttk.Entry(self)
        self.label_input_hash = ttk.Label(self, text="Hash to check: ")
        self.entry_input_hash = ttk.Entry(self)

        self.generate_button = ttk.Button(self, text="Check the Hash", command=self.check_hash)
        self.back_button = ttk.Button(self, text="Back to Main Menu",
                                      command=lambda: self.controller.show_frame(MainFrame))
        self.hash_text_button = ttk.Button(self, text="Hash the Text",
                                           command=lambda: self.controller.show_frame(MD5FrameText))
        self.check_hash_button = ttk.Button(self, text="Hash the File",
                                            command=lambda: self.controller.show_frame(MD5FrameFile))

        self.result_label = ttk.Label(self, text="Actual hash:")
        self.hash_text = scrolledtext.ScrolledText(self, height=20, width=40, exportselection=1)

        self.label_input_data.grid(column=0, row=0, sticky="w", padx=10, pady=5)
        self.label_input_hash.grid(column=0, row=1, sticky="w", padx=10, pady=5)
        self.entry_input_data.grid(column=1, row=0, padx=10, pady=5)
        self.entry_input_hash.grid(column=1, row=1, padx=10, pady=5)

        self.back_button.grid(column=2, row=0, padx=10, pady=5)
        self.hash_text_button.grid(column=2, row=1, padx=10, pady=5)
        self.check_hash_button.grid(column=2, row=2, padx=10, pady=5)
        self.generate_button.grid(column=2, row=3, padx=10, pady=5)

        self.result_label.grid(column=0, row=6, padx=5, pady=10, columnspan=2, sticky=tk.W)
        self.hash_text.grid(column=0, row=7, columnspan=6, rowspan=3, sticky='nsew')
        self.columnconfigure(5, weight=1)
        self.rowconfigure(7, weight=1)
        self.hash_text.config(state="disabled")

        # self.bind("<Configure>", self.on_window_resize)

    def check_hash(self):
        try:
            message = str(self.entry_input_data.get())
            inp_hash = str(self.entry_input_hash.get())
            contains_upper = any(char.isupper() for char in inp_hash)

        except ValueError:
            messagebox.showerror("Error", "Please, enter the valid name of the file in 'filename' format "
                                          "(without '.txt') and valid hash.")
            return

        if len(message) > 256:
            messagebox.showerror("Error", "The length of file name is too big (must be <256 characters). Please, "
                                          "check it up and try again.")
            return

        if len(message) == 0:
            messagebox.showerror("Error", "Please, enter the name of the file in 'filename' format (without '.txt').")
            return

        if not os.path.isfile(message + ".txt"):
            messagebox.showerror("Error", f"The file '{message}.txt' does not exist. Please, check it up and try "
                                          f"again. Remember: the name of the file should be in 'filename' format "
                                          f"(without '.txt').")
            return

        if len(inp_hash) == 0:
            messagebox.showerror("Error", f"Please, enter the hash you have for the file '{message}.txt'.")
            return

        if len(inp_hash) != 32:
            messagebox.showerror("Error", "The length of hash should be 32 characters 0-9, a-z. Please, try again.")
            return

        if contains_upper:
            messagebox.showerror("Error", "All the letters a-z in the hash should be lowercase. Please, try again.")
            return

        file_size = os.path.getsize(message + ".txt")

        if 3 * 1024 * 1024 < file_size < 5 * 1024 * 1024:  # між 3 та 4.5 МБ, то трохи повільніше буде
            messagebox.showinfo("Wait for a while", "Please, be patient. The file is a bit big. The program will "
                                                    "generate hash of it. Data processing may last for a few seconds.")

        if file_size > 5 * 1024 * 1024:  # 5 МБ
            messagebox.showerror("Error", "The file size is too large. Please, check it and try again.")
            return

        with open(message + ".txt", "r", encoding="utf-8") as file:
            file_contents = file.read()

        md5_obj = MD5()
        result = md5_obj.md5(file_contents)
        self.result_hash = result
        self.input_filename = message

        self.hash_text.config(state="normal")
        self.hash_text.delete("1.0", "end")
        self.hash_text.insert("end", result)
        self.hash_text.config(state="disabled")

        if inp_hash == str(result):
            messagebox.showinfo("Success!", "Hashes are the same.")
        else:
            messagebox.showerror("Failure!", "Hashes are different, your hash is not correct.")

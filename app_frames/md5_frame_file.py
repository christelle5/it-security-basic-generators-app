import tkinter as tk
import time
import os
from tkinter import ttk, messagebox, scrolledtext

from app_frames.main_frame import MainFrame
from app_methods.md5_generator import MD5


class MD5FrameFile(tk.Frame):

    def __init__(self, parent, controller):
        from app_frames.md5_frame_text import MD5FrameText
        from app_frames.md5_frame_check import MD5FrameCheck
        tk.Frame.__init__(self, parent)

        self.result_hash = None
        self.input_filename = None

        self.controller = controller
        self.label_filename = ttk.Label(self, text="Name of the file: ")
        self.entry_filename = ttk.Entry(self)

        self.generate_button = ttk.Button(self, text="Generate", command=self.generate_hash)
        self.save_button = ttk.Button(self, text="Save to File", command=self.save_to_file)
        self.back_button = ttk.Button(self, text="Back to Main Menu",
                                      command=lambda: self.controller.show_frame(MainFrame))
        self.hash_text_button = ttk.Button(self, text="Hash the Text",
                                           command=lambda: self.controller.show_frame(MD5FrameText))
        self.check_hash_button = ttk.Button(self, text="Check the Hash",
                                            command=lambda: self.controller.show_frame(MD5FrameCheck))

        self.result_label = ttk.Label(self, text="Your hash:")
        self.hash_text = scrolledtext.ScrolledText(self, height=20, width=40, exportselection=1)

        self.label_filename.grid(column=0, row=0, sticky="w", padx=10, pady=5)

        self.entry_filename.grid(column=1, row=0, padx=10, pady=5)

        self.back_button.grid(column=2, row=0, padx=10, pady=5)
        self.hash_text_button.grid(column=2, row=1, padx=10, pady=5)
        self.check_hash_button.grid(column=2, row=2, padx=10, pady=5)
        self.generate_button.grid(column=2, row=3, padx=10, pady=5)
        self.save_button.grid(column=2, row=4, padx=10, pady=5)

        self.result_label.grid(column=0, row=6, padx=5, pady=10, columnspan=2, sticky=tk.W)
        self.hash_text.grid(column=0, row=7, columnspan=6, rowspan=3, sticky='nsew')
        self.columnconfigure(5, weight=1)
        self.rowconfigure(7, weight=1)
        self.hash_text.config(state="disabled")

        # self.bind("<Configure>", self.on_window_resize)

    def generate_hash(self):
        try:
            message = str(self.entry_filename.get())

        except ValueError:
            messagebox.showerror("Error", "Please, enter the valid name of the file in 'filename' format "
                                          "(without '.txt').")
            return

        if len(message) > 256:
            messagebox.showerror("Error", "The length of file name is too big. Please, check it up and try again.")
            return

        if len(message) == 0:
            messagebox.showerror("Error", "Please, enter the name of the file in 'filename' format (without '.txt').")
            return

        if not os.path.isfile(message + ".txt"):
            messagebox.showerror("Error", f"The file '{message}.txt' does not exist. Please, check it up and try "
                                          f"again. Remember: the name of the file should be in 'filename' format "
                                          f"(without '.txt').")
            return

        file_size = os.path.getsize(message + ".txt")

        if 3 * 1024 * 1024 < file_size < 5 * 1024 * 1024:  # між 3 та 4.5 МБ, то трохи повільніше буде
            messagebox.showinfo("Wait for a while", "Please, be patient. The file is a bit big. Data processing "
                                                    "may last for a few seconds.")

        if file_size > 5 * 1024 * 1024:  # 5 МБ
            messagebox.showerror("Error", "The file size is too large. Please, check it and try again.")
            return

        with open(message + ".txt", "r", encoding="utf-8") as file:
            file_contents = file.read()

        md5_obj = MD5()
        result = md5_obj.md5(file_contents)
        print(file_contents)
        self.result_hash = result
        self.input_filename = message

        self.hash_text.config(state="normal")
        self.hash_text.delete("1.0", "end")
        self.hash_text.insert("end", result)
        self.hash_text.config(state="disabled")

    def save_to_file(self):

        if self.result_hash is None:
            messagebox.showwarning("Warning", "Please, generate the hash by pressing button 'Generate' before saving.")
            return

        try:
            current_time = time.localtime()
            time_str = time.strftime("%d-%m-%Y_%H-%M-%S", current_time)
            filename = f"result_md5_{time_str}.txt"

            with open(filename, "w", encoding="utf-8") as fo:
                fo.write("Input file:")
                fo.write('\n')
                fo.write(self.input_filename)
                fo.write('\n')
                fo.write("Hash: " + str(self.result_hash) + '\n')
            fo.close()

            messagebox.showinfo("Success", "Data successfully saved to " + filename)

            # Чистимо згенеровану послідовність та її параметри після збереження у файл
            self.result_hash = None
            self.input_filename = None

        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Please, enter valid integer values for all fields.")

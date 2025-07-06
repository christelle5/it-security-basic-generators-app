import tkinter as tk
import time
from tkinter import ttk, messagebox, scrolledtext

from app_frames.main_frame import MainFrame
from app_methods.md5_generator import MD5


class MD5FrameText(tk.Frame):

    def __init__(self, parent, controller):
        from app_frames.md5_frame_file import MD5FrameFile
        from app_frames.md5_frame_check import MD5FrameCheck
        tk.Frame.__init__(self, parent)

        self.result_hash = None
        self.input_text = None

        self.controller = controller
        self.label_message = ttk.Label(self, text="Message to hash: ")

        self.entry_message = ttk.Entry(self)

        self.generate_button = ttk.Button(self, text="Generate", command=self.generate_hash)
        self.save_button = ttk.Button(self, text="Save to File", command=self.save_to_file)
        self.back_button = ttk.Button(self, text="Back to Main Menu",
                                      command=lambda: self.controller.show_frame(MainFrame))
        self.hash_file_button = ttk.Button(self, text="Hash the File",
                                           command=lambda: self.controller.show_frame(MD5FrameFile))
        self.check_hash_button = ttk.Button(self, text="Check the Hash",
                                            command=lambda: self.controller.show_frame(MD5FrameCheck))

        self.result_label = ttk.Label(self, text="Your hash:")
        self.hash_text = scrolledtext.ScrolledText(self, height=20, width=40, exportselection=1)

        self.label_message.grid(column=0, row=0, sticky="w", padx=10, pady=5)

        self.entry_message.grid(column=1, row=0, padx=10, pady=5)

        self.back_button.grid(column=2, row=0, padx=10, pady=5)
        self.hash_file_button.grid(column=2, row=1, padx=10, pady=5)
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
            message = str(self.entry_message.get())

        except ValueError:
            messagebox.showerror("Error", "Please, enter the string you want to hash (256 chars maximum).")
            return

        if len(message) > 256:
            messagebox.showerror("Error", "The length of message is too big. Please, try to make a txt file with "
                                          "message, go to Hash the file page using button Hash the file, and "
                                          "try again.")
            return

        if len(message) == 0:
            messagebox.showerror("Error", "The message is an empty string. Please, write the message and try again.")
            return

        md5_obj = MD5()
        result = md5_obj.md5(message)
        self.result_hash = result
        self.input_text = message

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
                fo.write("Input text:")
                fo.write('\n')
                fo.write(self.input_text)
                fo.write('\n')
                fo.write("Hash: " + str(self.result_hash) + '\n')
            fo.close()

            messagebox.showinfo("Success", "Data successfully saved to " + filename)

            # Чистимо згенеровану послідовність та її параметри після збереження у файл
            self.result_hash = None
            self.input_text = None

        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Please, enter valid integer values for all fields.")

import tkinter as tk
import time
import os
from tkinter import ttk, messagebox

from app_frames.main_frame import MainFrame
from app_methods.loadconfig import LoadConfig
from app_methods.rc5_generator import RC5


def load_configuration():
    config = LoadConfig.load_configuration("../config3.json", config_type="rc5")
    if not config.get("error"):
        return config.get("configuration")
    else:
        messagebox.showerror("Error", str(config.get("error")))
        return config.get("configuration")


class RC5FrameEncode(tk.Frame):

    def __init__(self, parent, controller):
        from app_frames.rc5_frame_decode import RC5FrameDecode
        tk.Frame.__init__(self, parent)

        self.configurations = None

        self.controller = controller
        self.label_message = ttk.Label(self, text="Your key: ")
        self.label_filename = ttk.Label(self, text="File to encode: ")
        self.entry_message = ttk.Entry(self)
        self.entry_filename = ttk.Entry(self)

        self.generate_button = ttk.Button(self, text="Encode", command=self.encode_file)
        self.back_button = ttk.Button(self, text="Back to Main Menu",
                                      command=lambda: self.controller.show_frame(MainFrame))
        self.decode_file_button = ttk.Button(self, text="Go to Decode File Page",
                                             command=lambda: self.controller.show_frame(RC5FrameDecode))

        self.label_message.grid(column=0, row=0, sticky="w", padx=10, pady=5)
        self.label_filename.grid(column=0, row=1, sticky="w", padx=10, pady=5)
        self.entry_message.grid(column=1, row=0, padx=10, pady=5)
        self.entry_filename.grid(column=1, row=1, padx=10, pady=5)

        self.back_button.grid(column=2, row=0, padx=10, pady=5)
        self.decode_file_button.grid(column=2, row=1, padx=10, pady=5)
        self.generate_button.grid(column=2, row=3, padx=10, pady=5)

        self.columnconfigure(5, weight=1)
        self.rowconfigure(5, weight=1)

    def encode_file(self):
        try:
            file_name = str(self.entry_filename.get())
            inp_key = str(self.entry_message.get())

        except ValueError:
            messagebox.showerror("Error", "Please, enter the valid name of the file in 'filename.format' format "
                                          "and valid hash.")
            return

        if len(file_name) > 256:
            messagebox.showerror("Error", "The length of file name is too big (must be <256 characters). Please, "
                                          "check it up and try again.")
            return

        if len(inp_key) > 256:
            messagebox.showerror("Error", "The length of key is too big (must be <256 characters). Please, "
                                          "check it up and try again.")
            return

        if len(file_name) == 0:
            messagebox.showerror("Error", "Please, enter the name of the file in 'filename.format' format).")
            return

        if not os.path.isfile(file_name):
            messagebox.showerror("Error", f"The file '{file_name}' does not exist. Please, check it up and try "
                                          f"again. Remember: the name of the file should be in 'filename.format' "
                                          f"format.")
            return

        if len(inp_key) == 0:
            messagebox.showerror("Error", f"Please, enter the hash you have for the file '{file_name}'.")
            return

        file_size = os.path.getsize(file_name)

        if 3 * 1024 * 1024 < file_size < 5 * 1024 * 1024:  # між 3 та 4.5 МБ, то трохи повільніше буде
            messagebox.showinfo("Wait for a while", "Please, be patient. The file is a bit big. The program will "
                                                    "generate hash of it. Data processing may last for a few seconds.")

        if file_size > 5 * 1024 * 1024:  # 5 МБ
            messagebox.showerror("Error", "The file size is too large. Please, check it and try again.")
            return

        self.configurations = load_configuration()
        rc5_obj = RC5(RC5.get_md5_key(inp_key), self.configurations['w'], self.configurations['r'])
        current_time = time.localtime()
        time_str = time.strftime("%d-%m-%Y_%H-%M-%S", current_time)
        output_filename = f"result_{time_str}" + "_encoded_" + str(file_name)
        result = rc5_obj.encode_file(str(file_name), output_filename)

        if result:
            messagebox.showinfo("Success", "File was successfully encoded. Encoded text was saved "
                                           "in '" + str(output_filename) + "'.")

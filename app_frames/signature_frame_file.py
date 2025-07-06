import tkinter as tk
import os
import time
from tkinter import ttk, messagebox, scrolledtext

from app_frames.main_frame import MainFrame
from app_methods.signature_generator import SignatureGenerator


class SignatureFrameFile(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.input_file = None
        self.public_key = None
        self.private_key = None

        from app_frames.signature_frame_text import SignatureFrameText
        from app_frames.signature_frame_check import SignatureFrameCheck

        self.result_signed_message = None
        self.input_text = None

        self.controller = controller
        self.label_message = ttk.Label(self, text="File to sign: ")
        self.entry_message = ttk.Entry(self)
        self.label_private_key_file = ttk.Label(self, text="Private key file:")
        self.entry_private_key_file = ttk.Entry(self)

        self.generate_button = ttk.Button(self, text="Generate two keys", command=self.generate_pair_of_keys)
        self.sign_button = ttk.Button(self, text="Sign this File", command=self.sign_message)
        self.save_button = ttk.Button(self, text="Save to File", command=self.save_to_file)
        self.back_button = ttk.Button(self, text="Back to Main Menu",
                                      command=lambda: self.controller.show_frame(MainFrame))
        self.sign_file_button = ttk.Button(self, text="Sign the Text",
                                           command=lambda: self.controller.show_frame(SignatureFrameText))
        self.check_sign_button = ttk.Button(self, text="Check the Sign",
                                            command=lambda: self.controller.show_frame(SignatureFrameCheck))

        self.result_label = ttk.Label(self, text="Signed message:")
        self.signed_text = scrolledtext.ScrolledText(self, height=20, width=40, exportselection=1)

        self.label_message.grid(column=0, row=0, sticky="w", padx=10, pady=5)
        self.label_private_key_file.grid(column=0, row=1, sticky="w", padx=10, pady=5)

        self.entry_message.grid(column=1, row=0, padx=10, pady=5)
        self.entry_private_key_file.grid(column=1, row=1, padx=10, pady=5)

        self.back_button.grid(column=2, row=0, padx=10, pady=5)
        self.sign_file_button.grid(column=2, row=1, padx=10, pady=5)
        self.check_sign_button.grid(column=2, row=2, padx=10, pady=5)
        self.generate_button.grid(column=2, row=3, padx=10, pady=5)
        self.sign_button.grid(column=2, row=4, padx=10, pady=5)
        self.save_button.grid(column=2, row=5, padx=10, pady=5)

        self.result_label.grid(column=0, row=6, padx=5, pady=10, columnspan=2, sticky=tk.W)
        self.signed_text.grid(column=0, row=7, columnspan=6, rowspan=3, sticky='nsew')
        self.columnconfigure(5, weight=1)
        self.rowconfigure(7, weight=1)
        self.signed_text.config(state="disabled")

    def generate_pair_of_keys(self):

        dsa_obj = SignatureGenerator()
        result = dsa_obj.get_pair_of_key()
        res1 = "private_" + result
        res2 = "public_" + result
        mess = "The pair of public and private keys was successfully created and saved in '" + res2 + "' and '"\
               + res1 + "'."
        if result:
            messagebox.showinfo("Success", mess)

    def sign_message(self):
        try:
            message = str(self.entry_message.get())
            private_key = str(self.entry_private_key_file.get())

        except ValueError:
            messagebox.showerror("Error", "Please, enter valid filenames for file you want to sign and file with "
                                          "private key (the last one is in .pem format).")
            return

        if len(message) > 256:
            messagebox.showerror("Error", "The length of file with message is too big (must be <256 characters). "
                                          "Please, check it up and try again.")
            return

        if len(message) == 0:
            messagebox.showerror("Error", "Please, enter the name of the file with message and try again.")
            return

        if len(private_key) > 256:
            messagebox.showerror("Error", "The length of file with private key is too big (must be <256 characters). "
                                          "Please, check it up and try again.")
            return

        if len(private_key) == 0:
            messagebox.showerror("Error", "Please, enter the name of the file with private key as 'filename.format' "
                                          "where 'format' is '.pem'.")
            return

        if not os.path.isfile(message):
            messagebox.showerror("Error", f"The file '{message}' does not exist. Please, check it up and try again.")
            return

        if not os.path.isfile(private_key):
            messagebox.showerror("Error", f"The file '{private_key}' does not exist. Please, check it up and try "
                                          f"again. Remember: the name of the file should be as 'filename.format' "
                                          f"where 'format' is '.pem'.")
            return

        if private_key[-4:] != '.pem':
            messagebox.showinfo("Error", f"The file '{private_key}' is not in .rem format, but should be. "
                                         f"Check it up and try again.")
            return

        file_size = os.path.getsize(message)

        if file_size > 5 * 1024 * 1024:  # 5 МБ
            messagebox.showerror("Error", "The file size is too large. Please, check it and try again.")
            return

        with open(message, "rb") as file:
            file_contents = file.read()

        sign_gen_obj = SignatureGenerator()
        result = sign_gen_obj.sign(private_key, file_contents)
        self.result_signed_message = result
        self.input_text = message

        self.signed_text.config(state="normal")
        self.signed_text.delete("1.0", "end")
        self.signed_text.insert("end", result)
        self.signed_text.config(state="disabled")

    def save_to_file(self):

        if self.result_signed_message is None:
            messagebox.showwarning("Warning", "Please, sign the message by pressing button 'Sign' before saving.")
            return

        try:
            current_time = time.localtime()
            time_str = time.strftime("%d-%m-%Y_%H-%M-%S", current_time)
            filename = f"result_signed_{time_str}.txt"

            with open(filename, "w", encoding="utf-8") as fo:
                fo.write(str(self.result_signed_message))
            fo.close()

            messagebox.showinfo("Success", "Data successfully saved to " + filename)

            # Чистимо згенеровану послідовність та її параметри після збереження у файл
            self.result_signed_message = None
            self.input_text = None

        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Please, enter message you want to sign and try again.")

import tkinter as tk
import os
from tkinter import ttk, messagebox

from app_frames.main_frame import MainFrame
from app_methods.signature_generator import SignatureGenerator


class SignatureFrameCheck(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.input_file = None
        self.public_key = None
        self.private_key = None

        from app_frames.signature_frame_text import SignatureFrameText
        from app_frames.signature_frame_file import SignatureFrameFile

        self.result_signed_message = None
        self.input_text = None

        self.controller = controller
        self.label_message = ttk.Label(self, text="Initial file:")
        self.entry_message = ttk.Entry(self)
        self.label_public_key_file = ttk.Label(self, text="Public key file:")
        self.entry_public_key_file = ttk.Entry(self)
        self.label_signature_file = ttk.Label(self, text="Signature file:")
        self.entry_signature_file = ttk.Entry(self)

        self.check_button = ttk.Button(self, text="Verify the File", command=self.check_sign)
        self.back_button = ttk.Button(self, text="Back to Main Menu",
                                      command=lambda: self.controller.show_frame(MainFrame))
        self.sign_file_button = ttk.Button(self, text="Sign the Text",
                                           command=lambda: self.controller.show_frame(SignatureFrameText))
        self.check_sign_button = ttk.Button(self, text="Sign the File",
                                            command=lambda: self.controller.show_frame(SignatureFrameFile))

        self.label_message.grid(column=0, row=0, sticky="w", padx=10, pady=5)
        self.label_public_key_file.grid(column=0, row=1, sticky="w", padx=10, pady=5)
        self.label_signature_file.grid(column=0, row=2, sticky="w", padx=10, pady=5)

        self.entry_message.grid(column=1, row=0, padx=10, pady=5)
        self.entry_public_key_file.grid(column=1, row=1, padx=10, pady=5)
        self.entry_signature_file.grid(column=1, row=2, padx=10, pady=5)

        self.back_button.grid(column=2, row=0, padx=10, pady=5)
        self.sign_file_button.grid(column=2, row=1, padx=10, pady=5)
        self.check_sign_button.grid(column=2, row=2, padx=10, pady=5)
        self.check_button.grid(column=2, row=3, padx=10, pady=5)

        self.columnconfigure(5, weight=1)
        self.rowconfigure(7, weight=1)

    def check_sign(self):
        try:
            message = str(self.entry_message.get())
            public_key = str(self.entry_public_key_file.get())
            signature = str(self.entry_signature_file.get())

        except ValueError:
            messagebox.showerror("Error", "Please, enter valid filenames for file with signed message, file with "
                                          "public key (the last one is in .pem format), signature and try again.")
            return

        if len(message) > 256:
            messagebox.showerror("Error", "The length of name of file with initial message is too big (must be <256 "
                                          "characters). Please, check it up and try again.")
            return

        if len(message) == 0:
            messagebox.showerror("Error", "Please, enter the name of the file with initial message and try again.")
            return

        if len(signature) > 256:
            messagebox.showerror("Error", "The length of name of file with signed message is too big (must be <256 "
                                          "characters). Please, check it up and try again.")
            return

        if len(signature) == 0:
            messagebox.showerror("Error", "Please, enter the name of the file with signed message and try again.")
            return

        if len(public_key) > 256:
            messagebox.showerror("Error", "The length of name of file with public key is too big (must be <256 "
                                          "characters). Please, check it up and try again.")
            return

        if len(public_key) == 0:
            messagebox.showerror("Error", "Please, enter the name of the file with public key as 'filename.format' "
                                          "where 'format' is '.pem'.")
            return

        if not os.path.isfile(message):
            messagebox.showerror("Error", f"The file '{message}' does not exist. Please, check it up and try again.")
            return

        if not os.path.isfile(public_key):
            messagebox.showerror("Error", f"The file '{public_key}' does not exist. Please, check it up and try "
                                          f"again. Remember: the name of the file should be as 'filename.format' "
                                          f"where 'format' is '.pem'.")
            return

        if not os.path.isfile(signature):
            messagebox.showerror("Error", f"The file '{signature}' does not exist. Please, check it up and try again.")
            return

        if public_key[-4:] != '.pem':
            messagebox.showinfo("Error", f"The file '{public_key}' is not in .rem format, but should be. "
                                         f"Check it up and try again.")
            return

        file_size = os.path.getsize(message)

        if file_size > 5 * 1024 * 1024:  # 5 МБ
            messagebox.showerror("Error", "The initial file size is too large. Please, check it and try again.")
            return

        file_size = os.path.getsize(signature)

        if file_size > 256:  # 256 Байт
            messagebox.showerror("Error", "The file size of signed file is too large. Please, check it and try again.")
            return

        with open(message, "rb") as file:
            file_contents = file.read()

        with open(signature, "r") as file:
            signed_file = file.read()

        sign_gen_obj = SignatureGenerator()
        result = sign_gen_obj.verify(public_key, file_contents, signed_file)
        if result:
            messagebox.showinfo("Success!", "The signature is valid.")
        else:
            messagebox.showerror("Failure!", "The signature is not valid.")

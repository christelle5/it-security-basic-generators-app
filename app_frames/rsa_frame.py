import tkinter as tk
import os
from tkinter import ttk, messagebox, scrolledtext

from app_frames.main_frame import MainFrame
from app_methods.rsa_generator import RSAGenerator

import re


def check_public_key_format(file_name, status):
    if status == 'public':
        with open(file_name, 'r') as file:
            content = file.read()

            # Регулярний вираз для перевірки формату ключа, перевірка
            pattern = r'^-----BEGIN PUBLIC KEY-----\n(.+)\n-----END PUBLIC KEY-----$'
            match = re.match(pattern, content, re.DOTALL)

            if match:
                # Отримання ключа
                key_content = match.group(1)
                lines = key_content.split('\n')
                expected_num_lines = 4

                # перевірка кількості рядків
                if len(lines) != expected_num_lines:
                    return False

                # очікувана довжина символів у кожному рядку
                expected_lengths = [64, 64, 64, 24]

                for i, line in enumerate(lines):
                    if len(line) != expected_lengths[i]:
                        return False
                return True

            else:
                return False

    elif status == 'private':
        with open(file_name, 'r') as file:
            content = file.read()

            # Регулярний вираз для перевірки формату ключа
            pattern = r'^-----BEGIN RSA PRIVATE KEY-----\n(.+)\n-----END RSA PRIVATE KEY-----$'
            match = re.match(pattern, content, re.DOTALL)

            if match:
                # Отримання ключа
                key_content = match.group(1)
                lines = key_content.split('\n')
                expected_num_lines = 13

                # перевірка кількості рядків
                if len(lines) != expected_num_lines:
                    return False

                # очікувана довжина символів у кожному рядку
                expected_lengths = [64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 44]

                for i, line in enumerate(lines):
                    if len(line) != expected_lengths[i]:
                        return False
                return True

            else:
                return False


class RSAFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.input_file = None
        self.public_key = None
        self.private_key = None
        self.key_example = "-----BEGIN PUBLIC KEY-----\nchars[64]\nchars[64]" \
                           "\nchars[64]\nchars[24]\n-----END PUBLIC KEY-----" \
                           "\n\n" \
                           "-----BEGIN RSA PRIVATE KEY-----\n" \
                           "chars[64]\nchars[64]\nchars[64]\nchars[64]\n" \
                           "chars[64]\nchars[64]\nchars[64]\nchars[64]\n" \
                           "chars[64]\nchars[64]\nchars[64]\nchars[64]\n" \
                           "chars[44]\n-----END RSA PRIVATE KEY-----"

        self.controller = controller
        self.label_input_file = ttk.Label(self, text="Input file:")
        self.entry_input_file = ttk.Entry(self)
        self.label_public_key_file = ttk.Label(self, text="Public key file:")
        self.entry_public_key_file = ttk.Entry(self)
        self.label_private_key_file = ttk.Label(self, text="Private key file:")
        self.entry_private_key_file = ttk.Entry(self)

        self.generate_button = ttk.Button(self, text="Generate two keys", command=self.generate_pair_of_keys)
        self.back_button = ttk.Button(self, text="Back to Main Menu",
                                      command=lambda: self.controller.show_frame(MainFrame))
        self.encryption_button = ttk.Button(self, text="Encrypt", command=self.encryption)
        self.decryption_button = ttk.Button(self, text="Decrypt", command=self.decryption)

        self.result_label = ttk.Label(self, text="Example of public/private key format:")
        self.some_text = scrolledtext.ScrolledText(self, height=20, width=40, exportselection=1)

        self.label_input_file.grid(column=0, row=0, sticky="w", padx=10, pady=5)
        self.label_public_key_file.grid(column=0, row=1, sticky="w", padx=10, pady=5)
        self.label_private_key_file.grid(column=0, row=2, sticky="w", padx=10, pady=5)
        self.entry_input_file.grid(column=1, row=0, padx=10, pady=5)
        self.entry_public_key_file.grid(column=1, row=1, padx=10, pady=5)
        self.entry_private_key_file.grid(column=1, row=2, padx=10, pady=5)

        self.back_button.grid(column=2, row=0, padx=10, pady=5)
        self.generate_button.grid(column=2, row=1, padx=10, pady=5)
        self.encryption_button.grid(column=2, row=2, padx=10, pady=5)
        self.decryption_button.grid(column=2, row=3, padx=10, pady=5)

        self.result_label.grid(column=0, row=6, padx=5, pady=10, columnspan=2, sticky=tk.W)
        self.some_text.grid(column=0, row=7, columnspan=6, rowspan=3, sticky='nsew')
        self.columnconfigure(5, weight=1)
        self.rowconfigure(7, weight=1)

        self.some_text.config(state="normal")
        self.some_text.delete("1.0", "end")
        self.some_text.insert("end", self.key_example)
        self.some_text.config(state="disabled")

        # self.bind("<Configure>", self.on_window_resize)

    def generate_pair_of_keys(self):

        rsa_obj = RSAGenerator()
        result = rsa_obj.get_pair_of_key()
        res1 = "private_" + result
        res2 = "public_" + result
        mess = "The pair of public and private keys was successfully created and saved in '" + res2 + "' and '" + res1 + "'."
        if result:
            messagebox.showinfo("Success", mess)

    def encryption(self):
        try:
            file_name = str(self.entry_input_file.get())
            public_key = str(self.entry_public_key_file.get())

        except ValueError:
            messagebox.showerror("Error", "Please, enter the valid name of the file in 'filename.format' format "
                                          "and valid name of the file with public key as 'filename.format'. Remember,"
                                          "file with public key should be in .pem format.")
            return

        if len(file_name) > 256:
            messagebox.showerror("Error", "The length of input file name is too big (must be <256 characters). Please, "
                                          "check it up and try again.")
            return

        if len(public_key) > 256:
            messagebox.showerror("Error", "The length of file with public key is too big (must be <256 characters). "
                                          "Please, check it up and try again.")
            return

        if len(file_name) == 0:
            messagebox.showerror("Error", "Please, enter the name of the input file as 'filename.format'.")
            return

        if len(public_key) == 0:
            messagebox.showerror("Error", "Please, enter the name of the file with public key as 'filename.format' "
                                          "where 'format' is '.pem'.")
            return

        if not os.path.isfile(file_name):
            messagebox.showerror("Error", f"The file '{file_name}' does not exist. Please, check it up and try "
                                          f"again. Remember: the name of the file should be in 'filename.format' "
                                          f"format.")
            return

        if not os.path.isfile(public_key):
            messagebox.showerror("Error", f"The file '{public_key}' does not exist. Please, check it up and try "
                                          f"again. Remember: the name of the file should be as 'filename.format' "
                                          f"where 'format' is '.pem'.")
            return

        file_size_inp = os.path.getsize(file_name)
        print(file_size_inp)

        if file_size_inp > 86:  # 86 байт, більше бібліотека не бере
            messagebox.showerror("Error", "The size of the input file is too large. Please, check it and try again.")
            return

        if not check_public_key_format(public_key, status='public'):
            messagebox.showerror("Error", "Invalid content format for public key file. It should look like the "
                                          "example. Please, check it up and try again.")
            return

        if public_key[-4:] != '.pem':
            messagebox.showinfo("Error", f"The file '{public_key}' is not in .rem format, but should be. "
                                         f"Check it up and try again.")
            return

        rsa_obj = RSAGenerator()
        res = rsa_obj.encrypt(file_name, public_key)
        if res:
            mess = "The input was successfully encrypted. The result was saved in '" + res + "'."
            messagebox.showinfo("Success", mess)

    def decryption(self):
        try:
            file_name = str(self.entry_input_file.get())
            private_key = str(self.entry_private_key_file.get())

        except ValueError:
            messagebox.showerror("Error", "Please, enter the valid name of the file in 'filename.format' format "
                                          "and valid name of the file with public key as 'filename.format'. Remember,"
                                          "file with private key should be in .pem format.")
            return

        if len(file_name) > 256:
            messagebox.showerror("Error", "The length of input file name is too big (must be <256 characters). Please, "
                                          "check it up and try again.")
            return

        if len(private_key) > 256:
            messagebox.showerror("Error", "The length of file with private key is too big (must be <256 characters). "
                                          "Please, check it up and try again.")
            return

        if len(file_name) == 0:
            messagebox.showerror("Error", "Please, enter the name of the input file as 'filename.format'.")
            return

        if len(private_key) == 0:
            messagebox.showerror("Error", "Please, enter the name of the file with private key as 'filename.format' "
                                          "where 'format' is '.pem'.")
            return

        if not os.path.isfile(file_name):
            messagebox.showerror("Error", f"The file '{file_name}' does not exist. Please, check it up and try "
                                          f"again. Remember: the name of the file should be in 'filename.format' "
                                          f"format.")
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

        file_size_inp = os.path.getsize(file_name)

        if file_size_inp > 6*1024:  # 86 байт, більше бібліотека не бере
            messagebox.showerror("Error", "The size of the input file is too large. Please, check it and try again.")
            return

        if not check_public_key_format(private_key, status='private'):
            messagebox.showerror("Error", "Invalid content format for private key file. It should look like the "
                                          "example. Please, check it up and try again.")

        rsa_obj = RSAGenerator()
        res = rsa_obj.decrypt(file_name, private_key)
        if res:
            mess = "The input was successfully encrypted. The result was saved in '" + res + "'."
            messagebox.showinfo("Success", mess)

import tkinter as tk


class MainFrame(tk.Frame):
    def __init__(self, parent, controller):
        from app_frames.pseudorandom_frame import SequenceGeneratorFrame
        from app_frames.md5_frame_text import MD5FrameText
        from app_frames.rc5_frame_encode import RC5FrameEncode
        from app_frames.rsa_frame import RSAFrame
        from app_frames.signature_frame_text import SignatureFrameText
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Menu", font=("Arial", 18, "bold"), fg="black")
        label.pack(pady=15, padx=15)
        button1 = tk.Button(self, text="Pseudorandom number generator",
                            command=lambda: controller.show_frame(SequenceGeneratorFrame))
        button2 = tk.Button(self, text="MD5",
                            command=lambda: controller.show_frame(MD5FrameText))
        button3 = tk.Button(self, text="RC5-CBC-Pad",
                            command=lambda: controller.show_frame(RC5FrameEncode))
        button4 = tk.Button(self, text="RSA",
                            command=lambda: controller.show_frame(RSAFrame))
        button5 = tk.Button(self, text="Digital signature (DSS)",
                            command=lambda: controller.show_frame(SignatureFrameText))
        button1.configure(bg="light blue", fg="black", font=("Arial", 12))
        button2.configure(bg="light blue", fg="black", font=("Arial", 12))
        button3.configure(bg="light blue", fg="black", font=("Arial", 12))
        button4.configure(bg="light blue", fg="black", font=("Arial", 12))
        button5.configure(bg="light blue", fg="black", font=("Arial", 12))
        button1.pack(padx=5, pady=5)
        button2.pack(padx=5, pady=5)
        button3.pack(padx=5, pady=5)
        button4.pack(padx=5, pady=5)
        button5.pack(padx=5, pady=5)

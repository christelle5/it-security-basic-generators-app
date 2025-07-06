import tkinter as tk
from app_frames.main_frame import MainFrame
from app_frames.pseudorandom_frame import SequenceGeneratorFrame
from app_frames.md5_frame_text import MD5FrameText
from app_frames.md5_frame_file import MD5FrameFile
from app_frames.md5_frame_check import MD5FrameCheck
from app_frames.rc5_frame_encode import RC5FrameEncode
from app_frames.rc5_frame_decode import RC5FrameDecode
from app_frames.rsa_frame import RSAFrame
from app_frames.signature_frame_text import SignatureFrameText
from app_frames.signature_frame_file import SignatureFrameFile
from app_frames.signature_frame_check import SignatureFrameCheck


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("IT Security Basic Generators")
        self.geometry("406x406")
        self.resizable(False, False)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainFrame, SequenceGeneratorFrame, MD5FrameText, MD5FrameFile,
                  MD5FrameCheck, RC5FrameEncode, RC5FrameDecode, RSAFrame,
                  SignatureFrameText, SignatureFrameFile, SignatureFrameCheck):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainFrame)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()

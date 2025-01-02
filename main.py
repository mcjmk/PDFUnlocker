#! python3
# PDFUnlocker - a simple script to remove passwords from your PDF files (assuming you know the password).
import threading
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os
import pypdf
import time

class PDFUnlocker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF Unlocker")

        self.input_folder = ""
        self.output_folder = ""
        self.password = ""

        tk.Button(self.root, text="Choose input directory", command=self.choose_input_folder).pack()
        tk.Button(self.root, text="Choose output directory", command=self.choose_output_folder).pack()
        self.password_entry = tk.Entry(self.root)
        self.password_entry.pack()
        self.password_entry.insert(0, "5836294137")
        tk.Button(self.root, text="Unlock PDFs", command=self.unlock_pdfs).pack()

        tk.Button(self.root, text="Exit", command=self.root.destroy).pack()

    def choose_input_folder(self):
        self.input_folder = filedialog.askdirectory(title="Choose input directory")
        print(f"Input directory: {self.input_folder}")

    def choose_output_folder(self):
        self.output_folder = filedialog.askdirectory(title="Choose output directory")
        print(f"Output dir: {self.output_folder}")

    def enter_password(self):
        self.password = simpledialog.askstring("Password", "Enter password: ", initialvalue="5836294137")

    def unlock_pdfs(self):
        if not self.input_folder:
            messagebox.showerror("Error", "Please choose input_folder!")
            return

        elif not self.output_folder:
            messagebox.showerror("Error", "Please choose input_folder!")
            return

        start_time = time.time()
        unlockThreads = []
        for filename in os.listdir(self.input_folder):
            if filename.endswith('.pdf'):
                password = self.password_entry.get()
                input_path = os.path.join(self.input_folder, filename)
                output_path = os.path.join(self.output_folder, filename.replace('.pdf', '_unlocked.pdf'))
                unlockThread = threading.Thread(target=self.unlock_pdf, args=(filename, password, input_path, output_path))
                unlockThreads.append(unlockThread)
                unlockThread.start()
        for unlockThread in unlockThreads:
            unlockThread.join()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Unlocking time: {elapsed_time}")

    @staticmethod
    def unlock_pdf(filename, password, input_path, output_path):
        try:
            with open(input_path, 'rb') as lockedPDF:
                reader = pypdf.PdfReader(lockedPDF)
                if reader.is_encrypted:
                    try:
                        reader.decrypt(password)
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to decrypt {filename}. Error: {e}")
                with open(output_path, 'wb') as unlockedPDF:
                    writer = pypdf.PdfWriter()
                    for i in range(len(reader.pages)):
                        writer.add_page(reader.pages[i])
                    writer.write(unlockedPDF)
            print(f"{filename} unlocked successfully is now in {output_path}")
        except Exception as e:
            messagebox.showerror(f"Failed to decrypt {filename}", "")

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    PDFUnlocker().run()

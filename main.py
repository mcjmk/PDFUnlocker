#! python3
# PDFUnlocker - a simple script to remove passwords from your PDF files (assuming you know the password).
import PyPDF2
import os

# Enter password to your pdf files here
PASSWORD = ''

input_folder = 'in'
output_folder = 'out'

if __name__ == '__main__':
    print(os.getcwd())
    for filename in os.listdir(input_folder):
        if filename.endswith('.pdf'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace('.pdf', '_unlocked.pdf'))
            with open(input_path, 'rb') as lockedPDF:
                reader = PyPDF2.PdfReader(lockedPDF)
                reader.decrypt(PASSWORD)

                with open(output_path, 'wb') as unlockedPDF:
                    writer = PyPDF2.PdfWriter()
                    for i in range(len(reader.pages)):
                        writer.add_page(reader.pages[i])
                    writer.write(unlockedPDF)
            print(f"{filename} unlocked successfully is now in {output_path}")

import os
import sys
import fitz  # PyMuPDF
import datetime

# Get the path of the existing PDF and font in the bundled executable
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Function to modify the existing PDF and add input data
def create_pdf(name, id_number, input_pdf):
    # Load the existing PDF
    input_pdf = resource_path(input_pdf)  # Get the correct path for the bundled PDF
    doc = fitz.open(input_pdf)
    
    # Choose the first page to insert text (modify as needed for other pages)
    page = doc[0]
    
    # Define the position where you want to insert text
    name_position = (142, 407)
    id_position = (153, 423)
    date_position = (487, 92)
    
    # Insert system date
    current_date = datetime.datetime.now().strftime("%d/%m/%Y")
    
    # Load a font that supports Georgian characters
    font_path = resource_path("DejaVuSansCondensed.ttf")
    page.insert_font(fontname="DejaVu", fontfile=font_path, encoding="unicode")

    # Insert the text with the loaded font
    page.insert_text(name_position, f"{name}", fontsize=10, fontname="DejaVu")
    page.insert_text(id_position, f"{id_number}", fontsize=10, fontname="DejaVu")
    page.insert_text(date_position, f"{current_date}", fontsize=10, fontname="DejaVu")
    
    # Save the modified PDF to a new file
    output_pdf = "invoice.pdf"
    doc.save(output_pdf)
    doc.close()

    print("PDF modified successfully and saved as 'output_modified.pdf'!")

# Command-line input
name = input("Enter your Name: ")
id_number = input("Enter your ID Number: ")

# Specify the existing PDF to modify
input_pdf = "example.pdf"

# Modify the existing PDF with entered data
create_pdf(name, id_number, input_pdf)

# pyinstaller --onefile --add-data "example.pdf;." --add-data "DejaVuSansCondensed.ttf;." main.py
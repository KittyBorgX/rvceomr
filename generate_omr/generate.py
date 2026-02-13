import os
from io import BytesIO
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color
import copy

INPUT_FILE = "input.pdf"
OUTPUT_FILE = "output_serialized.pdf"
START = 1
END = 1500

TEXT_X = 455
TEXT_Y = 785
FONT_SIZE = 13


def create_overlay(page_width, page_height, text):
    """
    Create a PDF overlay with the serial number text.
    """
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))
    c.setFillColor(Color(238/255, 29/255, 35/255))
    # #ee1d23
    c.setFont("Times-Bold", FONT_SIZE)
    c.drawString(TEXT_X, TEXT_Y, text)
    c.save()
    packet.seek(0)
    return PdfReader(packet)


def convert_image_to_pdf(image_path):
    """
    Convert image to single-page PDF in memory.
    """
    image = Image.open(image_path)
    pdf_bytes = BytesIO()
    image.convert("RGB").save(pdf_bytes, format="PDF")
    pdf_bytes.seek(0)
    return PdfReader(pdf_bytes)


def main():
    # Determine if input is PDF or image
    if INPUT_FILE.lower().endswith(".pdf"):
        base_pdf = PdfReader(INPUT_FILE)
    else:
        base_pdf = convert_image_to_pdf(INPUT_FILE)

    base_page = base_pdf.pages[0]
    page_width = float(base_page.mediabox.width)
    page_height = float(base_page.mediabox.height)

    writer = PdfWriter()


    for i in range(START, END + 1):
        serial = f"1{i:04d}"

        page = copy.deepcopy(base_page)  # TRUE CLONE

        overlay_pdf = create_overlay(page_width, page_height, serial)
        overlay_page = overlay_pdf.pages[0]

        page.merge_page(overlay_page)
        writer.add_page(page)


    # Write final PDF
    with open(OUTPUT_FILE, "wb") as f:
        writer.write(f)

    print(f"Created {OUTPUT_FILE} with serial numbers from {START:04d} to {END:04d}")


if __name__ == "__main__":
    main()

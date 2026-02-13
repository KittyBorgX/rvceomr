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

    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))
    # color for the red text used in given template - #ee1d23
    c.setFillColor(Color(238/255, 29/255, 35/255))
    c.setFont("Times-Bold", FONT_SIZE)
    c.drawString(TEXT_X, TEXT_Y, text)
    c.save()
    packet.seek(0)
    return PdfReader(packet)

def main():
    # Determine if input is PDF or image
    base_pdf = PdfReader(INPUT_FILE)
    base_page = base_pdf.pages[0]
    page_width = float(base_page.mediabox.width)
    page_height = float(base_page.mediabox.height)

    writer = PdfWriter()

    for i in range(START, END + 1):
        serial = f"1{i:04d}"

        page = copy.deepcopy(base_page)

        overlay_pdf = create_overlay(page_width, page_height, serial)
        overlay_page = overlay_pdf.pages[0]

        page.merge_page(overlay_page)
        writer.add_page(page)

    with open(OUTPUT_FILE, "wb") as f:
        writer.write(f)

    print(f"Created {OUTPUT_FILE} with serial numbers from {START:04d} to {END:04d}")


if __name__ == "__main__":
    main()

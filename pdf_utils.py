from fpdf import FPDF
import textwrap

def safe_text(text):
    if not text:
        return ""
    replacements = {
        "–": "-",
        "—": "-",
        "•": "-",
        "’": "'",
        "“": '"',
        "”": '"',
        "…": "...",
        "\u00a0": " ",
        "\t": " ",
        "\r": " "
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    text = " ".join(text.split())
    return text.encode("latin-1", "ignore").decode("latin-1")

class PDFGenerator:
    def __init__(self, filename):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)
        self.filename = filename

    def add_heading(self, text):
        self.pdf.ln(2)
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.multi_cell(0, 10, safe_text(text))
        self.pdf.set_font("Arial", size=12)

    def add_line(self, text):
        text = safe_text(text)
        wrapped = textwrap.fill(text, width=90)
        self.pdf.set_x(10)
        self.pdf.multi_cell(0, 8, wrapped)

    def add_separator(self):
        self.pdf.ln(5)

    def save(self):
        self.pdf.output(self.filename)

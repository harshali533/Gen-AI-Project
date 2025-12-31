from fpdf import FPDF

class PDFGenerator:
    def __init__(self, filename):
        self.pdf = FPDF()
        self.pdf.set_margins(10, 10, 10)
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()
        self.pdf.set_font("Helvetica", size=11)
        self.filename = filename

    def add_heading(self, text):
        text = self._clean(text)
        if not text:
            return
        self._reset_x()
        self.pdf.set_font("Helvetica", "B", 14)
        self.pdf.multi_cell(self._width(), 8, text)
        self.pdf.ln(2)
        self.pdf.set_font("Helvetica", size=11)

    def add_line(self, text):
        text = self._clean(text)
        if not text:
            return
        self._reset_x()
        self.pdf.multi_cell(self._width(), 7, text)

    def add_separator(self):
        self._reset_x()
        self.pdf.ln(3)
        self.pdf.cell(self._width(), 0, "_" * 80)
        self.pdf.ln(5)

    def save(self):
        self.pdf.output(self.filename)

    # ---------- helpers ----------
    def _reset_x(self):
        self.pdf.set_x(self.pdf.l_margin)

    def _width(self):
        return self.pdf.w - self.pdf.l_margin - self.pdf.r_margin

    def _clean(self, text):
        if not text:
            return ""
        text = text.encode("latin-1", "ignore").decode("latin-1")
        words = []
        for w in text.split():
            if len(w) > 70:
                w = w[:70] + "..."
            words.append(w)
        return " ".join(words)

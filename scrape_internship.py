# sunbeam_scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pdf_generator import PDFGenerator

def scrape_internship(pdf_filename="Sunbeam_Internship_Data.pdf"):
    """
    Scrapes Sunbeam internship information and generates a PDF.
    
    Args:
        pdf_filename (str): The name of the PDF file to save.
    """
    # ---------------- PDF ----------------
    pdf = PDFGenerator(pdf_filename)

    # ---------------- Selenium ----------------
    driver = webdriver.Chrome()
    driver.get("https://www.sunbeaminfo.in/internship")
    wait = WebDriverWait(driver, 20)

    # Scroll to bottom (required)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait until table rows are loaded
    wait.until(EC.presence_of_element_located((By.XPATH, "//table//tr")))

    # ---------------- Internship Info ----------------
    pdf.add_heading("Sunbeam Internship Information")
    pdf.add_separator()

    info_sections = driver.find_elements(By.TAG_NAME, "p")
    for info in info_sections[:5]:
        if info.text.strip():
            pdf.add_line(info.text)

    # ---------------- Internship Batches ----------------
    pdf.add_heading("Internship Batches")
    pdf.add_separator()

    table = driver.find_element(By.XPATH, "(//table)[last()]")
    rows = table.find_elements(By.TAG_NAME, "tr")
    print("Rows found:", len(rows))  # Debug

    for row in rows[1:]:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 6:
            pdf.add_line(f"Batch Name : {cols[0].text}")
            pdf.add_line(f"Duration   : {cols[1].text}")
            pdf.add_line(f"Start Date : {cols[2].text}")
            pdf.add_line(f"End Date   : {cols[3].text}")
            pdf.add_line(f"Time       : {cols[4].text}")
            pdf.add_line(f"Fees       : {cols[5].text}")
            pdf.add_separator()

    # ---------------- Cleanup ----------------
    driver.quit()
    pdf.save()
    print(f"PDF generated: {pdf_filename}")

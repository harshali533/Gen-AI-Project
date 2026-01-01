from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from pdf_utils import PDFGenerator  # Updated import if you renamed pdf_generator.py

def scrape_about():
    print("\n=== Sunbeam About Us – PDF Generation ===\n")

    # ---------- PDF ----------
    # Use full raw path and add timestamp to avoid overwrite/permission issues
    import time
    timestamp = int(time.time())
    filename = f"Sunbeam_About_Us{timestamp}.pdf"
    pdf = PDFGenerator(filename)
    pdf.add_heading("About Sunbeam Infotech")
    pdf.add_separator()

    # ---------- Selenium ----------
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 20)
    driver.get("https://sunbeaminfo.in/about-us.php")

    # Wait for page render
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(3)

    # Force full scroll
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # ---------- Extract main content ----------
    content_blocks = driver.find_elements(By.XPATH, "//p | //li | //h2 | //h3")
    seen = set()
    for el in content_blocks:
        text = el.text.strip()
        if text and text not in seen:
            seen.add(text)
            pdf.add_line(text)

    # ---------- Cleanup ----------
    pdf.save()
    driver.quit()

    print(f"About Us PDF created successfully!\nFile saved as: {filename}")

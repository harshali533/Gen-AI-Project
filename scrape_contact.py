from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pdf_utils import PDFGenerator  # Updated import if you renamed pdf_generator.py

def scrape_contact():
    print("\n=== Sunbeam Contact Us – PDF Generation ===\n")

    # ---------- PDF ----------
    pdf = PDFGenerator("Sunbeam_Contact_Centres.pdf")
    pdf.add_heading("Sunbeam Contact Centres")
    pdf.add_separator()

    # ---------- Selenium ----------
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15)
    driver.get("https://sunbeaminfo.in/contact-us")
    time.sleep(3)

    # ---------- Locate centre blocks ----------
    centres = driver.find_elements(By.XPATH, "//div[contains(@class,'col')]")
    centre_count = 0

    for block in centres:
        text = block.text.strip()
        if "SunBeam" not in text:
            continue

        centre_count += 1
        pdf.add_heading(f"Centre {centre_count}")

        # Centre Name
        try:
            name = block.find_element(By.TAG_NAME, "h4").text.strip()
            pdf.add_line(f"Centre Name : {name}")
        except:
            pass

        # Address
        try:
            addr = block.find_element(By.XPATH, ".//p").text.strip()
            pdf.add_line(f"Address     : {addr}")
        except:
            pass

        # Phone
        try:
            phone_element = block.find_element(By.XPATH, ".//a[contains(@href,'tel')]")
            phone_text = phone_element.text.strip()
            pdf.add_line(f"Phone       : {phone_text}")
        except:
            pass

        # Email
        try:
            email_element = block.find_element(By.XPATH, ".//a[contains(@href,'mailto')]")
            email_text = email_element.text.strip()
            pdf.add_line(f"Email       : {email_text}")
        except:
            pass

        # Google Map
        try:
            iframe = block.find_element(By.XPATH, ".//iframe")
            map_url = iframe.get_attribute("src")
            pdf.add_line(f"Map URL     : {map_url}")
        except:
            pass

        pdf.add_separator()

    driver.quit()
    pdf.save()
    print(f"PDF created successfully with {centre_count} centres")
    print("File saved as: Sunbeam_Contact_Centres.pdf")

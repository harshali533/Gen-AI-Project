# main.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import time

# import all scraping modules
from aboutScraping import scrape_about
from coursesScraping import scrape_courses
from internshipScraping import scrape_internship
from contactScraping import scrape_contact


# ---------------------------
# Start Browser Session
# ---------------------------
def start_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")

    service = Service()  # uses installed chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    return driver


# ---------------------------
# Remove Header & Footer (Important)
# ---------------------------
def clean_layout(driver):
    driver.execute_script("""
        let header = document.querySelector('header');
        if(header) header.remove();
        let footer = document.querySelector('footer');
        if(footer) footer.remove();
    """)


# ---------------------------
# Save text into PDF
# ---------------------------
def save_to_pdf(text, filename="sunbeaminfo_scraped_data.pdf"):
    pdf = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    x_margin = 40
    y_margin = height - 40

    pdf.setFont("Helvetica", 10)
    y = y_margin

    for line in text.split("\n"):
        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y = y_margin

        pdf.drawString(x_margin, y, line[:120])
        y -= 14

    pdf.save()


# ---------------------------
# MAIN EXECUTION
# ---------------------------
def main():
    print("Scraping SunbeamInfo.in ...")

    driver = start_driver()
    final_text = ""

    try:
        # ABOUT
        clean_layout(driver)
        final_text += scrape_about(driver)
        time.sleep(2)

        # COURSES
        clean_layout(driver)
        final_text += scrape_courses(driver)
        time.sleep(2)

        # INTERNSHIP
        clean_layout(driver)
        final_text += scrape_internship(driver)
        time.sleep(2)

        # CONTACT
        clean_layout(driver)
        final_text += scrape_contact(driver)

    except Exception as e:
        print("Error occurred:", e)

    finally:
        driver.quit()

    save_to_pdf(final_text)
    print("PDF created successfully!")


# ---------------------------
# Run Program
# ---------------------------
if __name__ == "__main__":
    main()

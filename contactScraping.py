# contactScraping.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_contact(driver):
    driver.get("https://sunbeaminfo.in/contact")

    wait = WebDriverWait(driver, 15)

    centres = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//div[contains(text(),'SunBeam')]")
        )
    )

    content = "\n\n========== CONTACT ==========\n"

    for c in centres:
        content += c.text.strip() + "\n\n"

    return content

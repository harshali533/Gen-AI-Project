# internshipScraping.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_internship(driver):
    driver.get("https://sunbeaminfo.in/internship")

    wait = WebDriverWait(driver, 15)

    main_section = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//section | //div[contains(@class,'container')]")
        )
    )

    return "\n\n========== INTERNSHIP ==========\n" + main_section.text + "\n"

# aboutScraping.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_about(driver):
    driver.get("https://sunbeaminfo.in/about")

    wait = WebDriverWait(driver, 15)

    # MAIN CONTENT ONLY (not header/footer)
    about_section = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//section | //div[contains(@class,'container')]")
        )
    )

    text = about_section.text.strip()

    return "\n\n========== ABOUT US ==========\n" + text + "\n"

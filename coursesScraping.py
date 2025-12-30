# coursesScraping.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_courses(driver):
    driver.get("https://sunbeaminfo.in/courses")

    wait = WebDriverWait(driver, 15)

    course_blocks = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//div[contains(@class,'course') or //section]")
        )
    )

    content = "\n\n========== COURSES ==========\n"

    for block in course_blocks:
        txt = block.text.strip()
        if len(txt) > 50:        # filters menu & junk
            content += txt + "\n\n"

    return content

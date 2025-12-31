from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pdf_generator import PDFGenerator


def scrape_modular_courses():
    print("\n=== Sunbeam Modular Courses – PDF Generation ===\n")

    # ---------------- PDF ----------------
    pdf = PDFGenerator("Sunbeam_Modular_Courses.pdf")
    pdf.add_heading("Sunbeam Modular Courses Detailed Information")
    pdf.add_separator()

    # ---------------- Selenium ----------------
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15)

    try:
        driver.get("https://sunbeaminfo.in/modular-courses-home")
        time.sleep(2)

        # ---------- Collect all modular course links ----------
        links = set()
        anchors = driver.find_elements(
            By.XPATH,
            "//a[contains(@href,'modular-courses') and not(contains(@href,'home'))]"
        )

        for a in anchors:
            href = a.get_attribute("href")
            if href:
                links.add(href)

        links = sorted(list(links))

        # ---------- Helper functions ----------
        def safe_text(text):
            replacements = {
                "—": "-",
                "•": "-",
                "…": "...",
                "’": "'",
                "“": '"',
                "”": '"'
            }
            for k, v in replacements.items():
                text = text.replace(k, v)
            return text

        def collect_following_until_heading(base_el):
            texts = []
            siblings = base_el.find_elements(By.XPATH, "following-sibling::*")
            for s in siblings:
                if s.tag_name.lower() in ("h1", "h2", "h3", "h4"):
                    break
                t = s.text.strip()
                if t:
                    texts.append(t)
            return texts

        # ---------- Scrape each course ----------
        for link in links:
            driver.get(link)
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Course Name
            course_name = ""
            for tag in ("//h1", "//h2", "//h3"):
                try:
                    t = driver.find_element(By.XPATH, tag).text.strip()
                    if t:
                        course_name = t
                        break
                except:
                    continue

            pdf.add_heading(f"Course Name: {safe_text(course_name)}")

            # General info
            keys = [
                "Batch Schedule",
                "Schedule",
                "Duration",
                "Timings",
                "Fees",
                "Target Audience"
            ]

            for k in keys:
                try:
                    el = driver.find_element(
                        By.XPATH,
                        f"//*[contains(normalize-space(.),'{k}')]"
                    )
                    text = el.text.strip()
                    if text:
                        pdf.add_line(safe_text(text))
                except:
                    continue

            pdf.add_separator()

            # Sections
            section_headings = [
                "Syllabus",
                "Pre-requisites",
                "Software Setup",
                "Student Feedback",
                "Recorded Videos",
                "Batch schedule"
            ]

            for heading in section_headings:
                try:
                    els = driver.find_elements(
                        By.XPATH,
                        f"//h2[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{heading.lower()}')] | "
                        f"//h3[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{heading.lower()}')] | "
                        f"//h4[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{heading.lower()}')]"
                    )

                    for el in els:
                        pdf.add_heading(safe_text(el.text.strip()))
                        blocks = collect_following_until_heading(el)
                        for b in blocks:
                            pdf.add_line(safe_text(b))
                except:
                    continue

            pdf.add_separator()

        pdf.save()
        print("✅ Courses PDF created: Sunbeam_Modular_Courses.pdf")

    except Exception as e:
        print("❌ Courses scraping failed:", e)

    finally:
        driver.quit()

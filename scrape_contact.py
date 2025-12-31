def scrape_contact():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import time
    from pdf_utils import PDFGenerator

    print("\n=== Sunbeam Contact – PDF Generation ===\n")

    pdf = PDFGenerator("Sunbeam_Contact_Centres.pdf")
    driver = webdriver.Chrome()

    try:
        driver.get("https://www.sunbeaminfo.in/contact-us")
        time.sleep(3)

        centres = driver.find_elements(By.XPATH, "//div[contains(@class,'col')]")

        count = 0
        for block in centres:
            text = block.text.strip()
            if "SunBeam" not in text:
                continue

            count += 1
            pdf.add_heading(f"Centre {count}")
            pdf.add_separator()

            for line in text.split("\n"):
                pdf.add_line(line)

            pdf.add_separator()

    except Exception as e:
        print("❌ Contact scraping failed:", e)

    finally:
        driver.quit()
        pdf.save()

    print(f"✅ Contact PDF created with {count} centres")

from scrape_internship import scrape_internship
from scrape_contact import scrape_contact
from scrape_about import scrape_about
from scrape_courses import scrape_modular_courses   # ✅ correct import

if __name__ == "__main__":
    print("=== Sunbeam Scraping Tasks ===\n")

    scrape_about()
    scrape_modular_courses()
    scrape_internship()
    scrape_contact()
    
       # ✅ correct function call

    print("\n✅ All PDFs generated successfully!")

from scrape_internship import scrape_internship
from scrape_contact import scrape_contact
from scrape_about import scrape_about
from scrape_courses import scrape_courses

if __name__ == "__main__":
    print("=== Sunbeam Scraping Tasks ===\n")
    scrape_internship()
    scrape_contact()
    scrape_about()
    scrape_courses()
    print("\n✅ All PDFs generated successfully!")

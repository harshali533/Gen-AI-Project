import subprocess
import sys
import os
from scrape_internship import scrape_internship
from scrape_contact import scrape_contact
from scrape_about import scrape_about
from scrape_courses import scrape_modular_courses

def launch_chatbot():
    print("\n🚀 Launching Sunbeam Chatbot...")
    # This command is equivalent to running 'streamlit run chatbot_app.py' in your terminal
    subprocess.run([sys.executable, "-m", "streamlit", "run", "chatbot_s.py"])

if __name__ == "__main__":
    print("=== Sunbeam Scraping Tasks ===\n")

    # 1. Scrape data and generate PDFs
    scrape_about()
    scrape_modular_courses()
    scrape_internship()
    scrape_contact()

    print("\n✅ All PDFs generated successfully!")

    # 2. Launch the RAG Chatbot
    launch_chatbot()
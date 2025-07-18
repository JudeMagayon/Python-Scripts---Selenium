import os
import time
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Step 1: Launch Chrome and navigate to HRMIS login page ---
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Optional: Use your default Chrome profile to stay logged in
# chrome_options.add_argument("--user-data-dir=C:/Users/<YourUsername>/AppData/Local/Google/Chrome/User Data")
# chrome_options.add_argument("--profile-directory=Default")

driver = webdriver.Chrome(options=chrome_options)

print("🌐 Opening HRMIS login page...")
driver.get("https://hrmis.airforce.mil.ph/login")

# --- Step 2: Wait for manual login ---
input("✅ Please log in to HRMIS manually in the browser.\nAfter you're logged in, press Enter here to continue...")

# --- Step 3: Prompt to select Excel file ---
def choose_excel_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Select Excel file",
        filetypes=[("Excel Files", "*.xlsx *.xls")]
    )

excel_file = choose_excel_file()
if not excel_file:
    print("❌ No Excel file selected. Exiting.")
    driver.quit()
    exit()

# --- Step 4: Read URLs from Excel Column C ---
df = pd.read_excel(excel_file, usecols="C")
urls = df.iloc[:, 0].dropna().unique()
print(f"✅ Loaded {len(urls)} unique links from Column C")

# --- Step 5: Optional folder for PDFs ---
os.makedirs("pdfs", exist_ok=True)
pdf_count = 0

# --- Step 6: Process each URL ---
for idx, url in enumerate(urls):
    try:
        print(f"\n[{idx+1}/{len(urls)}] Opening: {url}")
        driver.get(url)

        # Wait and click Save button
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Save') or contains(@title, 'Save')]"))
        )
        ActionChains(driver).move_to_element(save_button).click().perform()
        print(f"✅ Clicked 'Save' icon for {url}")
        pdf_count += 1

        time.sleep(3)

    except Exception as e:
        print(f"❌ Could not click Save on {url}: {e}")

# --- Step 7: Done ---
driver.quit()
print(f"\n🏁 Done! PDFs clicked: {pdf_count}")

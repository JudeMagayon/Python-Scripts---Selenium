import os
import time
import shutil
import requests
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# === Prepare download directory ===
download_dir = os.path.abspath("downloads")
os.makedirs(download_dir, exist_ok=True)

# === Setup Chrome options ===
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)

# === Excel selection dialog ===
def select_excel():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])

# === Load Excel ===
excel_path = select_excel()
df = pd.read_excel(excel_path, header=None, usecols=[1, 2])
df.columns = ["filename", "url"]
df = df.dropna()

print(f"📄 Loaded {len(df)} entries.")

# === Login manually ===
driver.get("https://yourwebsitewithlogin.com")
input(" Please log in manually, then press Enter to continue...")

# === Download PDFs ===
for idx, row in df.iterrows():
    name = str(row["filename"]).strip().replace(" ", "_") + ".pdf"
    url = str(row["url"]).strip()
    print(f"\n[{idx+1}] Opening: {url}")

    try:
        driver.get(url)
        time.sleep(3)

        # Try to locate embedded PDF inside <iframe> or <embed>
        try:
            pdf_element = driver.find_element(By.TAG_NAME, "iframe")
            pdf_url = pdf_element.get_attribute("src")
        except:
            try:
                pdf_element = driver.find_element(By.TAG_NAME, "embed")
                pdf_url = pdf_element.get_attribute("src")
            except:
                print("❌ Could not find embedded PDF viewer.")
                continue

        if not pdf_url.startswith("http"):
            base = "/".join(url.split("/")[:3])
            pdf_url = base + pdf_url

        print(f"📎 Downloading PDF from: {pdf_url}")

        # Copy session cookies to requests
        cookies = driver.get_cookies()
        session = requests.Session()
        session.verify = False
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        response = session.get(pdf_url)
        if response.status_code == 200:
            file_path = os.path.join(download_dir, name)
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"✅ Saved: {name}")
        else:
            print(f"❌ Failed to download PDF (HTTP {response.status_code})")

    except Exception as e:
        print(f"⚠️ Error: {e}")

driver.quit()
print("\n🎉 Done downloading all PDFs.")

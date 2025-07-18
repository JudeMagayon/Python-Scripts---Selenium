# Auto-Download Script

This Python script automates the process of:
1. Opening the [website - edit the website part on the script]
2. Letting the user log in manually,
3. Reading a list of HRMIS page links from an Excel file,
4. Visiting each link and clicking the **Download icon** (downward arrow) to trigger downloads or save actions.

---

## Features

- ✅ Manual login support (secure for MFA)
- ✅ Excel input (URLs in Column C)
- ✅ Selenium-controlled Chrome browser
- ✅ Clicks download icons on each page
- 🗂️ Future support for auto-saving PDFs

---

## ⚙️ Setup Instructions

### 1. Install Python

- **Windows**: https://www.python.org/downloads/windows/
- **macOS**: https://www.python.org/downloads/mac-osx/

Make sure `python` or `python3` is in your system PATH.

### 2. Install Required Python Packages

Open a terminal (macOS) or command prompt (Windows), then run:

```
pip install selenium pandas openpyxl
```

### 3. Install Google Chrome

- https://www.google.com/chrome/

Make sure it’s the default or accessible via Selenium.

---

## Excel File Format

- The script expects an `.xlsx` or `.xls` file.
- All **HRMIS links must be in Column C** (starting at any row).
- Example:

| A        | B       | C                                                  |
|----------|---------|----------------------------------------------------|
| (empty)  | (empty) | https://hrmis.airforce.mil.ph/confirm_dash_a1/994 |
| ...      | ...     | https://hrmis.airforce.mil.ph/confirm_dash_a1/995 |

---

## How to Run the Script

### Windows

```
cd path\to\script
python hrmis_download_script.py
```

### macOS

```
cd /path/to/script
python3 hrmis_download_script.py
```

---

## How It Works

1. Launches Chrome and opens the HRMIS login page.
2. You log in manually using your credentials.
3. You press **Enter** in the terminal after login.
4. A file dialog prompts you to choose your Excel file.
5. The script reads the URLs from Column C.
6. Each URL is opened in the browser.
7. The script clicks the **Download icon** (down arrow) on each page.

---

## Output

- Optionally creates a `pdfs/` folder (for future file saving).
- Logs progress and errors in the terminal.

---

## Troubleshooting

- **Nothing happens after URL opens**: The download icon may be missing or has a different structure.
- **Element not clickable error**: The icon may load late or need scrolling. Try increasing wait time.
- **Selenium version issue**: Make sure `selenium` is v4.6+ (uses built-in ChromeDriver).

---

## Notes

- The script is designed for **manual login**, useful when MFA or Captchas are used.
- If you want persistent login (no login every run), ask how to enable Chrome profile reuse.
- Only clicks visible **download icon buttons** — won’t auto-save PDFs unless configured.

---

##  To-Do (Optional Enhancements)

- [ ] Auto-download PDF using DevTools Protocol
- [ ] Use Chrome user profile for persistent sessions
- [ ] Add progress bar or GUI
- [ ] Export logs to file

---

## Author

Created by Jude Magayon


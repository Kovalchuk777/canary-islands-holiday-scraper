from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import undetected_chromedriver as uc
import random
import csv
import pandas as pd
from openpyxl.styles import Border, Side

MAX_PRICE = 700
URL = "https://www.loveholidays.com/holidays/?destinationIds=474&departureAirports=BHX&nights=7&rooms=2&flexibility=0&sort=POPULAR&f.boardBasis=AI"

def extract_price(text):
    match = re.search(r'£(\d+[,.]?\d*)', text)
    if match:
        return float(match.group(1).replace(',', ''))
    return None

def parse_loveholidays():
    print("[*] Launching browser and loading page")
    options = uc.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    driver = uc.Chrome(options=options)
    driver.get(URL)

    try:
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "section[data-id='search-result-card']"))
        )
    except Exception:
        print("[-] Cards did not appear within 40 seconds.")
        driver.quit()
        return []

    SCROLL_PAUSE = 1.5
    MAX_SCROLLS = 100
    EMPTY_SCROLLS_LIMIT = 8

    last_count = 0
    empty_scrolls = 0
    for _ in range(MAX_SCROLLS):
        driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(SCROLL_PAUSE + random.uniform(0, 1.2))
        cards = driver.find_elements(By.CSS_SELECTOR, "section[data-id='search-result-card']")
        if len(cards) == last_count:
            empty_scrolls += 1
            if empty_scrolls >= EMPTY_SCROLLS_LIMIT:
                break
        else:
            empty_scrolls = 0
        last_count = len(cards)

    offers = []
    print(f"Cards found: {len(cards)}")
    for i, card in enumerate(cards):
        try:
            name = card.find_element(By.CSS_SELECTOR, "h2[data-id='hotel-name'] span").text.strip()
            price = card.find_element(By.CSS_SELECTOR, "span.css-z4soc5").text.strip()
            price_value = extract_price(price)
            if price_value and price_value <= MAX_PRICE:
                offers.append({"Hotel": name, "Price": price_value})
        except Exception as e:
            print(f"Error: {e}")
            continue

    driver.quit()
    return offers

if __name__ == "__main__":
    print("[*] Parsing offers on loveholidays...")
    data = parse_loveholidays()
    if data:
        print(f"[+] Found suitable tours: {len(data)}\n")
        for d in data:
            print(f"{d['Hotel']}: £{d['Price']}")

        df = pd.DataFrame(data)
        excel_path = r"E:\VS\loveholidays_offers.xlsx"
        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Offers")
            ws = writer.sheets["Offers"]
            for column_cells in ws.columns:
                length = max(len(str(cell.value)) for cell in column_cells)
                ws.column_dimensions[column_cells[0].column_letter].width = length + 2

            thin = Side(border_style="thin", color="000000")
            border = Border(left=thin, right=thin, top=thin, bottom=thin)
            for row in ws.iter_rows():
                for cell in row:
                    cell.border = border

        print(f"\n[+] Data saved to Excel: {excel_path}")
    else:
        print("[-] No offers found for the specified price.")
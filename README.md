# Canary Islands Holiday Scraper
Python automation script that scrapes LoveHolidays for 7-day holiday deals to the Canary Islands, filters them by price, and exports the results into a neatly formatted Excel file.

## ✨ Features
Scrapes dynamically loaded holiday listings from LoveHolidays

Automatically scrolls through the page to load all results

Filters offers by:

- Price (default: ≤ £700 per person)
- Board basis (e.g., All Inclusive)
- Departure airport (e.g., BHX)
- Exports the results into a clean, formatted Excel file

## 🖥️ Example Output
- SBH Fuerteventura Playa	409
- SBH Club Paraiso Playa - All Incl.	429
- Blue Sea Costa Jardin and Spa	399

## 📦 Installation

`git clone https://github.com/your-username/canary-islands-holiday-scraper.git`
`cd canary-islands-holiday-scraper`
`pip install -r requirements.txt `

## 🚀 Usage

`python loveholidays_scraper.py
The results will be saved in loveholidays_offers.xlsx in the project directory.`

## ⚙️ Requirements
- Python 3.8+
- Google Chrome
- undetected-chromedriver
- pandas, openpyxl
## Install dependencies:


`pip install pandas openpyxl undetected-chromedriver selenium`
## 📜 License
This project is licensed under the MIT License.

# Web Data Scrapers (Playwright + BeautifulSoup)

A collection of focused scrapers:

- Google Maps → distance & duration
- Amazon Laptops → multi-page product scraper (~400+ records)
- Ganpat University → semester result fetcher using enrollment ranges
- Google Sheet (View-Only / No-Copy Mode) → mid-sem marks via pure beautifulSoup

Each project is independent, minimal, and easy to extend.

---

## 1. Google Maps — Distance & Time Scraper

Fetches travel **distance** and **duration** for origin–destination pairs using Playwright.

**Features**
- Accepts list of routes Excel.
- Automates Google Maps search.
- Extracts clean values like `12.3 km`, `32 mins`.
- Outputs structured CSV.

---

## 2. Amazon Laptop Scraper (Multi-Page, Generic)

Scrapes laptop listings across **multiple pages** on Amazon (≈ **400+ products** in one run).

**Highlights**
- Playwright handles navigation + pagination.
- BeautifulSoup parses stored page HTML for speed.
- Extracts:
  - Product title  
  - Parsed configuration (RAM, storage, CPU)
  - Price  
  - Ratings  

**Generic Design**
- Only the **search query** and **a couple selectors** need to change to scrape:
  - TVs  
  - Mobile phones  
  - Any Amazon category with similar card structure  
- Only breaks if Amazon completely redesigns the product card layout.

---

## 3. Ganpat University — Result Scraper

Fetches final exam/semester results for **given enrollment number ranges**.

**Performance**
- Scrapes results for **100+ students within ~1 minute**.
- Useful for collecting full batch marks and comparing performance across students.

**Features**
- Reads enrollment number ranges from `.txt` files.
- Extracts:
  - **Name**
  - **Branch**
  - **SGPA**
  - **CGPA**
- Exports all results to **CSV** for analysis & comparision.
---

## 4. Google Sheet (No-Copy Mode) — Mid-Sem Result Scraper

Scrapes data from **view-only Google Sheets** using **Requests + BeautifulSoup**.

**Key Points**
- No Playwright required — direct HTTP fetch + DOM parsing.
- Captures full sheet data for:
  - Averages  
  - Statistics  
  - Quick offline analysis  
- Useful when copy/export is disabled.

---

## Setup & Installation

```bash
# Core scraping deps
pip install requests bs4

# For Playwright-based Scrapers (Google Maps, Amazon, Ganpat)
pip install playwright
python -m playwright install
```

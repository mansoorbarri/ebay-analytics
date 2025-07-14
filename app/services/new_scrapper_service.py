# app/services/scraper_service.py
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import concurrent.futures # For parallel processing

def init_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36") # Add a user agent to mimic a real browser

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def get_sold_count(item_url: str) -> dict:
    driver = init_driver()
    try:
        driver.get(item_url)
        try: 
            sold_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'ux-textspans--BOLD') and contains(@class, 'ux-textspans--EMPHASIS') and contains(text(), 'sold')]"))
            )
            sold_text = sold_element.text
            return sold_text
            print(f"Found sold text (Attempt 1): {sold_text}")
        except: 
            sold_text = ""
            print("Sold element not found with Attempt 1 XPath. Trying other methods...")
        if not sold_text:
            try:
                # This XPath looks for a link that contains "sold" in its href AND has "sold" in its text.
                # This is more precise than just any 'sold' text on the page.
                sold_link_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'sold') and contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sold')]"))
                )
                sold_text = sold_link_element.text
                print(f"Found sold text (Attempt 2 - from link): {sold_text}")
            except:
                sold_text = ""
                print("Sold link element not found with Attempt 2 XPath. Trying another method for direct quantity...")
        if not sold_text:
            try:
                quantity_sold_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'qty-tag') or contains(@class, 'vi-qty-purchases')]/span[@class='qty']"))
                )
                sold_text = quantity_sold_element.text + " sold" # Add " sold" for regex consistency
                print(f"Found sold text (Attempt 3 - direct quantity): {sold_text}")
            except:
                sold_text = ""
                print("Direct quantity element not found with Attempt 3 XPath.")

        # sold_text = ""
        # elements = driver.find_elements(By.XPATH, "//a[contains(@href, 'sold')]")
        # for el in elements:
        #     if "sold" in el.text.lower():
        #         sold_text = el.text
        #         break

        # total_sold = int(re.search(r'(\d+)', sold_text).group()) if sold_text else 0

        # return {
        #     "url": item_url,
        #     "total_sold": total_sold,
        #     "sold_last_30_days": round(total_sold * 0.7),
        #     "sold_last_7_days": round(total_sold * 0.25)
        # }
    except Exception as e:
        print(f"Error processing {item_url}: {e}")

def get_top_items_sold_by_keyword(keyword: str, max_items: int = 5):
    driver = init_driver()
    try:
        ebay_search_url = f"https://www.ebay.com/sch/i.html?_nkw={keyword.replace(' ', '+')}&_sop=12"
        driver.get(ebay_search_url)
        time.sleep(3)  # wait for search results

        item_links = []
        items = driver.find_elements(By.XPATH, "//li[contains(@class, 's-item')]//a[@class='s-item__link']")
        for item in items[:max_items]:
            link = item.get_attribute("href")
            if link:
                item_links.append(link)

        results = []
        for url in item_links:
            try:
                data = get_sold_count(url)
                results.append(data)
            except Exception as e:
                results.append({"item_url": url, "error": str(e)})

        return {
            "keyword": keyword,
            "results": results
        }
    finally:
        driver.quit()

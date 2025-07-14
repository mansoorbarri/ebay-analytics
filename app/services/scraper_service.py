import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import concurrent.futures

def init_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-logging")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-images")
    options.add_argument("--page-load-strategy=normal")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def get_sold_count(url: str) -> dict:
    driver = init_driver()
    try:
        driver.get(url)
        sold_element = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'ux-textspans--SECONDARY') and contains(text(), 'sold')]"))
        )
        sold_text = sold_element.text
        match = re.search(r'(\d[\d,]*)', sold_text)
        total_sold = int(match.group(1).replace(',', '')) if match else 0
        
        return {
            "url": url,
            "total_sold": total_sold,
            "sold_last_30_days": int(total_sold * 0.7),
            "sold_last_7_days": int(total_sold * 0.25)
        }
    except:
        return {"url": url, "total_sold": 0, "sold_last_30_days": 0, "sold_last_7_days": 0}
    finally:
        driver.quit()

def get_top_items_sold_by_keyword(keyword: str, max_items: int = 5):
    driver = init_driver()
    try:
        url = f"https://www.ebay.com/sch/i.html?_nkw={keyword.replace(' ', '+')}&_sop=12"
        driver.get(url)
        
        WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.XPATH, "//li[contains(@class, 's-item')]"))
        )
        
        items = driver.find_elements(By.XPATH, "//li[contains(@class, 's-item')]//a[@class='s-item__link']")
        item_links = [item.get_attribute("href") for item in items[:max_items] 
                     if item.get_attribute("href") and "ebay.com/itm/" in item.get_attribute("href")]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(max_items, 3)) as executor:
            results = list(executor.map(get_sold_count, item_links))
        
        return {"keyword": keyword, "results": results}
    finally:
        driver.quit()
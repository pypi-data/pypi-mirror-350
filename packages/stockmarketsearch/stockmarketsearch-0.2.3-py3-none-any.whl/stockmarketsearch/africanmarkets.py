from .webdriver import start_webdriver
from bs4 import BeautifulSoup
from dataclasses import dataclass
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import re
import json
from datetime import datetime

DOMAIN = "https://www.african-markets.com"

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

class AfricanMarketsScraper():
    def __init__(self):
        self.driver = None
    
    def __del__(self):
        if self.driver:
            self.driver.quit()
            
    def search(self, query: str):
        self.driver = start_webdriver()
        try:
            self.driver.get(f"{DOMAIN}/en/")
            WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, Selectors.search_input))).send_keys(query)
            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, Selectors.search_result)))
            html = self.driver.page_source
        except TimeoutException:
            self.driver.quit()
            return []
        except Exception as e:
            logging.error(f"An error occurred in search: {e}", exc_info=True)
            self.driver.quit()
            return []
        return self._extract_search_results(html)
    
    def _extract_search_results(self, html: str):
        soup = BeautifulSoup(html, "html.parser")
        try:
            results = [
                {
                    "result_from": DOMAIN,
                    "company_name": item.text.strip(),
                    "url": f"{DOMAIN}{item.get('href')}",
                }
                for item in soup.select(Selectors.search_result)
            ]
        except Exception as e:
            logging.error(f"An error occurred while extracting search results: {e}", exc_info=True)
            return []
        return results
    
    def get_stock_data(self, url: str, start_date: str, end_date: str) -> dict:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            html = response.text
            data = self._extract_stock_data(html)
            
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            
            if data.get("historical_data"):
                data["historical_data"] = [
                    item for item in data["historical_data"]
                    if start_dt <= datetime.strptime(item['date'], "%Y-%m-%d") <= end_dt
                ]
            
        except Exception as e:
            logging.error(f"An error occurred while fetching stock data: {e}", exc_info=True)
            return {}
        return data
    
    def _extract_stock_data(self, html: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")
        try:
            data = {
                "data_from": DOMAIN,
                "company_name": soup.select_one(Selectors.company_name).text.strip() if soup.select_one(Selectors.company_name) else None,
                "symbol": soup.select_one(Selectors.symbol).text.strip() if soup.select_one(Selectors.symbol) else None,
            }
            for block in soup.select(Selectors.stat_block):
                stat_name = block.select_one(Selectors.stat_name).text.strip()
                stat_value = block.select_one(Selectors.stat_value).text.strip()
                if stat_name and stat_value:
                    data[stat_name.replace(".","").replace(" ","_")] = stat_value
            data["historical_data"] = self._extract_chart_data(html)
            
        except Exception as e:
            logging.error(f"An error occurred while extracting stock data: {e}", exc_info=True)
            return {}
        return data
    
    def _extract_chart_data(self, html: str) -> dict:
        """
        Extracts the chart data JavaScript array from the HTML.
        Returns the string between 'var chartData=' and the next ';'
        """
        match = re.search(r"var\s+chartData\s*=\s*(\[.*?\]);", html, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        return None
        

@dataclass(frozen=True)
class Selectors:
    search_input: str = "#search-input"
    search_result: str = "#search-results li a"
    
    company_name: str = "h2"
    stat_block: str = ".bloc"
    stat_name: str = "p:nth-of-type(1)"
    stat_value: str = "p:nth-of-type(2)"
    symbol: str = "#mod1541_djtabpanel1 > div > div > div:nth-child(4) > table > tbody > tr:nth-child(1) > td:nth-child(1) > span:nth-child(3)"

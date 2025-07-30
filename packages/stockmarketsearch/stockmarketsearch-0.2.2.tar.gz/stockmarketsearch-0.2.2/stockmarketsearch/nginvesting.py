from .webdriver import start_webdriver, get_cloudscraper
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dataclasses import dataclass
import subprocess
import json
from urllib.parse import urlencode
import logging
import json

DOMAIN = "https://ng.investing.com"

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

class NGInvestingScraper:
    def __init__(self):
        self.driver = None
        self.cloudscraper = get_cloudscraper()

    def __del__(self):
        if self.driver:
            self.driver.quit()

    def search(self, query: str):
        try:
            self.driver = start_webdriver()
            self.driver.get(f"{DOMAIN}/search/?q={query}&tab=quotes")
            filter_button = self.driver.find_element(By.CSS_SELECTOR, Selectors.equities_filter)
            self.driver.execute_script("arguments[0].click();", filter_button)
            html = self.driver.page_source
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
                    "flag": item.select_one(Selectors.flag).get("class")[0] if item.select_one(Selectors.flag) else None,
                    "symbol": item.select_one(Selectors.symbol).text.strip(),
                    "company_name": item.select_one(Selectors.name1).text.strip(),
                    "exchange_name": item.select_one(Selectors.type).text.strip().replace("Share - ", ""),
                    "url": f"{DOMAIN}{item.get('href')}",
                }
                for item in soup.select(Selectors.result_row)
            ]
        except Exception as e:
            logging.error(f"An error occurred while extracting search results: {e}", exc_info=True)
            return []
        return results
    
    def get_stock_data(self, url: str, start_date: str, end_date: str):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            }
            response = self.cloudscraper.get(url, headers=headers)
            data = self._extract_stock_data(response.text)
            historical_data = self._get_historical_data(url, start_date, end_date)
            data["historical_data"] = historical_data
        except Exception as e:
            logging.error(f"An error occurred while fetching stock data: {e}", exc_info=True)
            return {}
        return data
    
    def _extract_stock_data(self, html: str):
        soup = BeautifulSoup(html, "html.parser")
        try:
            data = {
                "data_from": DOMAIN,
                "logo": soup.select_one(Selectors.logo).get("src") if soup.select_one(Selectors.logo) else None,
                "company_name": soup.select_one(Selectors.name).text.strip() if soup.select_one(Selectors.name) else None,
                "currency": soup.select_one(Selectors.currency).text.strip() if soup.select_one(Selectors.currency) else None,
            }
            
            for stat in soup.select(Selectors.stat_block):
                stat_name = stat.select_one(Selectors.stat_name).text.strip() if stat.select_one(Selectors.stat_name) else None
                stat_value = stat.select_one(Selectors.stat_value).text.strip() if stat.select_one(Selectors.stat_value) else None
                if stat_name and stat_value:
                    data[stat_name] = stat_value
        except Exception as e:
            logging.error(f"An error occurred while extracting stock data: {e}", exc_info=True)
            return {}
        return data
    
    def _get_historical_data(self, url: str, start_date: str, end_date: str) -> list[dict]:
        try:
            stock_id = self._get_stock_id(url)
            historical_data = self._get_data(stock_id, start_date, end_date)
        except Exception as e:
            logging.error(f"An error occurred while fetching historical data: {e}", exc_info=True)
            return []
        return historical_data
        
    def _get_stock_id(self, url: str) -> str:
        """
        Extracts the stock ID from the given url.
        """
        try:
            response = self.cloudscraper.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            script_data = soup.select_one(Selectors.data_script).get_text()
            data = json.loads(script_data)
            stock_id = data["props"]["pageProps"]["state"]["pageInfoStore"]["identifiers"]["instrument_id"]
        except Exception as e:
            logging.error(f"An error occurred while extracting stock ID: {e}", exc_info=True)
            return ""
        return stock_id
    
    def _get_data(self, stock_id: str, start_date: str, end_date: str) -> list[dict]:
        """
        Fetches historical data for the given stock ID.
        """
        try:
            url = f'https://api.investing.com/api/financialdata/historical/{stock_id}' 
            params = {
                'start-date': start_date,
                'end-date': end_date,
                'time-frame': 'Daily',
                'add-missing-rows': 'false'
            }

            cnfg = ['curl', '-A', 'Chrome/128.0.0.0', '-H', 'domain-id: www', '-G', url, '-d', urlencode(params)]

            output = subprocess.run(cnfg, capture_output=True).stdout.decode()
            data = json.loads(output)
            print(data)
        except Exception as e:
            logging.error(f"An error occurred while fetching historical data: {e}", exc_info=True)
            return []
        return self._clean_historical_data(data['data'])

    def _clean_historical_data(self, datas: list) -> list[dict]:
        """
        Cleans and formats the historical data.
        """
        cleaned_data = []
        try:
            for item in datas:
                cleaned_data.append({
                    "date": item.get("rowDate"),
                    "open": item.get("last_openRaw"),
                    "high": item.get("last_maxRaw"),
                    "low": item.get("last_minRaw"),
                    "close": item.get("last_closeRaw"),
                    "volume": item.get("volumeRaw"),
                    "change_percent": item.get("change_precentRaw"),
                })
        except Exception as e:
            logging.error(f"An error occurred while cleaning historical data: {e}", exc_info=True)
            return []
        return cleaned_data

@dataclass(frozen=True)
class Selectors:
    #Search selectors
    result_row: str = "#fullColumn > div > div:nth-child(5) > div.searchSectionMain > div .row"
    flag: str = ".first i"
    symbol: str = ".second"
    name1: str = ".third"
    type: str = ".fourth"
    
    equities_filter: str = "input[data-value='equities']"
    
    # Stock Data selectors
    logo: str = "#__next > div.md\:relative.md\:bg-white > div.relative.flex > div.md\:grid-cols-\[1fr_72px\].md2\:grid-cols-\[1fr_420px\].grid.flex-1.grid-cols-1.px-4.pt-5.font-sans-v2.text-\[\#232526\].antialiased.transition-all.xl\:container.sm\:px-6.md\:gap-6.md\:px-7.md\:pt-10.md2\:gap-8.md2\:px-8.xl\:mx-auto.xl\:gap-10.xl\:px-10 > div.min-w-0 > div.flex.flex-col.gap-6.md\:gap-0 > div.font-sans-v2.md\:flex > div.relative.mb-3\.5.md\:flex-1 > img"
    name: str = "#__next > div.md\:relative.md\:bg-white > div.relative.flex > div.md\:grid-cols-\[1fr_72px\].md2\:grid-cols-\[1fr_420px\].grid.flex-1.grid-cols-1.px-4.pt-5.font-sans-v2.text-\[\#232526\].antialiased.transition-all.xl\:container.sm\:px-6.md\:gap-6.md\:px-7.md\:pt-10.md2\:gap-8.md2\:px-8.xl\:mx-auto.xl\:gap-10.xl\:px-10 > div.min-w-0 > div.flex.flex-col.gap-6.md\:gap-0 > div.font-sans-v2.md\:flex > div.relative.mb-3\.5.md\:flex-1 > div.mb-1 > h1"
    currency: str = "#__next > div.md\:relative.md\:bg-white > div.relative.flex > div.md\:grid-cols-\[1fr_72px\].md2\:grid-cols-\[1fr_420px\].grid.flex-1.grid-cols-1.px-4.pt-5.font-sans-v2.text-\[\#232526\].antialiased.transition-all.xl\:container.sm\:px-6.md\:gap-6.md\:px-7.md\:pt-10.md2\:gap-8.md2\:px-8.xl\:mx-auto.xl\:gap-10.xl\:px-10 > div.min-w-0 > div.flex.flex-col.gap-6.md\:gap-0 > div.font-sans-v2.md\:flex > div.relative.mb-3\.5.md\:flex-1 > div.flex.justify-items-start.gap-3.whitespace-nowrap.text-\[\#5B616E\] > div.flex.items-center.gap-1 > div > span"
    stat_block: str = "#__next > div.md\:relative.md\:bg-white > div.relative.flex > div.md\:grid-cols-\[1fr_72px\].md2\:grid-cols-\[1fr_420px\].grid.flex-1.grid-cols-1.px-4.pt-5.font-sans-v2.text-\[\#232526\].antialiased.transition-all.xl\:container.sm\:px-6.md\:gap-6.md\:px-7.md\:pt-10.md2\:gap-8.md2\:px-8.xl\:mx-auto.xl\:gap-10.xl\:px-10 > div.min-w-0 > div.mb-\[30px\].flex.flex-col.items-start.gap-5 > div.hidden.w-full.sm\:block.md\:hidden > div > div"
    stat_name: str = ".inline-block"
    stat_value: str = ".key-info_dd-numeric__ZQFIs"
    
    data_script: str = "script[id='__NEXT_DATA__']"
    



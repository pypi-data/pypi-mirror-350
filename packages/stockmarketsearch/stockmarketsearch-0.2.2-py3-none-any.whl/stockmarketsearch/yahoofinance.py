import requests
import logging
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

DOMAIN = "https://finance.yahoo.com"

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

class YahooFinanceScraper:
    def __init__(self):
        pass
    
    def search(self, query: str) -> list[dict]:
        """Search for stocks on Yahoo Finance."""
        url = f"https://query1.finance.yahoo.com/v1/finance/search?q={query}&lang=en-US&region=US&quotesCount=6&newsCount=3&listsCount=2&enableFuzzyQuery=false&quotesQueryId=tss_match_phrase_query&multiQuoteQueryId=multi_quote_single_token_query&newsQueryId=news_cie_vespa&enableCb=false&enableNavLinks=true&enableEnhancedTrivialQuery=true&enableResearchReports=true&enableCulturalAssets=true&enableLogoUrl=true&enableLists=false&recommendCount=5&enablePrivateCompany=true"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            logging.error(f"An error occurred while searching: {e}")
            return []
        return self._extract_search_results(data)
    
    def _extract_search_results(self, data: dict):
        """Extract search results from the JSON response."""
        results = []
        try:
            for item in data["quotes"]:
                if item.get("quoteType") != "EQUITY":
                    continue
                symbol = item.get("symbol")
                result = {
                    "result_from": DOMAIN,
                    "logo": item.get("logoUrl"),
                    "symbol": symbol,
                    "company_name": item.get("longname"),
                    "exchange_name": item.get("exchDisp"),
                    "sector": item.get("sector"),
                    "industry": item.get("industry"),
                    "url": f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?events=capitalGain%7Cdiv%7Csplit&formatted=true&includeAdjustedClose=true&interval=1d&symbol={symbol}&userYfid=true&lang=en-US&region=US",
                }
                results.append(result)
        except Exception as e:
            logging.error(f"An error occurred while extracting search results: {e}")
            return []
        return results
    
    def get_stock_data(self, url: str, start_date: str, end_date: str) -> dict:
        """Get detailed stock data for a given symbol."""
        start_date = self._convert_to_edt(start_date)
        end_date = self._convert_to_edt(end_date)
        url = f"{url}&period1={start_date}&period2={end_date}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            logging.error(f"An error occurred while fetching historical data: {e}")
            return {}
        return self._clean_stock_data(data['chart']['result'][0])
        
    def _clean_stock_data(self, data: dict):
        """Clean and format historical stock data."""
        meta = data.get("meta", {})
        cleaned = {
            "data_from": DOMAIN,
            "currency": meta.get("currency"),
            "symbol": meta.get("symbol"),
            "exchange_name": meta.get("exchangeName"),
            "full_exchange_name": meta.get("fullExchangeName"),
            "instrument_type": meta.get("instrumentType"),
            "first_trade_date": meta.get("firstTradeDate"),
            "regular_market_time": meta.get("regularMarketTime"),
            "has_pre_post_market_data": meta.get("hasPrePostMarketData"),
            "gmt_offset": meta.get("gmtoffset"),
            "timezone": meta.get("timezone"),
            "exchange_timezone_name": meta.get("exchangeTimezoneName"),
            "regular_market_price": meta.get("regularMarketPrice"),
            "fifty_two_week_high": meta.get("fiftyTwoWeekHigh"),
            "fifty_two_week_low": meta.get("fiftyTwoWeekLow"),
            "regular_market_day_high": meta.get("regularMarketDayHigh"),
            "regular_market_day_low": meta.get("regularMarketDayLow"),
            "regular_market_volume": meta.get("regularMarketVolume"),
            "long_name": meta.get("longName"),
            "short_name": meta.get("shortName"),
            "chart_previous_close": meta.get("chartPreviousClose"),
            "price_hint": meta.get("priceHint"),
            "current_trading_period": {
                "pre": {
                "start": self._convert_from_edt(meta['currentTradingPeriod']['pre']['start']),
                "end": self._convert_from_edt(meta['currentTradingPeriod']['pre']['end']),
                },
                "regular": {
                "start": self._convert_from_edt(meta['currentTradingPeriod']['regular']['start']),
                "end": self._convert_from_edt(meta['currentTradingPeriod']['regular']['end']),
                },
                "post": {
                "start": self._convert_from_edt(meta['currentTradingPeriod']['post']['start']),
                "end": self._convert_from_edt(meta['currentTradingPeriod']['post']['end']),
                }
            },
            "historical_data": []
        }
        timestamps = data.get("timestamp", [])
        highs = data['indicators']['quote'][0].get('high', [])
        lows = data['indicators']['quote'][0].get('low', [])
        opens = data['indicators']['quote'][0].get('open', [])
        closes = data['indicators']['quote'][0].get('close', [])
        volumes = data['indicators']['quote'][0].get('volume', [])
        adjusted_closes = data['indicators']['adjclose'][0].get('adjclose', [])
        
        for i in range(len(timestamps)):
            cleaned['historical_data'].append({
                "date": self._convert_from_edt(timestamps[i]) if i < len(timestamps) else None,
                "high": highs[i] if i < len(highs) else None,
                "low": lows[i] if i < len(lows) else None,
                "open": opens[i] if i < len(opens) else None,
                "close": closes[i] if i < len(closes) else None,
                "volume": volumes[i] if i < len(volumes) else None,
                "adjusted_close": adjusted_closes[i] if i < len(adjusted_closes) else None
            })
        return cleaned
        
    def _convert_to_edt(self, date: str):
        date = date.split("-")
        dt_utc = datetime(int(date[0]), int(date[1]), int(date[2]), 0, 0, 0, tzinfo=ZoneInfo("America/New_York"))
        return int(dt_utc.timestamp())
    
    def _convert_from_edt(self, utc: int):
        dt = datetime.fromtimestamp(utc, tz=ZoneInfo("America/New_York"))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    
@dataclass(frozen=True)
class Selectors:
    """CSS selectors for extracting data from Yahoo Finance."""
    company_name: str = "h1.yf-xxbei9"
    currency: str = ".yf-wk4yba span:last-of-type"
    stat_block: str = "li.yf-1jj98ts"
    stat_name: str = ".label"
    stat_value: str = ".value"

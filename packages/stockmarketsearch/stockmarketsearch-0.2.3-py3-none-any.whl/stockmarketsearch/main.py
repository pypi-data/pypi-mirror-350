from .africanmarkets import AfricanMarketsScraper
from .nginvesting import NGInvestingScraper
from .yahoofinance import YahooFinanceScraper
import asyncio


am_scraper = AfricanMarketsScraper()
ng_scraper = NGInvestingScraper()
yf_scraper = YahooFinanceScraper()

async def search(query: str):
    """
    Searches for stock information across multiple sources.
    :param query: The stock or company name to search for.
    :return: A flattened list containing search results from different sources.
    """
    tasks = [
        asyncio.to_thread(am_scraper.search, query),
        asyncio.to_thread(ng_scraper.search, query),
        asyncio.to_thread(yf_scraper.search, query)
    ]
    results = await asyncio.gather(*tasks)
    
    # Flatten the results list (in case each result is a list)
    flattened_results = []
    for result in results:
        flattened_results.extend(result)
    
    return flattened_results

async def get_stock_data(url: str, start_date: str, end_date: str):
    """
    Fetches stock data from multiple sources for a given URL and date range.
    :param url: The URL of the stock page.
    :param start_date: The start date for historical data in 'YYYY-MM-DD' format.
    :param end_date: The end date for historical data in 'YYYY-MM-DD'
    :return: A dictionary containing stock data from different sources.
    """
    if url.startswith("https://ng.investing.com"):
        data = await asyncio.to_thread(ng_scraper.get_stock_data, url, start_date, end_date)
    elif url.startswith("https://www.african-markets.com"):
        data = await asyncio.to_thread(am_scraper.get_stock_data, url, start_date, end_date)
    elif url.startswith("https://query1.finance.yahoo.com"):
        data = await asyncio.to_thread(yf_scraper.get_stock_data, url, start_date, end_date)
    else:
        return {"error": "Unsupported URL format"}
    return data




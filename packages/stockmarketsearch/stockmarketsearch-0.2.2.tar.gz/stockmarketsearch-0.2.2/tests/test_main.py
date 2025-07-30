import pytest
import asyncio
from stockmarketsearch.main import search, get_stock_data

@pytest.mark.asyncio
async def test_search():
    query = "AAPL"
    results = await search(query)
    
    assert "africanmarkets" in results
    assert "nginvesting" in results
    assert "yahoofinance" in results
    assert isinstance(results["africanmarkets"], dict)
    assert isinstance(results["nginvesting"], dict)
    assert isinstance(results["yahoofinance"], dict)

@pytest.mark.asyncio
async def test_get_stock_data():
    url = "https://query1.finance.yahoo.com"
    start_date = "2023-01-01"
    end_date = "2023-01-31"
    data = await get_stock_data(url, start_date, end_date)
    
    assert isinstance(data, dict)
    assert "error" not in data  # Assuming no error for valid URL
    assert "historicalData" in data  # Adjust based on actual expected structure

@pytest.mark.asyncio
async def test_get_stock_data_unsupported_url():
    url = "https://unsupported.url"
    start_date = "2023-01-01"
    end_date = "2023-01-31"
    data = await get_stock_data(url, start_date, end_date)
    
    assert data == {"error": "Unsupported URL format"}
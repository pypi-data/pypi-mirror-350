# Stock Market Search

This project provides a set of tools for searching and retrieving stock information from various online sources, including African Markets, NG Investing, and Yahoo Finance. It utilizes asynchronous programming to efficiently gather data from multiple sources concurrently.

## Features

- Asynchronous search functionality for stock information.
- Fetch historical stock data for specified date ranges.
- Support for multiple data sources.

## Installation

To install the package, you can use pip:

```bash
pip install stockmarketsearch
```

## Usage

Here's a simple example of how to use the `stockmarketsearch` package:

```python
import asyncio
from stockmarketsearch.main import search, get_stock_data

async def main():
    # Search for stock information
    results = await search("AAPL")
    print(results)

    # Get historical stock data
    url = results[0]['url']
    historical_data = await get_stock_data(url, "2023-01-01", "2023-12-31")
    print(historical_data)

asyncio.run(main())
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
<div align="center">
  <h1>LinkGrid X-Transaction-ID</h1>
  
  <p>🔗 A Python package for generating X-Client-Transaction-Id headers used in API requests</p>

  <p>
    <a href="https://pypi.org/project/linkgrid-x-transaction-id/" target="_blank">
      <img src="https://img.shields.io/pypi/v/linkgrid-x-transaction-id?color=blue&label=PyPI" alt="PyPI Version">
    </a>
    <a href="https://www.python.org/downloads/" target="_blank">
      <img src="https://img.shields.io/pypi/pyversions/linkgrid-x-transaction-id?color=blue" alt="Python Version">
    </a>
    <a href="https://choosealicense.com/licenses/mit/" target="_blank">
      <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
    </a>
  </p>
  
  <p>
    <a href="#installation">Installation</a> •
    <a href="#quick-start">Quick Start</a> •
    <a href="#features">Features</a> •
    <a href="#api-reference">API Reference</a>
  </p>
</div>

## ✨ Overview

`deepsaha-x-transaction-id` is a powerful Python package that simplifies the generation of X-Client-Transaction-Id headers required for making authenticated requests to X's (formerly Twitter) API endpoints. It handles all the complexity of generating valid transaction IDs so you can focus on building your application.

## 🚀 Features

- 🔥 **Easy to Use**: Simple and intuitive API for generating transaction IDs
- ⚡ **High Performance**: Optimized for speed and efficiency
- 🔄 **Async Support**: Built-in support for both synchronous and asynchronous operations
- 📦 **Lightweight**: Minimal dependencies, maximum functionality
- 🛡 **Reliable**: Battle-tested and production-ready

## 📦 Installation

Install the package using pip:

```bash
pip install linkgrid-x-transaction-id
```

## 🚀 Quick Start

```python
from linkgrid_x_transaction_id import ClientTransaction

# Create a client instance
client = ClientTransaction()

# Get a transaction ID
transaction_id = client.get_transaction_id()
print(f"Generated Transaction ID: {transaction_id}")
```

import aiohttp
import asyncio
from deepsaha_x_transaction_id import ClientTransaction
from deepsaha_x_transaction_id.utils import generate_headers, handle_x_migration, get_ondemand_file_url

async def main():
    async with aiohttp.ClientSession(headers=generate_headers()) as session:
        # Get home page response
        home_page_response = await handle_x_migration(session, is_async=True)
        
        # Get ondemand file URL and response
        ondemand_file_url = get_ondemand_file_url(home_page_response)
        
        async with session.get(ondemand_file_url) as response:
            ondemand_file_response = await response.text()
        
        # Initialize client and generate transaction ID
        ct = ClientTransaction(home_page_response, ondemand_file_response)
        transaction_id = ct.generate_transaction_id(
            method="POST", 
            path="/i/api/1.1/jot/client_event.json"
        )
        print(f"Generated Transaction ID: {transaction_id}")

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())
```

## 📚 API Reference

### `ClientTransaction` Class

The main class for generating X-Client-Transaction-Id headers.

```python
ClientTransaction(
    home_page_response: bs4.BeautifulSoup, 
    ondemand_file_response: bs4.BeautifulSoup,
    random_keyword: str = "qbg",
    random_number: int = 1
)
```

#### Parameters
- `home_page_response` (bs4.BeautifulSoup): Parsed HTML response from X/Twitter home page
- `ondemand_file_response` (bs4.BeautifulSoup): Parsed HTML response from the ondemand script
- `random_keyword` (str, optional): Custom keyword for transaction ID generation. Defaults to "qbg"
- `random_number` (int, optional): Custom number for transaction ID generation. Defaults to 1

#### Methods

##### `generate_transaction_id(method: str, path: str) -> str`
Generate a transaction ID for the given HTTP method and path.

**Parameters:**
- `method` (str): HTTP method (e.g., "GET", "POST")
- `path` (str): API endpoint path (e.g., "/i/api/1.1/jot/client_event.json")

**Returns:**
- `str`: Generated transaction ID string

### Utility Functions

#### `generate_headers() -> Dict[str, str]`
Generate default headers for X/Twitter API requests.

#### `handle_x_migration(session: requests.Session, is_async: bool = False) -> Union[bs4.BeautifulSoup, Coroutine]`
Handle the X/Twitter migration and return the parsed home page response.

#### `get_ondemand_file_url(response: bs4.BeautifulSoup) -> str`
Extract the ondemand script URL from the home page response.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Deep Saha**

- Website: [deepsaha.com](https://deepsaha.com)
- Twitter: [@DeepSahaDev](https://x.com/LegendDeep2003)
- GitHub: [@OfficialDeepSaha](https://github.com/OfficialDeepSaha)


## Feedback

If you have any feedback, please reach out to us at hiremeasadeveloper@gmail.com or contact me on Social Media @LegendDeep2003

## Support

For support, email hiremeasadeveloper@gmail.com

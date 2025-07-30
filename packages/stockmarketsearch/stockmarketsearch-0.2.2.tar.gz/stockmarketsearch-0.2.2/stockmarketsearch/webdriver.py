from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import cloudscraper
from concurrent.futures import ThreadPoolExecutor

def webdriver_options() -> Options:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--enable-unsafe-swiftshader")
    return options

def _init_driver():
    driver = webdriver.Chrome(options=webdriver_options())
    return driver

def start_webdriver() -> webdriver:
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(_init_driver)
        driver = future.result()  # Waits for the driver to be ready
    return driver

def get_cloudscraper() -> cloudscraper.CloudScraper:
    scraper = cloudscraper.create_scraper(
        browser={
            "browser": "chrome",
            "platform": "windows",
        },
    )
    return scraper
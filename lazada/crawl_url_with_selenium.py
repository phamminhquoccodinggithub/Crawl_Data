"""Module for web scraping using Selenium and pandas."""
from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains


def setup_driver():
    """
    Set up the Selenium WebDriver with Chrome options.

    This function configures Chrome options for optimal web scraping performance
    and returns an instance of the Chrome WebDriver.

    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance.
    """
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.page_load_strategy = 'eager'
    chrome_options.add_argument("enable-automation")
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--dns-prefetch-disable")
    chrome_options.add_argument("--window-size=1300,900")

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_item_info():
    """
    Retrieve item information from the Lazada website.

    This function navigates through multiple pages of Lazada's product listings,
    collecting URLs for individual items. It handles potential pop-ups and
    scrolls through the page to load more items.

    The function uses Selenium to interact with the web page, clicking through
    pagination and avoiding interruptions like QR code prompts or pop-up windows.

    Returns:
        list: A list of URLs for individual product pages on Lazada.

    Note:
        This function assumes that the WebDriver (driver) has already been set up
        and the initial page has been loaded. It also assumes specific XPaths and
        CSS selectors for elements on the Lazada website, which may need to be
        updated if the website structure changes.
    """
    df = []
    for _ in range(1, 50):
        try:
            avoid_qr_btn = driver.find_element(
                "xpath", '/html/body/div[9]/div[2]/div')
            avoid_qr_btn.click()
        except:
            pass

        try:
            close_btn = driver.find_element(
                "xpath", '/html/body/div[8]/div/div[2]/div/span/i')
            close_btn.click()
        except:
            pass

        driver.execute_script("window.scrollTo(0,1200)")
        sleep(3)

        elems_content = driver.find_elements(
            By.CSS_SELECTOR, ".Bm3ON .Ms6aG.MefHh .qmXQo .ICdUp ._95X4G [href]")
        url = [elem.get_attribute('href') for elem in elems_content]

        df.extend(url)

        try:
            avoid_qr_btn = driver.find_element(
                "xpath", '/html/body/div[9]/div[2]/div')
            avoid_qr_btn.click()
        except:
            pass

        try:
            next_pagination_cmt = driver.find_element(
                "xpath", '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[3]/div/ul/li[11]/button')
            ActionChains(driver).scroll_to_element(
                next_pagination_cmt).perform()
            next_pagination_cmt.click()
        except:
            pass
    return df


if __name__ == '__main__':
    """
    Main execution function for the web scraping script.

    This function sets up the WebDriver, retrieves item URLs, and processes each
    item to extract and save comments. It handles the entire workflow from
    initializing the driver to fetching and saving data.
    """
    driver = setup_driver()
    links = 'https://www.lazada.vn/catalog/?_keyori=ss&from=search_history&page=1&q=giay&spm=a2o4n.homepage.search.2.19053bdcibER4w&sugg=giay_0_1'
    driver.get(links)
    df = get_item_info()
    df = pd.DataFrame(df).to_csv('url.csv')
    driver.quit()

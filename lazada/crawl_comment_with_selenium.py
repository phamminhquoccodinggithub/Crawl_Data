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
    # chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--dns-prefetch-disable")
    chrome_options.add_argument("--window-size=1300,900")

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_url_item():
    """
    Retrieve URLs of Lazada items from a CSV file.

    This function reads a CSV file named 'lazada_item_url.csv', which contains
    URLs of Lazada items. It processes these URLs to ensure they have the correct
    format (replacing the first two characters with 'https://') and returns them
    as a list.

    Returns:
        list: A list of processed Lazada item URLs.
    """
    df = pd.read_csv('lazada_item_url.csv')
    p_ids = df.url.to_list()
    links = []
    for i in range(0, len(p_ids)):
        current_url = p_ids[i]
        current_url = current_url.replace(current_url[0:2], 'https://')
        links.append(current_url)
    return links


def get_comment():
    """
    Retrieve comments from a Lazada product page.

    This function scrapes comments from a Lazada product page, including the content
    and SKU information for each comment. It handles pagination and attempts to
    avoid potential pop-ups or interruptions during the scraping process.

    The function uses Selenium WebDriver to interact with the page, scrolling and
    clicking as necessary to load and access comments across multiple pages.

    Returns:
        dict: A dictionary containing lists of comment content and SKU information.
              Keys are 'content_comment' and 'skuInfo_comment'.

    Note:
        - This function assumes that the WebDriver (driver) is already initialized
          and navigated to the correct product page.
        - It attempts to scrape comments from up to 10 pages.
        - The function includes error handling for common interruptions like
          QR code pop-ups and close buttons.
    """
    # df = {
    #     'content_comment': [],
    #     'skuInfo_comment': []
    # }
    df = []

    for _ in range(1, 3):
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
            By.CSS_SELECTOR, ".item-content .content")
        content_comment = [elem.text for elem in elems_content]

        # elems_skuInfo = driver.find_elements(
        #     By.CSS_SELECTOR, ".item-content .skuInfo")
        # skuInfo_comment = [elem.text for elem in elems_skuInfo]

        # df['content_comment'].extend(content_comment)
        # df['skuInfo_comment'].extend(skuInfo_comment)
        df.extend(content_comment)

        try:
            avoid_qr_btn = driver.find_element(
                "xpath", '/html/body/div[9]/div[2]/div')
            avoid_qr_btn.click()
        except:
            pass

        try:
            next_pagination_cmt = driver.find_element(
                "xpath", '//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/button[2]')
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
    links = get_url_item()
    df = []
    for i in range(1, 3):
        driver.get(links[i])
        sleep(5)
        df.append(get_comment())
    # for link in links:
    #     driver.get(link)
    #     sleep(5)
    #     df[link] = get_comment()
    df = pd.DataFrame(df).to_csv('lazada_comment.csv')
    driver.quit()

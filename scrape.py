
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
AUTH = 'brd-customer-hl_b045f9b3-zone-ai_scrap:bx58ylrfgg9i'
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'
import time

def scrape_website(website):
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        driver.get(website)
        print('Taking page screenshot to file page.png')
        driver.get_screenshot_as_file('./page.png')
        print('Navigated! Scraping page content...')
        html = driver.page_source
        return html
    
def extract_body_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.body
    if body:
        return str(body)
    return ""

def clean_body_content(body):
    soup = BeautifulSoup(body, 'html.parser')

    for script in soup(['script', 'style']):
        script.extract()

    clean_body = soup.get_text(separator='\n')
    clean_body = "\n".join(line.strip() for line in clean_body.splitlines() if line.strip())
    return clean_body

def split_dom_content(dom_content, max_length=6000):
    return[
        dom_content[i:i+max_length] for i in range(0, len(dom_content), max_length)
    ]
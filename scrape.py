# from selenium.webdriver import Remote, ChromeOptions
# from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
# from bs4 import BeautifulSoup
# from dotenv import load_dotenv
# import os

# load_dotenv()

# SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")


# def scrape_website(website):
#     print("Connecting to Scraping Browser...")
#     sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
#     with Remote(sbr_connection, options=ChromeOptions()) as driver:
#         driver.get(website)
#         print("Waiting captcha to solve...")
#         solve_res = driver.execute(
#             "executeCdpCommand",
#             {
#                 "cmd": "Captcha.waitForSolve",
#                 "params": {"detectTimeout": 10000},
#             },
#         )
#         print("Captcha solve status:", solve_res["value"]["status"])
#         print("Navigated! Scraping page content...")
#         html = driver.page_source
#         return html


# def extract_body_content(html_content):
#     soup = BeautifulSoup(html_content, "html.parser")
#     body_content = soup.body
#     if body_content:
#         return str(body_content)
#     return ""


# def clean_body_content(body_content):
#     soup = BeautifulSoup(body_content, "html.parser")

#     for script_or_style in soup(["script", "style"]):
#         script_or_style.extract()

#     # Get text or further process the content
#     cleaned_content = soup.get_text(separator="\n")
#     cleaned_content = "\n".join(
#         line.strip() for line in cleaned_content.splitlines() if line.strip()
#     )

#     return cleaned_content


# def split_dom_content(dom_content, max_length=6000):
#     return [
#         dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
#     ]
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def scrape_website(website):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0")

    print("Launching browser...")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(website)
        time.sleep(5)  # Wait for content to load or JavaScript to render

        print("✅ Page loaded. Extracting content...")
        html = driver.page_source
        return html

    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        return ""

    finally:
        driver.quit()


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    return str(body_content) if body_content else ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for tag in soup(["script", "style", "noscript", "footer", "nav", "svg", "img"]):
        tag.extract()

    text = soup.get_text(separator="\n")
    cleaned_text = "\n".join(
        line.strip() for line in text.splitlines() if line.strip()
    )
    return cleaned_text


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i: i + max_length]
        for i in range(0, len(dom_content), max_length)
    ]


# Example usage
if __name__ == "__main__":
    url = input("🔗 Enter the website URL to scrape: ").strip()
    html = scrape_website(url)
    if html:
        raw_body = extract_body_content(html)
        cleaned_text = clean_body_content(raw_body)
        chunks = split_dom_content(cleaned_text)

        for idx, chunk in enumerate(chunks, 1):
            with open(f"page_chunk_{idx}.txt", "w", encoding="utf-8") as f:
                f.write(chunk)
        print(f"✅ Extracted {len(chunks)} text chunk(s). Saved to files.")
    else:
        print("⚠️ No HTML content extracted.")


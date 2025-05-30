from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
from datetime import datetime

import json
import time
import random
import logging

CURRENT_TIME = datetime.now().strftime("%d-%m-%Y")

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AIToolsScraper:
    """
    AI Tools Scraper Class

    Functions:
        setup_driver:
        wait_for_content_load:
        wait_for_elements:
        wait_for_main_list:
        wait_for_network_idle:
        wait_for_page_ready:
        scroll_to_load_content:
        extract_tools_from_page:
        debug_main_list_structure:
        save_page_html:
        extract_tool_data:
        fallback_extraction:
        scrape_page:
        scrape_multiple_pages:
        remove_duplicates:
        save_tools:
        print_tools:
        close:
    """

    def __init__(self, headless=True, wait_time=10):
        self.wait_time = wait_time
        self.setup_driver(headless)
        self.tools = []

    def setup_driver(self, headless=True):
        chrome_options = Options()

        if headless:
            chrome_options.add_argument("--headless")

        # Anti-detection measures
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        # Realistic browser settings
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")

        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            self.wait = WebDriverWait(self.driver, self.wait_time)
            logger.info("WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise

    def wait_for_content_load(self, max_wait=30):
        logger.info("Waiting for content to load...")

        # Primary strategy: Wait for the specific tools list
        if self.wait_for_main_list():
            return True

        # Fallback strategies if main list selector fails
        strategies = [
            # Strategy 1: Wait for general selectors that might contain tools
            lambda: self.wait_for_elements(
                [
                    ".sv-tiles-list",
                    ".tool-card",
                    ".ai-tool",
                    ".tool-item",
                    ".card",
                    '[class*="tool"]',
                    '[class*="card"]',
                    ".grid > div",
                ]
            ),
            lambda: self.wait_for_network_idle(),
            lambda: self.wait_for_page_ready(),
        ]

        for i, strategy in enumerate(strategies, 1):
            try:
                logger.info(f"Trying fallback loading strategy {i}")
                if strategy():
                    logger.info(f"Content loaded using fallback strategy {i}")
                    return True
                time.sleep(2)
            except Exception as e:
                logger.warning(f"Fallback strategy {i} failed: {e}")
                continue

        # Final fallback: just wait a fixed time
        logger.info("Using final fallback wait time")
        time.sleep(max_wait)
        return True

    def wait_for_elements(self, selectors, timeout=15):
        for selector in selectors:
            try:
                element = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if element:
                    logger.info(f"Found elements with selector: {selector}")
                    return True
            except TimeoutException:
                continue
        return False

    def wait_for_main_list(self, timeout=20):
        main_list_selector = ".sv-tiles-list.sv-tiles-list--flex.sv-tiles-list--tile-view.sv-tiles-list--small-size"
        try:
            logger.info("Waiting for main tools list to load...")
            element = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, main_list_selector))
            )

            tools_selector = f"{main_list_selector} > *"
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, tools_selector))
            )

            logger.info("Main tools list loaded successfully")
            return True
        except TimeoutException:
            logger.warning("Main tools list not found within timeout")
            return False

    def wait_for_network_idle(self, timeout=20):
        try:
            self.driver.execute_async_script(
                """
                var callback = arguments[arguments.length - 1];
                var timeout = setTimeout(function() {
                    callback(true);
                }, arguments[0] * 1000);

                // Override fetch and XMLHttpRequest to track requests
                var pendingRequests = 0;
                var originalFetch = window.fetch;
                var originalXHR = window.XMLHttpRequest.prototype.open;

                window.fetch = function() {
                    pendingRequests++;
                    return originalFetch.apply(this, arguments).finally(() => {
                        pendingRequests--;
                        if (pendingRequests === 0) {
                            clearTimeout(timeout);
                            callback(true);
                        }
                    });
                };
            """,
                timeout,
            )
            return True
        except:
            return False

    def wait_for_page_ready(self):
        """Wait for page ready state and no loading indicators"""
        try:
            # Wait for document ready
            self.wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )

            # Wait for common loading indicators to disappear
            loading_selectors = [
                ".loading",
                ".spinner",
                ".loader",
                '[class*="loading"]',
                '[class*="spinner"]',
                '[class*="loader"]',
            ]

            for selector in loading_selectors:
                try:
                    self.wait.until(
                        EC.invisibility_of_element_located((By.CSS_SELECTOR, selector))
                    )
                except TimeoutException:
                    pass  # Loading indicator might not exist

            return True
        except:
            return False

    def scroll_to_load_content(self):
        logger.info("Scrolling to trigger lazy loading...")

        # Get initial height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        scroll_attempts = 0
        max_attempts = 5

        while scroll_attempts < max_attempts:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(2)

            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height
            scroll_attempts += 1
            logger.info(f"Scroll attempt {scroll_attempts}, new height: {new_height}")

        # Scroll back to top
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

    def extract_tools_from_page(self):
        logger.info("Extracting tools from page...")

        # Get page source after JavaScript execution
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # First, try to find the main tools list container
        main_list_selector = "div.sv-tiles-list.sv-tiles-list--flex.sv-tiles-list--tile-view.sv-tiles-list--small-size"
        main_list = soup.select_one(main_list_selector)

        tools_found = []

        if main_list:
            logger.info("Found main tools list container")

            tool_elements = main_list.find_all(recursive=False)
            logger.info(
                f"Found {len(tool_elements)} direct child elements in main list"
            )

            if not tool_elements:
                tool_elements = main_list.find_all(["div", "article", "section"])
                logger.info(
                    f"Found {len(tool_elements)} descendant elements in main list"
                )

            # Extract data from each tool element
            for element in tool_elements:
                tool_data = self.extract_tool_data(element)
                if tool_data and tool_data.get("name"):
                    tools_found.append(tool_data)

        # Fallback: try other common selectors if main list approach didn't work
        if not tools_found:
            logger.info("Main list approach failed, trying fallback selectors...")

            selectors_to_try = [
                ".sv-tiles-list div",
                ".sv-tiles-list > div",
                ".sv-tiles-list article",
                ".tool-card",
                ".ai-tool",
                ".tool-item",
                ".directory-item",
                ".card",
                ".item",
                ".product-card",
                ".listing-item",
                '[class*="tool"]',
                '[class*="card"]',
                '[class*="item"]',
                ".grid > div",
                ".list > div",
                ".container > div",
            ]

            for selector in selectors_to_try:
                elements = soup.select(selector)
                if elements and len(elements) > 2:
                    logger.info(
                        f"Using fallback selector '{selector}' - found {len(elements)} elements"
                    )

                    for element in elements:
                        tool_data = self.extract_tool_data(element)
                        if tool_data and tool_data.get("name"):
                            tools_found.append(tool_data)

                    if tools_found:
                        break

        if not tools_found:
            logger.info("Trying final fallback extraction method...")
            tools_found = self.fallback_extraction(soup)

        logger.info(f"Extracted {len(tools_found)} tools from current page")
        return tools_found

    def debug_main_list_structure(self):
        logger.info("Debugging main list structure...")

        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        main_list_selector = "div.sv-tiles-list.sv-tiles-list--flex.sv-tiles-list--tile-view.sv-tiles-list--small-size"
        main_list = soup.select_one(main_list_selector)

        if main_list:
            print(f"\n{'=' * 60}")
            print("MAIN LIST STRUCTURE DEBUG")
            print(f"{'=' * 60}")

            direct_children = main_list.find_all(recursive=False)
            print(f"Direct children count: {len(direct_children)}")

            for i, child in enumerate(direct_children[:3], 1):  # Show first 3
                print(f"\nChild {i}:")
                print(f"  Tag: {child.name}")
                print(f"  Classes: {child.get('class', [])}")
                print(f"  Text preview: {child.get_text(strip=True)[:100]}...")

                links = child.find_all("a")
                if links:
                    print(f"  Links found: {len(links)}")
                    for link in links[:2]:  # Show first 2 links
                        print(
                            f"    - {link.get('href', 'No href')} | Text: {link.get_text(strip=True)[:50]}"
                        )

            print(f"\nHTML Structure Preview:")
            print(
                str(main_list)[:500] + "..."
                if len(str(main_list)) > 500
                else str(main_list)
            )

        else:
            print("Main list container not found!")

            similar_containers = soup.select("div[class*='sv-tiles-list']")
            print(
                f"Found {len(similar_containers)} elements with 'sv-tiles-list' in class"
            )

            for container in similar_containers:
                print(f"Classes: {container.get('class', [])}")

    def save_page_html(self, filename="debug_page.html"):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
        logger.info(f"Page HTML saved to {filename}")

    def extract_tool_data(self, element):
        tool_data = {}

        title_selectors = [
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            '[class*="sv-tile__title sv-text-reset sv-is-link"]'  # Standard headings
            ".title",
            ".name",
            ".tool-name",
            ".product-name",  # Common title classes
            '[class*="title"]',
            '[class*="name"]',  # Partial class matches
            "a[href]",  # Links often contain tool names
            "strong",
            "b",  # Bold text
            ".sv-tile-title",
            ".sv-title",  # SV-specific classes
        ]

        for selector in title_selectors:
            title_elem = element.select_one(selector)
            if title_elem and title_elem.get_text(strip=True):
                title_text = title_elem.get_text(strip=True)
                # Skip very short or very long titles
                if 3 <= len(title_text) <= 100:
                    tool_data["name"] = title_text
                    break

        desc_selectors = [
            ".description",
            ".desc",
            ".summary",
            ".overview",
            '[class*="desc"]',
            '[class*="summary"]',
            "p",  # Paragraphs
            "sv-tile__description sv-text-reset",
            ".sv-tile-description",
            ".sv-description",  # SV-specific
        ]

        for selector in desc_selectors:
            desc_elem = element.select_one(selector)
            if desc_elem and desc_elem.get_text(strip=True):
                desc_text = desc_elem.get_text(strip=True)
                # Look for meaningful descriptions (not too short, not the same as title)
                if len(desc_text) > 20 and desc_text != tool_data.get("name", ""):
                    tool_data["description"] = desc_text
                    break

        if not tool_data.get("description"):
            all_text_elements = element.find_all(string=True)
            text_contents = [text.strip() for text in all_text_elements if text.strip()]
            if text_contents:
                # Find the longest text that's not the title
                longest_text = max(text_contents, key=len, default="")
                if len(longest_text) > 20 and longest_text != tool_data.get("name", ""):
                    tool_data["description"] = longest_text

        link_elements = element.select("a[href]")
        for link_elem in link_elements:
            href = link_elem.get("href", "")
            if href and not href.startswith("#"):
                if href.startswith("http"):
                    tool_data["url"] = href
                    break
                elif href.startswith("/") and "aitoolsdirectory.com" not in href:
                    # Skip internal directory links, look for external ones
                    continue
                elif href.startswith("/"):
                    tool_data["url"] = f"https://aitoolsdirectory.com{href}"

        tag_selectors = [
            ".tag",
            ".category",
            ".badge",
            ".label",
            ".chip",
            '[class*="tag"]',
            '[class*="category"]',
            '[class*="badge"]',
            ".sv-tag",
            ".sv-category",  # SV-specific
        ]

        tags = []
        for selector in tag_selectors:
            tag_elements = element.select(selector)
            for tag_elem in tag_elements:
                tag_text = tag_elem.get_text(strip=True)
                if tag_text and 2 <= len(tag_text) <= 30:  # Reasonable tag length
                    tags.append(tag_text)

        if tags:
            tool_data["tags"] = list(set(tags))  # Remove duplicates

        price_selectors = [
            ".price",
            ".pricing",
            ".cost",
            ".plan",
            '[class*="price"]',
            '[class*="cost"]',
            '[class*="plan"]',
            ".sv-price",
            ".sv-pricing",
        ]

        for selector in price_selectors:
            price_elem = element.select_one(selector)
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                if price_text and len(price_text) <= 50:
                    tool_data["pricing"] = price_text
                    break

        return tool_data

    def fallback_extraction(self, soup):
        tools = []
        ai_keywords = [
            "ai tool",
            "artificial intelligence",
            "machine learning",
            "chatbot",
            "automation",
        ]

        for keyword in ai_keywords:
            elements = soup.find_all(
                text=lambda text: text and keyword.lower() in text.lower()
            )

            for text_elem in elements[:10]:  # Limit to avoid too many results
                parent = text_elem.parent
                if parent:
                    # Try to extract meaningful data from parent elements
                    tool_data = self.extract_tool_data(parent)
                    if tool_data.get("name"):
                        tools.append(tool_data)

        return tools

    def scrape_page(self, url, page_num=1):
        logger.info(f"Scraping page {page_num}: {url}")

        try:
            self.driver.get(url)
            self.wait_for_content_load()
            self.scroll_to_load_content()

            tools = self.extract_tools_from_page()
            for tool in tools:
                tool["page"] = page_num

            return tools

        except Exception as e:
            logger.error(f"Error scraping page {page_num}: {e}")
            return []

    def scrape_multiple_pages(self, base_url, max_pages=5):
        all_tools = []

        for page in range(1, max_pages + 1):
            url = f"{base_url}?page={page}"

            page_tools = self.scrape_page(url, page)
            all_tools.extend(page_tools)

            if page < max_pages:
                delay = random.uniform(2, 5)
                logger.info(f"Waiting {delay:.1f} seconds before next page...")
                time.sleep(delay)

        # Remove duplicates based on name
        unique_tools = self.remove_duplicates(all_tools)
        logger.info(f"Total unique tools scraped: {len(unique_tools)}")

        return unique_tools

    def remove_duplicates(self, tools):
        seen_names = set()
        unique_tools = []

        for tool in tools:
            name = tool.get("name", "").lower().strip()
            if name and name not in seen_names:
                seen_names.add(name)
                unique_tools.append(tool)

        return unique_tools

    def save_tools(self, tools, filename=f"../etl/data/{CURRENT_TIME}_ai_tools_scraped.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(tools, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(tools)} tools to {filename}")

    def print_tools(self, tools):
        for i, tool in enumerate(tools, 1):
            print(f"\n{i}. {tool.get('name', 'Unknown Tool')}")
            if tool.get("description"):
                desc = (
                    tool["description"][:150] + "..."
                    if len(tool["description"]) > 150
                    else tool["description"]
                )
                print(f"   Description: {desc}")
            if tool.get("url"):
                print(f"   URL: {tool['url']}")
            if tool.get("tags"):
                print(
                    f"   Tags: {', '.join(tool['tags'][:5])}{'...' if len(tool['tags']) > 5 else ''}"
                )
            if tool.get("pricing"):
                print(f"   Pricing: {tool['pricing']}")
            if tool.get("page"):
                print(f"   Found on page: {tool['page']}")

    def close(self):
        if hasattr(self, "driver"):
            self.driver.quit()
            logger.info("WebDriver closed")


def main(all_page: int):
    scraper = None

    try:
        print("AI Tools Directory Scraper")
        print("=" * 40)

        scraper = AIToolsScraper(wait_time=15)
        base_url = "https://aitoolsdirectory.com/"

        max_pages = all_page
        max_pages = min(max_pages, 10)

        print(f"\nStarting to scrape {max_pages} pages...")
        tools = scraper.scrape_multiple_pages(base_url, max_pages)

        if tools:
            print(f"\n{'=' * 60}")
            print(f"SCRAPING COMPLETED - Found {len(tools)} unique AI tools")
            print(f"{'=' * 60}")

            scraper.save_tools(tools)
        else:
            print("No tools were scraped. The website structure might have changed.")

    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
    except Exception as e:
        logger.error(f"Scraping failed: {e}")

    finally:
        if scraper:
            scraper.close()


if __name__ == "__main__":
    main(4)

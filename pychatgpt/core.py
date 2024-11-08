"""
ChatGPT API Module
"""
import os
import platform
import time
import pyperclip

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

import undetected_chromedriver as uc

LOGIN_PAGE_TIME_OUT = 10
NOTIFICATION_WINDOW_TIME_OUT = 30
RESPONSE_GENERATION_TIME_OUT = 300

LOGIN_URL = "https://chatgpt.com"

class ChatGPT:
    def __init__(self, auth_file_path=None, username=None, 
                 password=None, headless=False, uc_driver=True, 
                 login=False):
        self._is_ready = False
        self._driver = None
        self.headless = headless
        self.uc_driver = uc_driver
        self.login = login

        if login:
            self.username = username
            self.password = password
            self.auth_file_path = auth_file_path
            if (not self.username or not self.password) and self.auth_file_path:
                self._read_login_credentials()
                
            if self.username and self.password:
                self._setup_engine()
            else:
                print("Error: login credentials are not provided.")
        else:
            self._setup_engine()

    def _read_login_credentials(self):
        """Read login credentials from file."""
        username = None
        password = None
        with open(self.auth_file_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("username"):
                    username = line.split("=")[1].strip()
                    continue
                if line.startswith("password"):
                    password = line.split("=")[1].strip()
                    continue
        assert username is not None and password is not None
        self.username = username
        self.password = password

    def _setup_engine(self):
        driver = self._build_driver()
        print("Initialized driver...")
        driver.get(LOGIN_URL)

        if self.login:
            # Click the Log In button
            driver.find_element(By.XPATH, "//button/div[text()='Log in']").click()

            WebDriverWait(driver, timeout=LOGIN_PAGE_TIME_OUT).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))

            # Enter account email
            driver.find_element(By.XPATH, '//input[@id="username"]').send_keys(self.username)

            # Click the Continue button
            driver.find_element(By.XPATH, '//button[@type="submit"]').click()

            # Enter account password
            driver.find_element(By.XPATH, '//input[@id="password"]').send_keys(self.password)

            # Click the unhidden Continue button
            driver.find_elements(By.XPATH, '//button[@type="submit"]')[1].click()

            # Handle notification windows
            while True:
                try:
                    # Click the Next buttons if exist
                    WebDriverWait(driver, timeout=NOTIFICATION_WINDOW_TIME_OUT).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Next']")))
                    driver.find_element(By.XPATH, "//div[text()='Next']").click()
                except:
                    # Click the Done button in the end
                    WebDriverWait(driver, timeout=NOTIFICATION_WINDOW_TIME_OUT).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Done']")))
                    driver.find_element(By.XPATH, "//div[text()='Done']").click()
                    break
        self._is_ready = True

    def _is_alive(self):
        driver = self._driver
        if not self._is_ready:
            return False
        
        try:
            # Check if the "New chat" button is there
            driver.find_element(By.XPATH, "//a[text()='New chat']")
        except:
            return False
        return True

    def _build_driver(self):
        if self.uc_driver:
            options = uc.ChromeOptions()
            if self.headless:
                options.add_argument('--headless')
            
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--start-maximized')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

            os_name = platform.system()
            if os_name == "Linux":
                executable = "chromedriver-linux"
            elif os_name == "Darwin":  # macOS
                executable = "chromedriver-mac"
            driver = uc.Chrome(
                driver_executable_path=os.path.join(os.path.dirname(__file__), f"../{executable}"),
                options=options
            )
        else:
            options = webdriver.ChromeOptions()
            if self.headless:
                options.add_argument("--headless")
                options.add_argument('--disable-gpu')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument("--enable-javascript")
                options.add_argument("--window-size=1920,1080")

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(
                service=service,
                options=options
            )
        self._driver = driver
        return driver

    def _traverse_response_tree(self, root, responses):
        children = root.find_elements(By.XPATH, "./*")
        print("children:", len(children))
        for elem in children:
            if elem.tag_name in ["p", "li"]:
                responses.append({
                    "type": "text",
                    "content": elem.text
                })
            elif elem.tag_name == "pre":
                parts = elem.text.split("\n")
                code_lang = parts[0]
                code_snippet = "\n".join(parts[2:])
                responses.append({
                    "type": "code",
                    "lang": code_lang,
                    "content": code_snippet
                })
            else:
                self._traverse_response_tree(elem, responses)

    def predict(self, prompt):
        """Retrieve the response of a prompt."""
        driver = self._driver
        os_name = platform.system()

        # Copy the text to the clipboard
        pyperclip.copy(prompt)

        WebDriverWait(driver, timeout=NOTIFICATION_WINDOW_TIME_OUT).until(
            EC.visibility_of_element_located((
                By.XPATH, "//div[@id='prompt-textarea']//p")))
        input_box = driver.find_element(by=By.XPATH, value="//div[@id='prompt-textarea']//p")
        input_box.click()
        if os_name == "Linux":
            input_box.send_keys(Keys.CONTROL, 'v')
        elif os_name == "Darwin":  # macOS
            input_box.send_keys(Keys.COMMAND, 'v')
        input_box.send_keys(Keys.RETURN)

        print("Generating...")
        # Wait for results fully loaded
        WebDriverWait(driver, timeout=RESPONSE_GENERATION_TIME_OUT).until_not(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='stop-button']")))
        
        print("Finish generating...")
        WebDriverWait(driver, timeout=NOTIFICATION_WINDOW_TIME_OUT).until(
            EC.presence_of_element_located((
                By.XPATH, "//button[@data-testid='copy-turn-action-button']")))
        response_elements = driver.find_elements(by=By.XPATH, value="//div[@data-message-author-role='assistant']")
        print("response_elements:", len(response_elements))
        response_content = response_elements[-1].find_element(By.XPATH, "//div[contains(@class, 'markdown')]")
        
        result_json = dict()
        result_json["prompt"] = prompt
        result_json["response"] = list()
        self._traverse_response_tree(response_content, result_json["response"])
        return result_json
    
    def new_chat(self):
        """Create a new chat."""
        driver = self._driver
        driver.find_element(By.XPATH, "//nav[contains(@class, 'flex-col')]").find_element(By.XPATH, "//a").click()
    
    def delete_current_chat(self):
        """Delete the current chat."""
        driver = self._driver
        sessions = driver.find_element(By.XPATH, "//nav[contains(@class, 'flex-col')]").find_elements(By.XPATH, "//li")
        sessions[0].find_elements(By.XPATH, "//button")[3].click()
        time.sleep(3)
        sessions[0].find_elements(By.XPATH, "//button")[1].click()
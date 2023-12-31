"""
ChatGPT API Module
"""
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc

LOGIN_PAGE_TIME_OUT = 10
NOTIFICATION_WINDOW_TIME_OUT = 5
RESPONSE_GENERATION_TIME_OUT = 300

LOGIN_URL = "https://chat.openai.com"

class ChatGPT:
    def __init__(self, auth_file_path=None, username=None, 
                 password=None, headless=True):
        self._is_ready = False
        self._driver = None
        self.headless = headless
        self.username = username
        self.password = password
        self.auth_file_path = auth_file_path
        if (not self.username or not self.password) and self.auth_file_path:
            self._read_login_credentials()
            
        if self.username and self.password:
            self._setup_engine()
        else:
            print("Error: login credentials are not provided.")

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
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument("--headless")
        driver = uc.Chrome(options=options)
        self._driver = driver
        return driver

    def _traverse_response_tree(self, root, responses):
        children = root.find_elements(By.XPATH, "./*")        
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
        input_box = driver.find_element(by=By.XPATH, value='//textarea[contains(@placeholder, "Send a message")]')
        input_box.send_keys(prompt)
        input_box.send_keys(Keys.RETURN)

        # Wait for results fully loaded
        WebDriverWait(driver, timeout=RESPONSE_GENERATION_TIME_OUT).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Regenerate response']")))
        
        response_elements = driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')
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
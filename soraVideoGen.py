from selenium import webdriver
from selenium.webdriver.common.by import By # location methods
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
import numpy as np

class SoraVideoGenerator:
    def __init__(self, myuserprofile: str):
        options = webdriver.ChromeOptions()
        
        # Use your existing Chrome profile
        options.add_argument(f'--user-data-dir={myuserprofile}')

        self.driver = webdriver.Chrome(options=options)
        time.sleep(6 + np.random.randint(0, 10) / 6)
        self.textarea = self.find_text_area()

    def enterPrompt(self, prompt: str):
        # Find and enter text into the prompt textarea
        textarea = self.textarea
        textarea.clear()
        # Handle any newlines in the prompt by sending them as literal characters
        for char in prompt:
            if char == '\n':
                textarea.send_keys(Keys.SHIFT + Keys.ENTER)
            else:
                textarea.send_keys(char)
        textarea.send_keys(Keys.RETURN)
        time.sleep(1 + np.random.randint(0, 10) / 6)

    def editDisplayRatio(self, ratio: str):
        """
        A currrently defunct method meant to enable control over the display ratio.
        """
        # Find and click the display ratio button
        # Find and click the display ratio button using the exact class and attributes
        edit_ratio_button = self.driver.find_element(By.CSS_SELECTOR, 
            "button.inline-flex.gap-1\\.5.items-center.justify-center.whitespace-nowrap.text-sm[role='combobox']")
        edit_ratio_button.click()
        print("clicked")

        time.sleep(2)
        # Wait for the panel to be present AND visible
        wait = WebDriverWait(self.driver, 10)
        edit_ratio_panel = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='radix-popper-content-wrapper']"))
        )
        print('k')
        edit_ratio_panel.click()
        time.sleep(1)
        print("clicked2")
        edit_display_ratio_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Edit display ratio']")
        parent = self.driver.find_element(By.CSS_SELECTOR, "div[class*='radix-popper-content-wrapper']")
        children = parent.find_elements(By.XPATH, ".//*")  # All descendants
        for child in children:
            print(child.get_attribute("class"))
            if child.get_attribute("class") == "radix-select-trigger":
                child.click()
                break
    
    def find_text_area(self):
        return self.driver.find_element("css selector", 
            "textarea.flex.w-full.rounded-md[placeholder='Describe your video...']")

    def detect_queue_length(self):
        # Check for notification bell SVG to detect queue length
        try:
            bell_svg = self.driver.find_element(By.CSS_SELECTOR, 
                "svg[viewBox='0 0 24 24'] path[d*='M3.8 9.603a8.248 8.248 0 0 1 16.399 0']")
            return 0
        except:
            return 1
    
    def submit(self):
        try:
            self.textarea.send_keys(Keys.RETURN)
        except Exception as e:
            print('self.textarea', str(self.textarea))
            raise e
    
    def submitPrompts(self, prompts: list[str]):
        for prompt in prompts:
            print(prompt)
            self.enterPrompt(prompt)
            time.sleep(3 + np.random.randint(0, 10) / 6)
            #self.submit()
            time.sleep(1 + np.random.randint(0, 10) / 6)
            while self.detect_queue_length() == 1:
                time.sleep(1 + np.random.randint(0, 10) / 6)
        self.driver.quit()
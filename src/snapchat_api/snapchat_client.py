import requests
from dotenv import load_dotenv
import os
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

class SnapchatClient:
    def __init__(self, chatbot):
        load_dotenv()
        self.chatbot = chatbot
        self.username = os.getenv('SNAPCHAT_USERNAME')
        self.password = os.getenv('SNAPCHAT_PASSWORD')
        self.admin_username = os.getenv('SNAPCHAT_ADMIN_USERNAME')
        self.driver = None
        self.connected = False
        self.last_message_timestamps = {}
        self.processed_messages = set()
        self.startup_message = "Bot is online and ready! 🤖"
        self.cooldown_period = 2  # seconds between responses
        self.last_response_time = 0
        self.rate_limit_delay = 10  # seconds between API calls
        self.last_api_call = 0

    def connect(self):
        """Connect to Snapchat using Selenium (two-step login, handles cookie popups)"""
        try:
            # Set up Chrome options
            chrome_options = Options()
            chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
            chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(10)

            # Go to the new Snapchat login page
            self.driver.get('https://accounts.snapchat.com/accounts/v2/login')
            print("Navigating to Snapchat login page...")

            try:
                # Handle cookie consent popups if present
                time.sleep(2)
                cookie_selectors = [
                    "//button[contains(text(), 'Accept')]",
                    "//button[contains(text(), 'accept')]",
                    "//button[contains(text(), 'Agree')]",
                    "//button[contains(text(), 'agree')]",
                    "//button[contains(text(), 'OK')]",
                    "//button[contains(text(), 'ok')]",
                    "//button[contains(text(), 'Got it')]",
                    "//button[contains(@id, 'cookie')]",
                    "//button[contains(@class, 'cookie')]",
                    "//button[@mode='primary']"
                ]
                for selector in cookie_selectors:
                    try:
                        cookie_btn = self.driver.find_element(By.XPATH, selector)
                        if cookie_btn.is_displayed() and cookie_btn.is_enabled():
                            print("Cookie consent found, clicking...")
                            cookie_btn.click()
                            time.sleep(1)
                            break
                    except Exception:
                        continue

                # Step 1: Enter username/email
                username_field = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@name='accountIdentifier']"))
                )
                username_field.clear()
                username_field.send_keys(self.username)
                print("Entered username/email")

                next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[.='Next']"))
                )
                next_button.click()
                print("Clicked Next after username/email")

                # Step 2: Enter password
                password_field = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
                )
                password_field.clear()
                password_field.send_keys(self.password)
                print("Entered password")

                next_button_pw = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[.='Next']"))
                )
                next_button_pw.click()
                print("Clicked Next after password")

                # Wait for successful login (look for some post-login element or redirect)
                WebDriverWait(self.driver, 20).until(
                    EC.url_contains("accounts.snapchat.com/accounts/sessions")
                )
                print("Successfully logged in to Snapchat!")

                self.connected = True
                return True

            except TimeoutException as e:
                print(f"Timeout while waiting for elements: {str(e)}")
                try:
                    self.driver.save_screenshot("snapchat_login_error.png")
                    print("Saved error screenshot to snapchat_login_error.png")
                except:
                    pass
                return False
            except NoSuchElementException as e:
                print(f"Element not found: {str(e)}")
                try:
                    self.driver.save_screenshot("snapchat_login_error.png")
                    print("Saved error screenshot to snapchat_login_error.png")
                except:
                    pass
                return False
        except Exception as e:
            print(f"Error during Snapchat login: {str(e)}")
            if self.driver:
                self.driver.quit()
            return False

    def is_valid_message(self, message):
        """Check if a message should be processed"""
        # Don't process our own messages
        if message.get('sender') == self.username:
            return False
            
        # Don't process error messages
        if message.get('text') in ["Sorry, ich komm grad nicht zum Antworten.", "Bot is online and ready! 🤖"]:
            return False
            
        # Check cooldown period
        current_time = time.time()
        if current_time - self.last_response_time < self.cooldown_period:
            return False
            
        # Check if message is new
        thread_id = message.get('thread_id')
        timestamp = message.get('timestamp')
        
        if not thread_id or not timestamp:
            return False
            
        last_timestamp = self.last_message_timestamps.get(thread_id, 0)
        if timestamp <= last_timestamp:
            return False
            
        return True

    def get_messages(self):
        """Get new messages from Snapchat"""
        if not self.connected or not self.driver:
            return []
            
        try:
            # Wait for chat list to be present
            chat_list = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'chat-list')]"))
            )
            
            # Get all chat items
            chat_items = chat_list.find_elements(By.XPATH, ".//div[contains(@class, 'chat-item')]")
            messages = []
            
            for chat in chat_items:
                try:
                    # Get thread ID and last message
                    thread_id = chat.get_attribute('data-thread-id')
                    last_message = chat.find_element(By.XPATH, ".//div[contains(@class, 'last-message')]")
                    
                    message = {
                        'thread_id': thread_id,
                        'text': last_message.text,
                        'timestamp': time.time(),
                        'sender': 'user'  # We'll need to determine the actual sender
                    }
                    
                    if self.is_valid_message(message):
                        messages.append(message)
                        
                except NoSuchElementException:
                    continue
                    
            return messages
            
        except Exception as e:
            print(f"Error getting messages: {str(e)}")
            return []

    def send_message(self, thread_id, text):
        """Send a message to a Snapchat thread"""
        if not self.connected or not self.driver:
            return False
            
        try:
            # Find the chat input field
            input_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'chat-input')]//textarea"))
            )
            
            # Clear and send message
            input_field.clear()
            input_field.send_keys(text)
            
            # Find and click send button
            send_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'send-button')]")
            send_button.click()
            
            # Update last response time
            self.last_response_time = time.time()
            return True
            
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            return False

    def handle_api_error(self, error, max_retries=3):
        """Handle API errors with exponential backoff"""
        retry_count = 0
        while retry_count < max_retries:
            wait_time = (2 ** retry_count) * self.rate_limit_delay
            print(f"API error: {str(error)}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            retry_count += 1
        return False

    def listen_for_messages(self):
        """Listen for new messages and respond"""
        if not self.connected:
            print("Not connected to Snapchat")
            return
            
        while self.connected:
            try:
                # Rate limiting
                current_time = time.time()
                if current_time - self.last_api_call < self.rate_limit_delay:
                    time.sleep(self.rate_limit_delay)
                self.last_api_call = current_time
                
                # Get and process messages
                messages = self.get_messages()
                for message in messages:
                    try:
                        # Get AI response
                        response = self.chatbot.get_response(message['text'])
                        
                        # Send response
                        if response and self.send_message(message['thread_id'], response):
                            # Update last message timestamp
                            self.last_message_timestamps[message['thread_id']] = message['timestamp']
                            
                    except Exception as e:
                        print(f"Error processing message: {str(e)}")
                        self.handle_api_error(e)
                        
            except Exception as e:
                print(f"Error in message loop: {str(e)}")
                self.handle_api_error(e)
                
            time.sleep(1)  # Small delay between checks

    def disconnect(self):
        """Disconnect from Snapchat"""
        if self.driver:
            self.driver.quit()
        self.connected = False 
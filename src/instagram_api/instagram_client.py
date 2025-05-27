from instagrapi import Client
from dotenv import load_dotenv
import os
import time
import json
import datetime
from typing import Set, Dict, Optional
from .proxy_manager import ProxyManager
from .proxy_scraper import ProxyScraper

class InstagramClient:
    def __init__(self, gemini_client):
        load_dotenv()
        self.username = os.getenv('INSTAGRAM_USERNAME')
        self.password = os.getenv('INSTAGRAM_PASSWORD')
        self.client = Client()
        self.is_connected = False
        self.admin_username = "im3vn"
        self.sent_message_ids: Set[str] = set()
        self.processed_message_ids: Set[str] = set()
        self.session_file = "ig_session.json"
        self.startup_message = "Bot is online and ready! 🤖"
        self.error_messages = {
            "Sorry, ich komm grad nicht zum Antworten.",
            "Failed to send message",
            "Error generating response"
        }
        self.last_response_time = datetime.datetime.now()
        self.last_check_time = datetime.datetime.now()
        self.rate_limit_delay = 10
        self.max_retries = 3
        self.retry_delay = 30
        self.gemini_client = gemini_client
        
        # Initialize proxy management
        self.proxy_scraper = ProxyScraper()
        self.proxy_manager = ProxyManager()
        
        print("[Instagram] Initializing Instagram client...")

    def connect(self):
        """Connect to Instagram, using session if available"""
        try:
            print("[Instagram] Attempting to connect...")
            
            # Start proxy scraper in background
            self.proxy_scraper.start_periodic_update(interval=1800)
            print("[Instagram] Proxy scraper started in background")
            
            if os.path.exists(self.session_file):
                print("[Instagram] Loading existing session...")
                self.client.load_settings(self.session_file)
                self.client.login(self.username, self.password)
            else:
                print("[Instagram] Creating new session...")
                self.client.login(self.username, self.password)
                self.client.dump_settings(self.session_file)
            
            self.is_connected = True
            admin_id = self.client.user_id_from_username(self.admin_username)
            sent_ids = self.client.direct_send(self.startup_message, [admin_id])
            self.sent_message_ids.update(sent_ids)
            print("[Instagram] Connected and ready!")

            # Set up proxy
            proxy = self.proxy_manager.get_next_proxy()
            if proxy:
                self.client.set_proxy(proxy)
                print(f"[Instagram] Using proxy: {proxy}")
            else:
                print("[Instagram] No proxies available, continuing without proxy")

            return True
        except Exception as e:
            print(f"[Instagram] Login failed: {e}")
            return False

    def is_error_message(self, text: str) -> bool:
        """Check if a message is an error message"""
        return any(error in text for error in self.error_messages)

    def is_bot_message(self, message) -> bool:
        """Check if a message is from the bot"""
        return message.user_id == self.client.user_id

    def is_processed_message(self, message) -> bool:
        """Check if a message has been processed"""
        return hasattr(message, 'id') and message.id in self.processed_message_ids

    def is_valid_message(self, message, thread_id: str) -> bool:
        """Check if a message should be processed"""
        # Basic message validation
        if not hasattr(message, 'text') or not message.text:
            return False
            
        # Skip bot's own messages
        if self.is_bot_message(message):
            return False
            
        # Skip already processed messages
        if self.is_processed_message(message):
            return False
            
        # Skip error messages
        if self.is_error_message(message.text):
            return False
            
        # Skip the startup message
        if message.text == self.startup_message:
            return False
            
        # Prevent rapid-fire responses
        time_since_last_response = (datetime.datetime.now() - self.last_response_time).total_seconds()
        if time_since_last_response < 2:
            return False
            
        return True

    def handle_api_error(self, error, retry_count):
        """Handle API errors with exponential backoff"""
        if "500" in str(error) or "Max retries exceeded" in str(error):
            wait_time = self.retry_delay * (2 ** retry_count)  # exponential backoff
            print(f"Instagram API error (attempt {retry_count + 1}/{self.max_retries}). Waiting {wait_time} seconds...")
            time.sleep(wait_time)
            return True
        return False

    def listen_for_messages(self, callback):
        """Listen for new direct messages and handle them"""
        if not self.is_connected:
            print("[Instagram] Not connected, cannot listen for messages")
            return

        print("[Instagram] Starting message listener...")
        retry_count = 0

        while True:
            try:
                # Rate limiting
                time_since_last_check = (datetime.datetime.now() - self.last_check_time).total_seconds()
                if time_since_last_check < self.rate_limit_delay:
                    time.sleep(self.rate_limit_delay - time_since_last_check)

                self.last_check_time = datetime.datetime.now()
                threads = self.client.direct_threads(selected_filter="unread")
                print(f"[Instagram] Found {len(threads)} unread threads")
                
                # Reset retry count on successful API call
                retry_count = 0
                
                for thread in threads:
                    thread_id = thread.id
                    messages = self.client.direct_messages(thread_id)
                    print(f"[Instagram] Thread {thread_id}: Processing {len(messages)} messages")
                    
                    if not messages:
                        continue

                    # Process only the most recent message
                    latest_message = messages[0]
                    print(f"[Instagram] Processing message: {latest_message.text[:50]}...")
                    
                    if not self.is_valid_message(latest_message, thread_id):
                        print(f"[Instagram] Skipping invalid message: {latest_message.text[:50]}...")
                        continue

                    print(f"[Instagram] Received valid message: {latest_message.text}")
                    response = callback(latest_message.text)
                    
                    if response and not self.is_error_message(response):
                        print(f"[Instagram] Sending response: {response[:50]}...")
                        sent_ids = self.send_message(thread_id, response)
                        if sent_ids:
                            self.sent_message_ids.update(sent_ids)
                            self.last_response_time = datetime.datetime.now()
                            print(f"[Instagram] Message sent successfully to thread {thread_id}")
                        else:
                            print(f"[Instagram] Failed to send message to thread {thread_id}")
                    else:
                        print("[Instagram] No valid response generated")
                    
                    # Mark message as processed
                    if hasattr(latest_message, 'id'):
                        self.processed_message_ids.add(latest_message.id)
                        print(f"[Instagram] Marked message {latest_message.id} as processed")

                # Clean up old message IDs
                if len(self.processed_message_ids) > 1000:
                    self.processed_message_ids = set(list(self.processed_message_ids)[-1000:])
                if len(self.sent_message_ids) > 1000:
                    self.sent_message_ids = set(list(self.sent_message_ids)[-1000:])

            except Exception as e:
                print(f"[Instagram] Error in message loop: {e}")
                
                if retry_count < self.max_retries and self.handle_api_error(e, retry_count):
                    retry_count += 1
                    continue
                
                if retry_count >= self.max_retries:
                    print("[Instagram] Max retries reached. Waiting 5 minutes...")
                    time.sleep(300)
                    retry_count = 0
                else:
                    time.sleep(5)

    def send_message(self, thread_id: str, message: str) -> Optional[list]:
        """Send a message to a specific thread and return the message ID(s)"""
        try:
            sent_ids = self.client.direct_answer(thread_id, message)
            return sent_ids
        except Exception as e:
            print(f"Failed to send message: {e}")
            return None
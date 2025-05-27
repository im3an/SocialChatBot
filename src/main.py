import os
import sys
import time
from dotenv import load_dotenv
from chatbot.gemini_client import GeminiClient
from instagram_api.instagram_client import InstagramClient
from snapchat_api.snapchat_client import SnapchatClient

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("\n" + "="*50)
    print("🤖 Multi-Platform Chatbot 🤖".center(50))
    print("="*50 + "\n")

def print_menu():
    print("\nAvailable Options:")
    print("1. Instagram only")
    print("2. Snapchat only")
    print("3. Both platforms")
    print("4. Exit")
    print("\n" + "-"*50)

def initialize_platforms(choice, gemini_client):
    platforms = []
    
    if choice in [1, 3]:  # Instagram
        print("\n[System] Initializing Instagram...")
        instagram_client = InstagramClient(gemini_client)
        if instagram_client.connect():
            print("[System] Instagram connected successfully!")
            platforms.append(("instagram", instagram_client))
        else:
            print("[System] Failed to connect to Instagram!")
    
    if choice in [2, 3]:  # Snapchat
        print("\n[System] Initializing Snapchat...")
        snapchat_client = SnapchatClient(gemini_client)
        if snapchat_client.connect():
            print("[System] Snapchat connected successfully!")
            platforms.append(("snapchat", snapchat_client))
        else:
            print("[System] Failed to connect to Snapchat!")
    
    return platforms

def main():
    try:
        clear_screen()
        print_header()
        
        # Initialize Gemini client
        print("[System] Initializing Gemini client...")
        gemini_client = GeminiClient()
        print("[System] Gemini client initialized successfully!")
        
        while True:
            print_menu()
            try:
                choice = int(input("Enter your choice (1-4): "))
                if choice == 4:
                    print("\n[System] Shutting down...")
                    sys.exit(0)
                
                if choice not in [1, 2, 3]:
                    print("\n[Error] Invalid choice! Please enter a number between 1 and 4.")
                    continue
                
                platforms = initialize_platforms(choice, gemini_client)
                
                if not platforms:
                    print("\n[Error] No platforms were successfully initialized!")
                    continue
                
                print("\n[System] Starting message listeners...")
                for platform_name, client in platforms:
                    print(f"[System] Starting {platform_name} listener...")
                    client.listen_for_messages(gemini_client.generate_response)
                
            except ValueError:
                print("\n[Error] Please enter a valid number!")
            except KeyboardInterrupt:
                print("\n[System] Shutdown requested...")
                sys.exit(0)
            except Exception as e:
                print(f"\n[Error] An unexpected error occurred: {e}")
                time.sleep(2)
    
    except Exception as e:
        print(f"\n[Fatal Error] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
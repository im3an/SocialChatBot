from src.chatbot.chatbot import Chatbot
import sys
import os

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def chat_interface():
    clear_screen()
    bot = Chatbot()
    
    # Print welcome message
    print("\n=== Chat with Riley ===")
    print("(Type 'quit' to exit)")
    print("------------------------\n")
    
    # Show initial greeting
    greeting = bot.greet_user()
    print(f"Riley: {greeting}\n")
    
    # Main chat loop
    while True:
        # Get user input
        user_message = input("You: ").strip()
        
        # Check for quit command
        if user_message.lower() in ['quit', 'exit']:
            print("\nEnding chat session...")
            break
            
        # Get bot response
        response = bot.respond_to_message(user_message)
        print(f"\nRiley: {response}\n")

if __name__ == "__main__":
    try:
        chat_interface()
    except KeyboardInterrupt:
        print("\n\nChat session ended by user.")
        sys.exit(0)
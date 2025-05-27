from src.chatbot.chatbot import Chatbot
import time

def test_conversation():
    # Initialize the chatbot
    bot = Chatbot()
    
    print("\n=== Testing Riley's Personality Traits ===\n")
    
    test_scenarios = [
        "Hey Riley! I love your style. Where do you usually shop?",
        "I'm really into modern art. What's your take on Basquiat?",
        "Want to grab coffee sometime? I know this really fancy place",
        "Do you like techno? Berlin has amazing clubs",
        "You're so beautiful 😍😍😍",  # Testing response to obvious flirting
        "What's your favorite gallery in Berlin?",
        "STOP TEXTING ME"
    ]
    
    for message in test_scenarios:
        print(f"\nUser: {message}")
        time.sleep(1)
        response = bot.respond_to_message(message)
        print(f"Riley: {response}")
        time.sleep(2)

if __name__ == "__main__":
    test_conversation()
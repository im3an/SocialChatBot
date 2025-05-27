# 🤖 Riley: The Instagram & Snapchat Chatbot

Welcome to **Riley**, your multi-platform, personality-driven chatbot for Instagram and Snapchat. Riley isn’t just another bot—she’s a fictional 22-year-old art history student in Berlin, with a sharp wit, a unique style, and a memory for your conversations. She’s designed to make every chat feel real, engaging, and just a little bit mysterious.


## 🚀 Features

- **Multi-Platform:** Seamlessly connects to both Instagram and Snapchat.
- **Personality Engine:** Riley’s responses are shaped by a detailed, editable [personality profile](data/personality.txt).
- **Conversational Memory:** Remembers past chats and references them for continuity.
- **Modern Slang:** Uses Gen-Z slang naturally (but sparingly) for authenticity.
- **AI-Powered:** Leverages Google Gemini for intelligent, context-aware replies.
- **Proxy Support:** Robust proxy management for reliable Instagram connectivity.
- **Safety First:** Strict controls to prevent inappropriate or unsafe interactions.


## 🗂️ Project Structure

```
instagram-chatbot/
├── src/
│   ├── main.py                  # Main entry point (CLI)
│   ├── chatbot/
│   │   ├── chatbot.py           # Riley's core logic
│   │   ├── gemini_client.py     # Gemini API integration
│   │   ├── nlp_model.py         # (Optional) Local NLP model
│   │   └── personality.py       # Personality trait loader
│   ├── instagram_api/
│   │   ├── instagram_client.py  # Instagram automation
│   │   ├── proxy_manager.py     # Proxy rotation
│   │   └── proxy_scraper.py     # Proxy scraping
│   └── snapchat_api/
│       └── snapchat_client.py   # Snapchat automation
├── data/
│   └── personality.txt          # Riley's personality definition
├── tests/
│   └── test_local.py            # Local chatbot tests
├── .env.example                 # Example environment config
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```


## 🛠️ Setup & Installation

1. **Clone the repository**
   ```sh
   git clone <repository-url>
   cd instagram-chatbot
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   - Copy `.env.example` to `.env` and fill in your credentials:
     - Instagram & Snapchat usernames/passwords
     - Gemini API key
     - Path to `personality.txt` (default: `data/personality.txt`)

4. **(Optional) Edit Riley’s personality**
   - Tweak [data/personality.txt](data/personality.txt) to change Riley’s style, memory, or slang.


## 💬 Usage

### Start the Chatbot

```sh
python src/main.py
```

- **Choose your platform:** Instagram, Snapchat, or both.
- **Interact:** Riley will respond to DMs on the selected platforms, using her unique personality.

### Local Testing

For local, terminal-based chat with Riley:

```sh
python chat_local.py
```

## ✨ Customization

- **Personality:** Edit [data/personality.txt](data/personality.txt) to shape Riley’s character, memory, and slang.
- **Slang & Style:** Add or remove slang terms, tweak her background, or adjust her communication style.
- **Safety:** Riley will never initiate conversations or respond after receiving "STOP TEXTING ME".

## 🧪 Testing

Run the included test script to simulate conversations and verify Riley’s responses:

```sh
python -m tests.test_local
```

## 🛡️ Safety & Ethics

- Riley will **never** engage in illegal, unethical, or harmful conversations.
- All responses are filtered for safety and appropriateness.

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

## 🙏 Credits

- [Google Gemini](https://ai.google.dev/) for AI-powered conversations
- [instagrapi](https://github.com/adw0rd/instagrapi) for Instagram automation
- [Selenium](https://www.selenium.dev/) for Snapchat automation

> _“Riley is more than code—she’s a vibe.”_
# README.md

# Instagram Chatbot

This project is an Instagram chatbot that connects to Instagram and interacts with users. The chatbot is designed to have a personality defined by the contents of `data/personality.txt`, allowing for engaging and personalized conversations.

## Project Structure

```
instagram-chatbot
├── src
│   ├── main.py                # Entry point of the application
│   ├── chatbot
│   │   ├── __init__.py        # Marks the chatbot directory as a package
│   │   ├── chatbot.py          # Contains the Chatbot class for user interaction
│   │   ├── nlp_model.py        # Functions for natural language processing tasks
│   │   └── personality.py      # Defines the Personality class for chatbot traits
│   └── instagram_api
│       ├── __init__.py        # Marks the instagram_api directory as a package
│       └── instagram_client.py  # Handles connection to the Instagram API
├── data
│   └── personality.txt         # Contains personality traits for the chatbot
├── requirements.txt            # Lists project dependencies
├── .env                        # Contains environment variables
└── README.md                   # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd instagram-chatbot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables in the `.env` file. Make sure to include your Instagram API keys and any other necessary configuration settings.

4. Run the application:
   ```
   python src/main.py
   ```

## Usage Guidelines

- The chatbot will initiate a conversation upon running the application.
- You can customize the chatbot's personality by editing the `data/personality.txt` file.
- Ensure that your Instagram account is properly configured to allow API interactions.

## License

This project is licensed under the MIT License.
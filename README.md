# Telegram AI Chatbot

This is an AI-powered Telegram chatbot designed to handle various user interactions, including registration, Gemini-powered chat, image/file analysis, and web search. All user data is stored in a **MongoDB** database. The project also features optional sentiment analysis, referral systems, and dashboards for enhanced functionality.

## Features
- **User Registration**: Users can register with the chatbot for personalized interactions.
- **Gemini-Powered Chat**: The chatbot leverages Gemini Flash for engaging conversations.
- **Image/File Analysis**: Upload images or files for analysis and get real-time feedback.
- **Web Search**: Perform web searches directly from the chatbot.
- **Data Storage**: All user data is stored in MongoDB for easy access and management.
- **(Optional) Sentiment Analysis**: Analyzes user sentiment to adjust chatbot responses.

## Getting Started

### Prerequisites

- **Python 3.x**
- **MongoDB** (You can use MongoDB Atlas for a cloud solution or set up MongoDB locally)
- **Telegram Bot API Token** (To create a bot, follow [this guide](https://core.telegram.org/bots#botfather))
- **Gemini Flash** (For image processing)

### Installation

1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd <repo_name>
## Install the required Python packages:

**pip install -r requirements.txt**
## Set up your MongoDB and update the config.py file with your MongoDB URI.

Add your Telegram Bot API Token to config.py:


**TELEGRAM_API_TOKEN = '<your_bot_token>'**
(Optional) If you're using Gemini Flash for image processing, ensure it's properly installed and configured.

Usage
Start the chatbot by running:


## python bot.py
Interact with the bot on Telegram. Type /start to begin registration.

## Contributing
Feel free to fork the repository and submit pull requests for improvements, bug fixes, or new features.

## License
This project is licensed under the MIT License - see the LICENSE file for details.


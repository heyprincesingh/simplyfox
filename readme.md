# Slack Summary Project

This Django project provides a system to summarize Slack conversations, including important mentions and topic summaries. The project leverages LangChain and various utility functions to generate summaries from Slack data.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Utilities](#utilities)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.11
- Django
- Slack API Token
- Google Generative AI API Key

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/slack-summary.git
    cd slack-summary
    ```

2. Create a virtual environment and activate it:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the `.env` file with your credentials:

    ```ini
    SLACK_API_TOKEN=your-slack-api-token
    GOOGLE_API_KEY=your-google-api-key
    ```

5. Apply migrations and run the server:

    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

## Configuration

### Slack API Token

Get your Slack API token from the [Slack API website](https://api.slack.com).

### Google Generative AI API Key

Get your Google Generative AI API Key from the [Google Cloud Console](https://console.cloud.google.com/).

## Usage

### Fetch Slack Conversations

The function `get_channel_conversation` in `slack_utils/slack_get_functions.py` retrieves the conversation history for a specified channel between start and end dates.

### Generate Summaries

The main function for generating summaries is `langchain_generate_summary` in `utils/llm_model/langchain_main.py`. This function processes the conversation data to provide important mentions and topic summaries.

### Example Code

Here is an example of how to use the main functions:

```python
from slack_channel_summary.slack_utils.slack_get_functions import get_channel_conversation
from slack_channel_summary.utils.llm_model.langchain_main import langchain_generate_summary

# Fetch conversation data
client = YourSlackClient(slack_api_token)
conversation_data = get_channel_conversation(client, 'channel_id', start_date, end_date)

# Generate summary
user_id = 'U1234567890'
token_counts = 5000
summary = langchain_generate_summary(user_id, conversation_data, token_counts)
print(summary)

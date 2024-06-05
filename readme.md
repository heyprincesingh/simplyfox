# Slack AI Summary Project

This Django project provides a system to summarize Slack conversations, including important mentions and topic summaries. The project leverages LangChain and various utility functions to generate summaries from Slack data.

## Tech Stacks:
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![Python](https://img.shields.io/badge/python-%2307405e.svg?style=for-the-badge&logo=python&logoColor=white&color=blue) ![Slack](https://img.shields.io/badge/slack-%23092E20.svg?style=for-the-badge&logo=slack&logoColor=white&color=purple) ![Docker](https://img.shields.io/badge/docker-%238511FA.svg?style=for-the-badge&logo=docker&logoColor=white&color=darkblue)

## Table of Contents

- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Steps](#steps)
- [Configuration](#configuration)
  - [Slack API Token](#slack-api-token)
  - [Google Generative AI API Key](#google-generative-ai-api-key)
  - [Claude AI API Key](#claude-ai-api-key)
- [Project Structure](#project-structure)
- [Slack App Setup Guide](#slack-app-setup-guide)
  - [Step 1: Set Up a Slack App](#step-1-set-up-a-slack-app)
  - [Step 2: Add Manifest File Data](#step-2-add-manifest-file-data)
  - [Step 3: Install the App](#step-3-install-the-app)
- [Slack App Manifest Update Guide](#slack-app-manifest-update-guide)
  - [Update Slack App Manifest](#update-slack-app-manifest)
  - [Additional steps and Resources](#additional-steps-and-resources)

## Installation

### Prerequisites

- Python 3.11
- Django
- Slack API Token
- Google Generative AI or Claude AI API Key

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/HappyFox-Labs/slack-ai.git
    cd slack-ai
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
    SLACK_BOT_TOKEN=your-slack-api-token
    GEMINI_AI_API_KEY=your-gemini-api-key
    CLAUDE_AI_API_KEY=your-claude-api-key
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

### Claude AI API Key

Get your Claude AI API Key from the [Claude API\Anthropic](https://www.anthropic.com/api).

## Project Structure

```bash
├── slack-ai/
│
├── slack_channel_summary/
│   ├── actions/            # Action classes
│   ├── middleware/         # Middleware for api authentication 
│   ├── slack_utils/        # Slack utilities for slack actions
│   ├── utils/              # General funtions
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── shared_data.py      # Store the user's conversation data in session
│   ├── urls.py
│   └── views.py
│   
├── .env
├── .gitignore
├── manage.py
└── requirements.py
```

## Slack App Setup Guide

This guide will walk you through the process of setting up a Slack app, adding the manifest file data, and installing the app onto your workspace.

### Step 1: Set Up a Slack App

1. Visit the [Slack App Quickstart Guide](https://api.slack.com/quickstart) to create a new Slack app.
2. Follow the instructions to set up your app, including naming your app and selecting the workspace for installation.

### Step 2: Add Manifest File Data

1. Go to the "App Manifest" section in the Slack API console.
2. Copy the content of app_manifest.yaml (provided separately in the repository) and paste it into the manifest editor.

### Step 3: Install the App

1. Navigate to the "Install App" section in the Slack API console.
2. Click "Install App to Workspace" and follow the prompts to authorize the app.

Congratulations! Your Slack app should now be installed and ready to use.

## Slack App Manifest Update Guide
This guide will walk you through replacing the URL in your Slack app manifest with your server URL.

### Update Slack App Manifest

Get your server URL, and follow these steps to update the URL in your Slack app manifest:

1. **Access Slack App Manifest**: Go to the "App Manifest" section in the Slack API console for your app.

2. **Update URL Field**: In the manifest editor, find the field related to the URL of your app. This could be the `redirect_urls` field.

3. **Replace URL**: Replace the existing URLs with your server URL that you had.

4. **Save Changes**: After updating the URL, save the changes to the manifest.

### Additional steps and Resources

Remember to restart your Django server after updating the server URL to ensure that it's using the new URL for any necessary callbacks or requests.

For more detailed instructions and additional features, refer to the [Slack API Documentation](https://api.slack).


## API Endpoints

The application provides the following endpoints:

`/slack_summary`
- **Method:** POST
- **Description:** Handles Slack slash commands.
- **View:** `SlackSummaryView`
- **Handler:** `SlackSlashActions`

`/eventsubs`
- **Method:** POST
- **Description:** Handles Slack events.
- **View:** `SlackEventsView`
- **Handler:** `SlackEventsHandler`

`/userinteraction`
- **Method:** POST
- **Description:** Handles user interactions within Slack.
- **View:** `SlackUserInteractionView`
- **Handler:** `SlackInteractionHandler`

## Views

### SlackSummaryView
- **Description:** Handles incoming Slack slash commands and processes them using `SlackSlashActions`.

### SlackUserInteractionView
- **Description:** Handles user interactions (e.g., button clicks, dialog submissions) in Slack and processes them using `SlackInteractionHandler`.

### SlackEventsView
- **Description:** Handles Slack events (e.g., message events, reaction events) and processes them using `SlackEventsHandler`.
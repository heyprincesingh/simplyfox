import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai_token = os.getenv("GEMINI_AI_API_TOKEN")


def generate_ai_summary(conversationData):
    genai.configure(api_key=genai_token)
    generation_config = {
        "temperature": 0.0,
        "top_p": 1,
        "top_k": 0,
        "max_output_tokens": 1000,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_ONLY_HIGH",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_ONLY_HIGH",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_ONLY_HIGH",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_ONLY_HIGH",
        },
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.0-pro",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )

    convo = model.start_chat(history=[])

    convo.send_message(
        f"""You are tasked with summarizing the conversation data from a Slack channel. The channel contains discussions on various topics, and your goal is to create titles and summaries for each topic based on potential use cases.
          Title Generation:
          Based on the conversation data, identify potential use cases that align with the discussions in the channel. Each identified use case should serve as a title for a summarized topic within the channel.
          If the conversation spans multiple days, mention the dates along with the summarization. Use a single * at the beginning and end to bold a keyword.

          Summarization:
          For each identified use case:
          Each topic to summarize strictly under 80 words.
          Analyze the conversation data to extract key points and highlights relevant to the specific use case.
          Generate a concise summary paragraph that captures the essence of the discussions related to the use case.
          Ensure that the summary provides enough context for readers to understand the main topics and discussions covered in the channel.
          If multiple topics or subtopics are discussed within the use case, organize the summary paragraph accordingly to maintain clarity and coherence.

          Keyword topics Extraction:
          After summarizing, provide a list of key-topics extracted from the conversation data that represent the main themes and topics discussed within the channel at the end only. This will help readers quickly identify the key points covered. The conversation data={conversationData}
          """
    )

    # convo.send_message(
    #     f"Summarize my conversation here given below. I'd like it to be in a human-like paragraph format, mentioning who said what. Also Give the important topics/headlines as bullet points. The conversation data={conversationData}. Here in the conversation data, 'me' as a user is defined for the user asking the query, replace it with 'you'",
    # )

    return (
        convo.last.text.replace("**", "*")
        .replace("\n*", "\n *")
        .replace("*\n", "* \n")
        .strip()
        if convo.last
        else ""
    )


def generate_ai_query_answer(conversationData, user_query):
    genai.configure(api_key=genai_token)
    generation_config = {
        "temperature": 0.0,
        "top_p": 1,
        "top_k": 0,
        "max_output_tokens": 400,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.0-pro",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )

    convo = model.start_chat(history=[])

    convo.send_message(
        f"""Go through the conversation data {conversationData} closely and give the final answer for the question: {user_query}.
        1. keep the answer strictly under 50 word counts. 
        2. Answer should only be from the conversation data given above.
        3. Here in the conversation data, 'me' as a user is defined for the user asking the query, replace it with 'you'"""
    )

    return (
        convo.last.text.replace("**", "*")
        .replace("\n*", "\n *")
        .replace("*\n", "* \n")
        .strip()
        if convo.last.text
        else ""
    )

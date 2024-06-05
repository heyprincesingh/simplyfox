from slack_summary.slack_utils.slack_blocks_data_functions import (
    replace_heading_lines,
    space_around_newline,
)
from slack_summary.utils.llm_model.llm_langchain_instance import get_llm_instance
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from datetime import datetime


def langchain_generate_summary(user_id, conversation_data, token_counts):
    current_datetime = datetime.now()
    summary_data_format = """
    **Important Mentions**
    • ddmmyyyy hh:mm, @sender1 said: message1
    • ddmmyyyy hh:mm, @sender2 said: message2

    **Important Topics**
    • Topic 1
    • Topic 2
    • Topic 3

    **Summary**
    • Topic 1
    ➥ Summary under 50 words

    • Topic 2
    ➥ Summary under 50 words

    • Topic 3
    ➥ Summary under 50 words
    """


    DATA_SEPARATION_TEMPLATE_TEXT = """
    From the conversation data, return just a dictionary which will hold the topic name as key and all the conversations related to the topic and all its metadata from the conversation data.

    {conversation_data}
    """

    SUMMARIZATION_TEMPLATE_TEXT = """
    Current date time: {current_datetime},
    The result should follow this format: {summary_data_format},
    In the conversation data, {user_id} refers to my user id mentioned by other users.
    Create three sections: 
    section 1: Extract the only most important messages where {user_id} is mentioned.
        The Strict rules to follow are:
        a. Provide who mentioned the user and what they said.
        b. Strictly Summarize any mentioned message under 20 words that is more than 50 words.
        c. The timestamp should be in 'dd mmm yy hh:mm am/pm' format with 12 hours.
        d. Remove all greetings like 'hey' or 'hello'.
    section 2: Give a bulleted list of the top 5 most important topics from the conversation.
    section 3: From the given topic wise separated conversation data, Extract a maximum of 10 most important topics.
        The Strict rules to follow are:
        a. Which will be sorted in priority of the topic by keeping the most important discussion topic on the top.
        b. For each topic extracted, provide a summarized context in 50 words. 
        c. User is the one who sent text message and replace any instances of 'me' with 'you' in the results.
        d. My messages are set as 'me'. Don't include my conversation's summary context in the result.
        d. The summarized context should be in past continuous tense.
    
    {categorized_conversation_data}
    """
 
    llm = get_llm_instance(token_counts=token_counts)

    data_separation_template = PromptTemplate(
        input_variables=["conversation_data"], template=DATA_SEPARATION_TEMPLATE_TEXT
    )

    summarization_template = PromptTemplate(
        input_variables=[
            "current_datetime",
            "summary_data_format",
            "user_id",
            "categorized_conversation_data",
        ],
        template=SUMMARIZATION_TEMPLATE_TEXT,
    )

    data_separation_chain = LLMChain(llm=llm, prompt=data_separation_template)

    categorized_conversation_data = data_separation_chain.run(
        {"conversation_data": conversation_data}
    )

    summarization_chain = LLMChain(llm=llm, prompt=summarization_template)

    combined_input = {
        "current_datetime": current_datetime,
        "summary_data_format": summary_data_format,
        "user_id": user_id,
        "categorized_conversation_data": categorized_conversation_data,
    }

    result = summarization_chain.run(combined_input)

    return (
        space_around_newline(replace_heading_lines(result))
        .replace("* ", "• ")
        .replace("- ", "• ")
        .replace("**", "*")
        .replace("\n*", "\n\n *")
        .replace("*\n", "* \n")
        .replace("```", "")
        .strip()
    )


def langchain_generate_query_answer(
    user_id, conversation_data, user_query, token_counts
):
    SUMMARIZATION_TEMPLATE_TEXT = """
    You are given the following conversation data and a user query. Please provide a concise answer to the user query based solely on the provided conversation data. 
    Your answer should be:
    1. Strictly under 50 words.
    2. Derived only from the conversation data.
    3. In the conversation data, 'me' refers to the user asking the query. Replace it with 'you' in your response.
    4. In the conversation data, {user_id} refers to my user_id mentioned by other users and return who sent the message mentioning me and the message too.
    Conversation Data:
    {conversation_data}
    
    User Query:
    {user_query}
    
    Answer:
    """

    llm = get_llm_instance(token_counts=token_counts)

    summarization_template = PromptTemplate(
        input_variables=["user_id", "conversation_data", "user_query"],
        template=SUMMARIZATION_TEMPLATE_TEXT,
    )

    summarization_chain = summarization_template | llm

    combined_input = {
        "user_id": user_id,
        "conversation_data": conversation_data,
        "user_query": user_query,
    }

    result = summarization_chain.invoke(combined_input)

    cleaned_data = (
        space_around_newline(replace_heading_lines(result))
        .replace("- ", "• ")
        .replace("**", "*")
        .replace("\n*", "\n\n *")
        .replace("*\n", "* \n")
        .replace("```", "")
        .strip()
    )

    return f"*Ques: {user_query}*\n*Ans:* {cleaned_data}"
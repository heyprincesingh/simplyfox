from langchain_google_genai import GoogleGenerativeAI
# from langchain.llms.bedrock import Bedrock
# from langchain.llms.openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
def get_llm_instance(token_counts):
    llm_model = os.getenv("LLM_MODEL")

    if llm_model == "GEMINI_AI":
        return GoogleGenerativeAI(
            model=os.getenv("GEMINI_AI_MODEL"),
            max_output_tokens=token_counts,
            google_api_key=os.environ["GEMINI_AI_API_KEY"],
        )
        
    # elif llm_model == "GPT_AI":
    #     return OpenAI(max_tokens=token_counts)
    
    # elif llm_model == "BEDROCK_AI":
    #     return Bedrock(
    #         credentials_profile_name="default",
    #         model_id=os.getenv("BEDROCK_LLM_MODEL"),      ## meta.llama2-70b-chat-v1 / anthropic.claude-v2
    #         model_kwargs={"max_tokens_to_sample": token_counts},
    #     )
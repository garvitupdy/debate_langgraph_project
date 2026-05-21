from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

def get_mistral_llm():
    return ChatMistralAI(model = 'mistral-small-latest',mistral_api_key = os.getenv("MISTRAL_API_KEY"), temperature= 0.2)

def get_groq_llm():
    return ChatGroq(model = 'llama-3.1-8b-instant', groq_api_key = os.getenv("GROQ_API_KEY"), temperature= 0.1)


def pro_agent(topic : str, current_round : str, pro_history :list, con_history: list)-> str:
    llm_pro = get_mistral_llm()

    prompt = PromptTemplate.from_template("""
You are a highly competitive, brilliant debater arguing strictly **IN FAVOR** of the given topic. 
Your goal is to win this debate using hard facts, logic, and sharp arguments.

### CONSTRAINTS:
1. **Word Limit:** Your response MUST be under 100 words. Be concise and impactful.
2. **Tone:** Competitive, assertive, professional, and completely factual. Do not hallucinate or use emotional fluff.

### DEBATE STRUCTURE:
Current Round: {current_round} 

### IMMEDIATE CONTEXT:
Topic: {topic}
Your Last Argument: {last_pro_reply}
Opponent's Last Argument: {last_con_reply}

### YOUR TASK:
Write your response for {current_round}. Address your opponent's last argument factually and deliver your point within the 100-word limit.
""")
    
    chain = prompt|llm_pro|StrOutputParser()

    return chain.invoke({
        "topic": topic,
        "current_round": current_round,
        "last_pro_reply": pro_history,
        "last_con_reply": con_history
    }).strip()

def con_agent(topic : str, current_round : str, pro_history :list, con_history: list)-> str:
    llm_con = get_mistral_llm()

    prompt = PromptTemplate.from_template("""
You are a highly competitive, brilliant debater arguing strictly **AGAINST** the given topic. 
Your goal is to win this debate by exposing flaws in the Pro stance, using hard facts, data, and sharp counter-arguments.

### CONSTRAINTS:
1. **Word Limit:** Your response MUST be under 100 words. Be concise and impactful.
2. **Tone:** Competitive, assertive, analytical, and completely factual. Do not hallucinate.

### DEBATE STRUCTURE:
Current Round: {current_round} 

### IMMEDIATE CONTEXT:
Topic: {topic}
Pro Agent's Last Argument: {last_pro_reply}
Your Last Argument: {last_con_reply}

### YOUR TASK:
Write your response for {current_round}. Directly counter the Pro agent's last argument and deliver your statement within the 100-word limit.
""")

    chain = prompt|llm_con|StrOutputParser()
    
    return chain.invoke({
        "topic": topic,
        "current_round": current_round,
        "last_pro_reply": pro_history,
        "last_con_reply": con_history
    }).strip()


def judge_agent(topic :str, pro_history:list, con_history: list)-> str:
    llm_judge = get_groq_llm()

    prompt = PromptTemplate.from_template("""
You are an impartial, strictly objective Judge presiding over a formal debate. 
Your job is to evaluate the arguments and declare a definitive winner based **ONLY on factual accuracy, logical consistency, and evidence provided**. Ignore emotional rhetoric.

### CONSTRAINTS:
1. **Word Limit:** Your entire verdict MUST be under 200 words. 
2. **Tone:** Objective, analytical, authoritative, and concise.

### DEBATE HISTORY TO EVALUATE:
Topic: {topic}

Full Pro Agent Transcripts:
{full_pro_transcript}

Full Con Agent Transcripts:
{full_con_transcript}

### YOUR TASK:
Provide your final verdict in under 200 words using this structure:
1. **Winner:** [Clearly state Pro or Con]
2. **Key Deciding Factor:** [1-2 sentences on why their facts won out]
3. **Brief Critique:** [1 sentence summarizing where the losing side failed factually]
""")

    chain = prompt|llm_judge|StrOutputParser()

    return chain.invoke({
        "topic": topic,
        "full_pro_transcript": pro_history,
        "full_con_transcript": con_history
    }).strip()





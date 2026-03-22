from dotenv import load_dotenv
from functions import call_groq, call_gemini

load_dotenv()

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

groq_llm = ChatGroq(model = "qwen/qwen3-32b",reasoning_format="parsed")
gemini_llm = ChatGoogleGenerativeAI(model = "gemini-3-flash-preview")

groq_msg = ["Hi"]
gemini_msg = ["Hello"]

print(f"Groq:\n{groq_msg[0]}\n")
print(f"Gemini:\n{gemini_msg[0]}\n")

for i in range(5):
    groq_next = call_groq(groq_msg, gemini_msg, groq_llm)
    print(f"{i+1}. Groq:\n{groq_next}\n")
    groq_msg.append(groq_next)
    
    gemini_next = call_gemini(groq_msg, gemini_msg, gemini_llm)
    print(f"{i+1}. Gemini:\n{gemini_next}\n")
    gemini_msg.append(gemini_next)
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import easyocr

load_dotenv()
os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')
reply_llm = ChatGroq(model='llama-3.1-8b-instant')
ocr_llm = "gemini-2.5-flash"



lang_list = ['en']
reader = easyocr.Reader(lang_list, gpu=True) 
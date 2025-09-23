from src.utils.models_loader import ocr_llm
from .prompts import prompt
from .state import State
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from google.genai import types
from google import genai
from langchain_core.messages import HumanMessage



class Generate:
    def __init__(self):
        self.client = genai.Client()
        self.model_name = ocr_llm

    
    def run(self, state:State):
        latest_human_message = next(
            (msg for msg in reversed(state['messages']) if isinstance(msg, HumanMessage)),
            None
        )
        response = self.client.models.generate_content(
        model=self.model_name,

        contents=[
            types.Part.from_bytes(data=state['image'], mime_type="image/jpeg"),
            prompt(latest_human_message)
        ]
        )
        print('The prompt is:', prompt(latest_human_message))
        return {
            'messages':[{'role': 'assistant', 'content': response.text}],
            'suggestions': response.text
        }

     

class Graph:
    def __init__(self):
        self.memory = MemorySaver()
    
    def run(self):
        workflow = StateGraph(State)
        workflow.add_node('generate_pickups', Generate().run)
        workflow.add_edge(START,'generate_pickups')
        workflow.add_edge('generate_pickups',END)
        return workflow.compile(checkpointer=self.memory)
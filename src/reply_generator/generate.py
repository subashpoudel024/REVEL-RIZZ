from src.utils.models_loader import reply_llm
from .prompts import prompt
from .schemas import ReplyFormatter
from .state import State
from langchain_core.messages import SystemMessage, HumanMessage, FunctionMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class Generate:
    def __init__(self):
        self.llm = reply_llm
    
    def run(self, state:State):
        messages = [SystemMessage(content=prompt),
        FunctionMessage(name='conversation-context',content=state['conversation_chat']),
         HumanMessage(content=f'''The required tone: {state["tones"]}''')]
        reply = reply_llm.with_structured_output(ReplyFormatter).invoke(messages)
        print('The reply is:',reply)
        print(reply.model_dump())
        
        return {
            'messages':[{'role': 'assistant', 'content': str(reply.model_dump())}],
            'replies': reply.model_dump()
        }
        

class Graph:
    def __init__(self):
        self.memory = MemorySaver()
    
    def run(self):
        workflow = StateGraph(State)
        workflow.add_node('generate_reply', Generate().run)
        workflow.add_edge(START,'generate_reply')
        workflow.add_edge('generate_reply',END)
        return workflow.compile(checkpointer=self.memory)



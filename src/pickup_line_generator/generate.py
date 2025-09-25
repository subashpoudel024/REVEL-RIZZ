from src.utils.models_loader import reply_llm
from .prompts import pickup_line_prompt
from .schemas import PickupFormatter
from .state import State
from langchain_core.messages import SystemMessage, HumanMessage, FunctionMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class Generate:
    def __init__(self):
        self.llm = reply_llm
    
    def run(self, state:State):
        messages = [SystemMessage(content=pickup_line_prompt),
        FunctionMessage(name='attrubutes',content=f'''The attributes of person are: {state['attributes']}\n. The user is saying: {state['messages'][-1]}'''),
        HumanMessage(content=f'''The required tone: {state["tones"]}''')]
        pickup_lines = reply_llm.with_structured_output(PickupFormatter).invoke(messages)
        return {
            'messages':[{'role': 'assistant', 'content': str(pickup_lines.model_dump())}],
            'pickup_lines': pickup_lines.model_dump()
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



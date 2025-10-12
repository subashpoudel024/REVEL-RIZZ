from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from api.stored_data import stored_data
from src.pickup_line_generator.generate import Graph
from typing import List

router = APIRouter()
pickup_generator = Graph()
graph = pickup_generator.run()

class UserRequest(BaseModel):
    user_query: Optional[str] = None
    tones: Optional[List[str]] = None
    attributes: list


@router.post("/pickup-line-generator")
async def generate_pickup_line(request: UserRequest):
    """
    Endpoint to extract conversation from a base64-encoded image
    """
    config={"configurable": {"thread_id": "reply-generator-thread"}}

    result = graph.invoke({
        'messages': [request.user_query],
        'tones': request.tones,
        'attributes': request.attributes
    },config=config)
    print('The result is:', result)
    return {'response':result['pickup_lines']}
    

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from src.looks_analyzer.generate import Graph

router = APIRouter()
reply_generator = Graph()
graph = reply_generator.run()

class UserRequest(BaseModel):
    image_base64: Optional[str] = None
    user_query: Optional[str] = None


@router.post("/looks-analyzer")
async def generate_reply(request: UserRequest):
    """
    Endpoint to analyze looks
    """
    config={"configurable": {"thread_id": "looks-analyzer-thread"}}

    result = graph.invoke({
        'image': request.image_base64,
        'messages': [request.user_query]
    },config=config)
    # print('The result is:', result)
    return {'response':result['suggestions']}
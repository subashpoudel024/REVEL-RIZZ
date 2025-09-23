import base64
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from src.conversation_extractor.extractor import ConversationExtractor
from api.stored_data import stored_data
from src.reply_generator.generate import Graph
from typing import List

router = APIRouter()
reply_generator = Graph()
graph = reply_generator.run()

class UserRequest(BaseModel):
    image_base64: str
    user_query: Optional[str] = None
    tones: Optional[List[str]] = None

@router.post("/reply-generator")
async def generate_reply(request: UserRequest):
    """
    Endpoint to extract conversation from a base64-encoded image
    """
    config={"configurable": {"thread_id": "reply-generator-thread"}}
    image_bytes = base64.b64decode(request.image_base64)
    conversation_text = ConversationExtractor().extract_conversation(image_bytes)
    stored_data['conversation_context'] = conversation_text

    result = graph.invoke({
        'messages': [request.user_query],
        'tones': request.tones,
        'conversation_chat': stored_data['conversation_context']
    },config=config)
    print('The result is:', result)
    return {'response':result['replies']}
    

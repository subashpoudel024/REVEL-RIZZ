from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from ..serializers import ReplyRequestSerializer
from src.conversation_extractor.extractor import ConversationExtractor
from src.reply_generator.generate  import Graph 
import base64

reply_generator = Graph()
graph = reply_generator.run()
stored_data = {}

@extend_schema(
    request=ReplyRequestSerializer,
    responses={200: dict},
    description=(
        "Endpoint to extract conversation from a base64-encoded image and generate replies.\n\n"
        "### Expected JSON Body:\n"
        "```json\n"
        "{\n"
        "  \"image_base64\": \"<base64-string>\",\n"
        "  \"tones\": [\"friendly\", \"funny\"]\n"
        "}\n"
        "```"
    ),
)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_reply(request):
    """
    Endpoint to extract conversation from a base64-encoded image
    Expects JSON: {"image_base64": "...", "tones": ["friendly", "funny"]}
    """
    if request.method == 'POST':
        image_base64 = request.data.get('image_base64')
        tones = request.data.get('tones', None)

        if not image_base64:
            return Response(
                {"error": "'image_base64' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Decode base64 image
            image_bytes = base64.b64decode(image_base64)
        except Exception as e:
            return Response(
                {"error": f"Invalid base64 image: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract conversation from image
        conversation_text = ConversationExtractor().extract_conversation(image_bytes)
        stored_data['conversation_context'] = conversation_text

        # Invoke the graph
        config = {"configurable": {"thread_id": "reply-generator-thread"}}
        result = graph.invoke({
            'tones': tones,
            'conversation_chat': stored_data['conversation_context']
        }, config=config)

        return Response({'response': result.get('replies', [])})
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from ..serializers import LooksAnalyzerRequestSerializer
from src.looks_analyzer.generate import Graph 

looks_analyzer = Graph()
graph = looks_analyzer.run()


@extend_schema(
    request=LooksAnalyzerRequestSerializer,
    responses={200: dict},
    description=(
        "Endpoint to analyze looks based on an image or a user query.\n\n"
        "### Expected JSON Body:\n"
        "```json\n"
        "{\n"
        "  \"image_base64\": \"<base64-string>\",\n"
        "  \"user_query\": \"Describe my look\"\n"
        "}\n"
        "```"
    ),
)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_looks(request):
    """
    Endpoint to analyze looks
    Expects JSON: {"image_base64": "...", "user_query": "..."}
    """
    if request.method == 'POST':
        image_base64 = request.data.get('image_base64', None)
        user_query = request.data.get('user_query', None)

        if not image_base64 and not user_query:
            return Response(
                {"error": "At least one of 'image_base64' or 'user_query' must be provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        config = {"configurable": {"thread_id": "looks-analyzer-thread"}}

        result = graph.invoke({
            'image': image_base64,
            'messages': [user_query] if user_query else []
        }, config=config)

        return Response({'response': result.get('suggestions', [])})
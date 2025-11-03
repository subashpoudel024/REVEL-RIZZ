from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from ..serializers import PickupLineRequestSerializer
from src.pickup_line_generator.generate import Graph 


pickup_generator = Graph()
graph = pickup_generator.run()

@extend_schema(
    request=PickupLineRequestSerializer,
    responses={200: dict},
    description="Generate pickup lines with tones and attributes."
)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_pickup_line(request):
    serializer = PickupLineRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    user_query = data['user_query']
    tones = data.get('tones', [])
    attributes = data.get('attributes', [])

    config = {"configurable": {"thread_id": "pickup-line-generator-thread"}}

    result = graph.invoke({
        'messages': [user_query],
        'tones': tones,
        'attributes': attributes
    }, config=config)

    return Response({'response': result.get('pickup_lines', [])})

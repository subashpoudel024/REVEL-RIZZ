from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from typing import Optional
from pydantic import BaseModel
from src.looks_analyzer.generate import Graph as LooksAnalyzeGraph
from src.reply_generator.generate import Graph as ReplyGenerateGraph
from src.pickup_line_generator.generate import Graph as PickupGenerateGraph


import base64
from src.conversation_extractor.extractor import ConversationExtractor

stored_data = {}

# Initialize your agentic graph (same as FastAPI)
reply_generator = ReplyGenerateGraph()
reply_generator_graph = reply_generator.run()

looks_analyzer = LooksAnalyzeGraph()
looks_analyzer_graph = looks_analyzer.run()

pickup_generatpr = PickupGenerateGraph()
pickup_generator_graph = pickup_generatpr.run()


@api_view(['POST'])
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

        result = looks_analyzer_graph.invoke({
            'image': image_base64,
            'messages': [user_query] if user_query else []
        }, config=config)

        return Response({'response': result.get('suggestions', [])})

@api_view(['POST'])
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
        result = reply_generator_graph.invoke({
            'tones': tones,
            'conversation_chat': stored_data['conversation_context']
        }, config=config)

        return Response({'response': result.get('replies', [])})


@api_view(['POST'])
def generate_pickup_line(request):
    """
    Endpoint to generate pickup lines
    Expects JSON:
    {
        "user_query": "string",
        "tones": ["funny", "friendly"],
        "attributes": ["charming", "cute"]
    }
    """
    if request.method == 'POST':
        user_query = request.data.get('user_query', None)
        tones = request.data.get('tones', None)
        attributes = request.data.get('attributes', [])

        if not user_query:
            return Response(
                {"error": "'user_query' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not isinstance(attributes, list):
            return Response(
                {"error": "'attributes' must be a list."},
                status=status.HTTP_400_BAD_REQUEST
            )

        config = {"configurable": {"thread_id": "pickup-line-generator-thread"}}

        result = pickup_generator_graph.invoke({
            'messages': [user_query],
            'tones': tones,
            'attributes': attributes
        }, config=config)

        # Optionally store context if needed
        stored_data['last_pickup_line_query'] = user_query

        return Response({'response': result.get('pickup_lines', [])})



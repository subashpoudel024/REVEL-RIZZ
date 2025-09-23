
from google import genai
from google.genai import types
from src.utils.models_loader import ocr_llm
from .prompts import prompt

from dotenv import load_dotenv
import os

load_dotenv()
os.environ['GOOGLE_API_KEY']=os.getenv('GOOGLE_API_KEY')

class ConversationExtractor:
    def __init__(self):
        self.client = genai.Client()
        self.model_name = ocr_llm
        self.prompt = prompt

    def extract_conversation(self, image_bytes: bytes) -> str:
        """
        Extract conversation text from an image.
        :param image_bytes: Binary content of the image
        :return: Extracted conversation text
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                self.prompt
            ]
        )
        return response.text

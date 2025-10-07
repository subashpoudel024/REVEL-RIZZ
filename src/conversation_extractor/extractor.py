
from google import genai
from google.genai import types
from src.utils.models_loader import ocr_llm , reply_llm , reader
from .prompts import prompt
import easyocr
from PIL import Image
import io
import numpy as np
from dotenv import load_dotenv
import os
from langchain_core.messages import HumanMessage , SystemMessage

load_dotenv()
os.environ['GOOGLE_API_KEY']=os.getenv('GOOGLE_API_KEY')

class ConversationExtractor:
    def __init__(self):
        self.client = genai.Client()
        self.model_name = ocr_llm
        self.prompt = prompt
    
    def complete_ocr(self, image_bytes:bytes , lang_list=['en']):
        img = Image.open(io.BytesIO(image_bytes))
        w_img = img.width

        # Convert PIL image to RGB and read it directly using EasyOCR
        results = reader.readtext(np.array(img))  # Use numpy array instead of file path

        conversation = []
        for bbox, text, conf in results:
            # bbox: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
            x_coords = [p[0] for p in bbox]
            y_coords = [p[1] for p in bbox]
            x, y, w, h = int(min(x_coords)), int(min(y_coords)), int(max(x_coords)-min(x_coords)), int(max(y_coords)-min(y_coords))

            # Determine left or right speaker
            speaker = "A" if (x + w/2) < w_img/2 else "B"

            conversation.append({
                "speaker": speaker,
                "text": text.strip(),
                "box": [x, y, w, h]
            })

        # Sort top to bottom
        raw_ocr = sorted(conversation, key=lambda x: x["box"][1])
        raw_ocr_text = "Detected Conversation:\n" + "\n".join(
        [f"Line {i}: {turn['text']}" for i, turn in enumerate(raw_ocr, start=1)]
        )
        return raw_ocr_text
    
    def extract_conversation(self, image_bytes:bytes):
        raw_ocr_text=self.complete_ocr(image_bytes)
        messages = [SystemMessage(content = prompt),
        HumanMessage(content = raw_ocr_text)]
        response =reply_llm.invoke(messages)
        print('The cleaned ocr:', response.content)
        return response.content


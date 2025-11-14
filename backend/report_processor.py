import io
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes
import anthropic
import os
import shutil
from typing import Dict, Any, Optional

# Configure tesseract path for different environments
if shutil.which('tesseract'):
    pytesseract.pytesseract.tesseract_cmd = shutil.which('tesseract')
else:
    # Try common paths
    for path in ['/usr/bin/tesseract', '/usr/local/bin/tesseract']:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            break

# Lazy initialization of Anthropic client
# Set your API key in environment variable: ANTHROPIC_API_KEY
_anthropic_client: Optional[anthropic.Anthropic] = None

def get_anthropic_client() -> Optional[anthropic.Anthropic]:
    """Get or create Anthropic client if API key is available."""
    global _anthropic_client
    if _anthropic_client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        if api_key:
            try:
                _anthropic_client = anthropic.Anthropic(api_key=api_key)
            except Exception as e:
                print(f"Warning: Could not initialize Anthropic client: {e}")
                return None
    return _anthropic_client


async def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extract text from an image using OCR (Tesseract).
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error extracting text from image: {str(e)}")
        raise


async def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text from a PDF file.
    First tries to extract text directly, then falls back to OCR if needed.
    """
    try:
        # Try using pdf2image to convert PDF to images (requires poppler)
        images = convert_from_bytes(pdf_bytes)
        
        # Extract text from each page using OCR
        full_text = ""
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image)
            full_text += f"\n--- Page {i + 1} ---\n{text}\n"
        
        return full_text
    except Exception as e:
        error_msg = str(e)
        if "poppler" in error_msg.lower() or "Unable to get page count" in error_msg:
            raise ValueError(
                "PDF processing requires Poppler. Install it with: brew install poppler (macOS) or "
                "sudo apt-get install poppler-utils (Linux). PDF files cannot be processed without Poppler."
            )
        print(f"Error extracting text from PDF: {error_msg}")
        raise


async def parse_with_genai(text: str) -> Dict[str, Any]:
    """
    Use Anthropic Claude to parse medical report text and extract structured data.
    """
    anthropic_client = get_anthropic_client()
    
    if not anthropic_client:
        print("Warning: Anthropic API key not set. Using mock data.")
        return {
            "conditions": ["Mild symptoms"],
            "test_results": [],
            "symptoms": ["General discomfort"],
            "severity": "low"
        }
    
    try:
        prompt = f"""Analyze the following medical report text and extract structured information.
Return a JSON object with the following structure:
{{
    "conditions": ["list of medical conditions found"],
    "test_results": ["list of test results with values"],
    "symptoms": ["list of symptoms mentioned"],
    "severity": "low|moderate|high|critical",
    "summary": "brief summary of the report"
}}

Medical Report Text:
{text}

Only return the JSON object, no additional text."""

        message = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.3,
            system="You are a medical report analyzer. Extract structured information from medical reports.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Parse the response
        result_text = message.content[0].text.strip()
        
        # Try to extract JSON from the response
        import json
        # Remove markdown code blocks if present
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        parsed_data = json.loads(result_text)
        return parsed_data
    
    except Exception as e:
        print(f"Error parsing with GenAI: {str(e)}")
        # Return fallback data
        return {
            "conditions": ["Unable to parse"],
            "test_results": [],
            "symptoms": [],
            "severity": "low",
            "summary": "Error parsing report"
        }


async def process_medical_report(file_contents: bytes, content_type: str, file_name: str) -> Dict[str, Any]:
    """
    Main function to process a medical report file.
    Returns structured data extracted from the report.
    """
    try:
        # Extract text based on file type
        if content_type.startswith("image/"):
            print(f"Extracting text from image: {file_name}")
            raw_text = await extract_text_from_image(file_contents)
        elif content_type == "application/pdf":
            print(f"Extracting text from PDF: {file_name}")
            raw_text = await extract_text_from_pdf(file_contents)
        else:
            raise ValueError(f"Unsupported content type: {content_type}")
        
        print(f"Extracted text length: {len(raw_text)} characters")
        
        # Parse text with GenAI
        print("Parsing with GenAI...")
        parsed_data = await parse_with_genai(raw_text)
        parsed_data["raw_text"] = raw_text[:500]  # Include first 500 chars for debugging
        
        return parsed_data
    
    except Exception as e:
        print(f"Error in process_medical_report: {str(e)}")
        raise


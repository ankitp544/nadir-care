import anthropic
import os
import base64
import re
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
# Get the directory where this script is located
script_dir = Path(__file__).parent
env_path = script_dir / ".env"

# Load .env file if it exists
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print(f"Loaded .env file from: {env_path}")
else:
    # Try loading from current directory as fallback
    load_dotenv()
    if not os.getenv("ANTHROPIC_API_KEY"):
        print(f"Warning: .env file not found at {env_path}")
        print("Please create a .env file in the backend directory with: ANTHROPIC_API_KEY=your_key")

# Lazy initialization of Anthropic client
# Set your API key in environment variable: ANTHROPIC_API_KEY or .env file
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
        else:
            print("Warning: ANTHROPIC_API_KEY not found in environment variables or .env file")
    return _anthropic_client


async def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extract text from an image.
    Note: OCR functionality has been removed.
    """
    raise ValueError("Image text extraction is not available. OCR dependencies have been removed.")


async def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text from a PDF file.
    Note: PDF processing functionality has been removed.
    """
    raise ValueError("PDF text extraction is not available. PDF processing dependencies have been removed.")


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


async def extract_anc_from_cbc_image(image_bytes: bytes) -> Dict[str, Any]:
    """
    Extract Absolute Neutrophil Count (ANC) from a CBC report image using Claude Haiku 4.5 with vision.
    
    Args:
        image_bytes: The image file as bytes
        
    Returns:
        Dictionary containing the extracted ANC value and metadata
    """
    anthropic_client = get_anthropic_client()
    
    if not anthropic_client:
        raise ValueError("Anthropic API key not set. Please set ANTHROPIC_API_KEY environment variable.")
    
    try:
        # Convert image bytes to base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        # Determine media type based on image format
        # Check magic bytes to detect image type
        if image_bytes.startswith(b'\xff\xd8\xff'):
            media_type = "image/jpeg"
        elif image_bytes.startswith(b'\x89PNG\r\n\x1a\n'):
            media_type = "image/png"
        elif image_bytes.startswith(b'GIF87a') or image_bytes.startswith(b'GIF89a'):
            media_type = "image/gif"
        elif len(image_bytes) >= 12 and image_bytes[:4] == b'RIFF' and image_bytes[8:12] == b'WEBP':
            media_type = "image/webp"
        else:
            # Default to JPEG if format cannot be determined
            media_type = "image/jpeg"
        
        # Load the prompt from file
        prompt_file = Path(__file__).parent / "prompts" / "anc_extraction_prompt.txt"
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompt = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Prompt file not found: {prompt_file}. "
                "Please ensure the prompts/anc_extraction_prompt.txt file exists."
            )
        
        # Replace the placeholder with actual instruction
        prompt = prompt.replace("{{IMAGE}}", "[The CBC report image is provided below]")
        
        # Create the message with image and text content
        message = anthropic_client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            temperature=0.3,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": base64_image
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        )
        
        # Extract the response text
        response_text = message.content[0].text.strip()
        
        # Parse the response to extract the answer
        anc_value = None
        status = "unknown"
        answer_section = None
        
        if "<answer>" in response_text and "</answer>" in response_text:
            answer_section = response_text.split("<answer>")[1].split("</answer>")[0].strip()
            
            if "not found" in answer_section.lower():
                status = "not_found"
            elif "too unclear" in answer_section.lower() or "unreadable" in answer_section.lower():
                status = "unclear"
            else:
                # Try to extract the numerical value
                # Look for patterns like "1234 per microliter" or "1.5 per microliter"
                # Match numbers (including decimals) followed by "per microliter" or similar
                match = re.search(r'([\d,]+\.?\d*)\s*(?:per\s+)?microliter', answer_section, re.IGNORECASE)
                if match:
                    anc_value_str = match.group(1).replace(',', '')
                    try:
                        anc_value = float(anc_value_str)
                        status = "success"
                    except ValueError:
                        status = "parse_error"
                else:
                    # Try to extract just a number
                    numbers = re.findall(r'[\d,]+\.?\d*', answer_section)
                    if numbers:
                        try:
                            anc_value = float(numbers[0].replace(',', ''))
                            status = "success"
                        except ValueError:
                            status = "parse_error"
        
        return {
            "anc_value": anc_value,
            "status": status,
            "raw_response": response_text,
            "answer_section": answer_section
        }
    
    except Exception as e:
        print(f"Error extracting ANC from CBC image: {str(e)}")
        raise


async def process_medical_report(file_contents: bytes, content_type: str, file_name: str) -> Dict[str, Any]:
    """
    Main function to process a medical report file.
    Returns structured data extracted from the report.
    """
    try:
        # Process based on file type
        if content_type.startswith("image/"):
            print(f"Processing CBC report image: {file_name}")
            
            # Extract ANC from CBC image using vision model
            anc_result = await extract_anc_from_cbc_image(file_contents)
            
            # Format the results for the recommendation engine
            parsed_data = {
                "conditions": [],
                "test_results": [],
                "symptoms": [],
                "severity": "low",
                "summary": ""
            }
            
            # Add ANC information
            if anc_result["status"] == "success" and anc_result["anc_value"] is not None:
                anc_value = anc_result["anc_value"]
                parsed_data["test_results"] = [
                    f"Absolute Neutrophil Count (ANC): {anc_value} per microliter"
                ]
                
                # Determine severity based on ANC value
                # Normal ANC: 1500-8000 per microliter
                # Mild neutropenia: 1000-1500
                # Moderate neutropenia: 500-1000
                # Severe neutropenia: <500
                if anc_value < 500:
                    parsed_data["severity"] = "critical"
                    parsed_data["conditions"] = ["Severe neutropenia"]
                    parsed_data["summary"] = f"Critical: Severe neutropenia detected (ANC: {anc_value} per microliter). Immediate medical attention required."
                elif anc_value < 1000:
                    parsed_data["severity"] = "high"
                    parsed_data["conditions"] = ["Moderate neutropenia"]
                    parsed_data["summary"] = f"High severity: Moderate neutropenia detected (ANC: {anc_value} per microliter). Medical consultation recommended."
                elif anc_value < 1500:
                    parsed_data["severity"] = "moderate"
                    parsed_data["conditions"] = ["Mild neutropenia"]
                    parsed_data["summary"] = f"Moderate: Mild neutropenia detected (ANC: {anc_value} per microliter). Monitor and consult healthcare provider."
                else:
                    parsed_data["severity"] = "low"
                    parsed_data["conditions"] = ["Normal neutrophil count"]
                    parsed_data["summary"] = f"Normal ANC value: {anc_value} per microliter."
            elif anc_result["status"] == "not_found":
                parsed_data["summary"] = "Absolute Neutrophil Count not found in the CBC report image."
                parsed_data["test_results"] = ["ANC extraction: Not found in image"]
            elif anc_result["status"] == "unclear":
                parsed_data["summary"] = "Image quality too poor to read the Absolute Neutrophil Count."
                parsed_data["test_results"] = ["ANC extraction: Image unclear"]
            else:
                parsed_data["summary"] = f"ANC extraction status: {anc_result['status']}"
                parsed_data["test_results"] = [f"ANC extraction: {anc_result['status']}"]
            
            # Include raw response for debugging
            parsed_data["anc_extraction"] = anc_result
            print(f"ANC extraction result: {anc_result}")
            return parsed_data
            
        elif content_type == "application/pdf":
            print(f"Extracting text from PDF: {file_name}")
            raw_text = await extract_text_from_pdf(file_contents)
            
            print(f"Extracted text length: {len(raw_text)} characters")
            
            # Parse text with GenAI
            print("Parsing with GenAI...")
            parsed_data = await parse_with_genai(raw_text)
            parsed_data["raw_text"] = raw_text[:500]  # Include first 500 chars for debugging
            
            return parsed_data
        else:
            raise ValueError(f"Unsupported content type: {content_type}")
    
    except Exception as e:
        print(f"Error in process_medical_report: {str(e)}")
        raise


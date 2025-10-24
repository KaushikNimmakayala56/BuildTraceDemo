"""
Gemini Service - AI-powered drawing analysis using Google Gemini 2.0 Flash
Two-step process: Extract problem number → Analyze with targeted context
"""

import os
import json
import re
from typing import Dict, Optional
from pathlib import Path
import google.generativeai as genai
from PIL import Image
import io
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class GeminiService:
    """Service to interact with Gemini AI for drawing analysis"""
    
    def __init__(self):
        # Get API key from environment
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("❌ GEMINI_API_KEY not found in environment")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Model configuration
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')
        self.generation_config = {
            "temperature": 0.2,  # Low temperature for consistent, factual responses
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
        
        # Initialize model
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=self.generation_config
        )
        
        print(f"✅ Gemini Service initialized with model: {self.model_name}")
    
    def extract_problem_number(self, image_bytes: bytes) -> Optional[str]:
        """
        Extract problem number from image using Gemini Vision
        
        Args:
            image_bytes: Image file bytes
            
        Returns:
            str: Problem number (e.g., "12-12") or None if not found
        """
        try:
            # Prepare image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Simple prompt to extract problem number
            prompt = """
Look at this engineering drawing problem image.

What is the problem number shown in the image?

Return ONLY the problem number in format "12-X" where X is the number.
For example: "12-12" or "12-1" or "12-5"

If no problem number is visible, return "UNKNOWN"

Response (just the number, nothing else):
"""
            
            print("🔍 Extracting problem number from image...")
            
            # Send to Gemini
            response = self.model.generate_content([prompt, image])
            result = response.text.strip()
            
            print(f"  Raw response: {result}")
            
            # Parse response to extract problem number
            # Look for pattern "12-X" or "Problem 12-X"
            match = re.search(r'12[-\s](\d+)', result)
            if match:
                problem_num = f"12-{match.group(1)}"
                print(f"  ✅ Extracted problem number: {problem_num}")
                return problem_num
            
            print("  ⚠️  Could not extract problem number")
            return None
            
        except Exception as e:
            print(f"❌ Error extracting problem number: {str(e)}")
            return None
    
    def analyze_drawing(
        self, 
        image_bytes: bytes, 
        textbook_context: str,
        problem_number: Optional[str] = None
    ) -> Dict:
        """
        Analyze drawing and generate step-by-step solution
        
        Args:
            image_bytes: Image file bytes
            textbook_context: Relevant textbook section text
            problem_number: Optional problem number for context
            
        Returns:
            dict: Analysis results with steps
        """
        try:
            # Prepare image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Construct prompt
            prompt = self._build_analysis_prompt(textbook_context, problem_number)
            
            print(f"🤖 Analyzing drawing with Gemini...")
            print(f"  Context size: {len(textbook_context)} characters")
            
            # Send to Gemini
            response = self.model.generate_content([prompt, image])
            result_text = response.text.strip()
            
            print(f"  ✅ Received response: {len(result_text)} characters")
            
            # Parse JSON response
            parsed = self._parse_response(result_text)
            
            return parsed
            
        except Exception as e:
            print(f"❌ Error analyzing drawing: {str(e)}")
            return {
                "error": str(e),
                "problem_identification": "Error occurred",
                "construction_steps": []
            }
    
    def _build_analysis_prompt(self, textbook_context: str, problem_number: Optional[str]) -> str:
        """Build the analysis prompt with textbook context"""
        
        problem_context = f" (Problem {problem_number})" if problem_number else ""
        
        prompt = f"""
You are an expert Engineering Drawing tutor specializing in Projections of Planes{problem_context}.

=== CRITICAL INSTRUCTIONS ===
1. You MUST use ONLY the textbook content provided below to answer
2. DO NOT use any external knowledge or information not in this textbook
3. If something is not covered in the textbook, state "Not covered in provided textbook"
4. Be educational, clear, and encouraging - you're teaching students

=== TEXTBOOK CONTENT START ===
{textbook_context}
=== TEXTBOOK CONTENT END ===

=== YOUR TASK ===
Analyze this incomplete engineering drawing problem and provide a step-by-step guide to complete it.

Return your response as a JSON object with this EXACT structure:
{{
  "problem_identification": "Brief description of what problem this is",
  "given_information": [
    "List each piece of given information",
    "Example: Circular plate 50mm diameter",
    "Example: Appears as ellipse in front view"
  ],
  "required_output": "What needs to be drawn/completed",
  "key_concept": "Main concept from textbook being applied",
  "construction_steps": [
    {{
      "step": 1,
      "instruction": "Clear, actionable instruction",
      "explanation": "Why this step is necessary and what principle applies"
    }},
    {{
      "step": 2,
      "instruction": "Next instruction",
      "explanation": "Explanation with reasoning"
    }}
    // Continue for 4-6 steps total
  ],
  "common_mistakes": [
    "What students typically get wrong",
    "Common errors to avoid"
  ]
}}

=== GUIDELINES ===
- Provide 4-6 construction steps (not too few, not too many)
- Each step must be clear and actionable
- Use exact terminology from the textbook
- Be educational and encouraging
- Reference specific concepts or methods from textbook when relevant
- Steps should be in logical construction order

IMPORTANT: Return ONLY the JSON object, no markdown formatting, no code blocks.
"""
        
        return prompt
    
    def _parse_response(self, response_text: str) -> Dict:
        """Parse and validate Gemini JSON response"""
        try:
            # Remove any markdown code block formatting
            cleaned = response_text.strip()
            if cleaned.startswith('```'):
                # Remove ```json and ``` markers
                cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned)
                cleaned = re.sub(r'\s*```$', '', cleaned)
            
            # Parse JSON
            parsed = json.loads(cleaned)
            
            # Validate required fields
            required_fields = ['problem_identification', 'construction_steps']
            for field in required_fields:
                if field not in parsed:
                    print(f"⚠️  Missing required field: {field}")
                    parsed[field] = "Not provided" if field == 'problem_identification' else []
            
            # Validate construction_steps structure
            if not isinstance(parsed['construction_steps'], list):
                print("⚠️  construction_steps is not a list")
                parsed['construction_steps'] = []
            
            # Ensure each step has required fields
            for i, step in enumerate(parsed['construction_steps']):
                if 'step' not in step:
                    step['step'] = i + 1
                if 'instruction' not in step:
                    step['instruction'] = "Step instruction not provided"
                if 'explanation' not in step:
                    step['explanation'] = "Explanation not provided"
            
            print(f"  ✅ Parsed {len(parsed['construction_steps'])} construction steps")
            
            return parsed
            
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON response: {str(e)}")
            print(f"  Raw response: {response_text[:200]}...")
            return {
                "error": "Failed to parse AI response",
                "problem_identification": "Parse error",
                "construction_steps": [],
                "raw_response": response_text
            }


# Global instance
_gemini_service = None


def get_gemini_service() -> GeminiService:
    """Get the global Gemini service instance"""
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service


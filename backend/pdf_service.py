"""
PDF Service - Loads and parses engineering drawing textbook
Splits textbook into individual problem sections for targeted context retrieval
"""

import re
from typing import Dict, Optional
import PyPDF2
from pathlib import Path


class PDFService:
    """Service to load and parse PDF textbook into problem sections"""
    
    def __init__(self):
        self.full_text = ""
        self.problem_sections = {}
        self.loaded = False
        self.pdf_path = None
        
    def load_and_parse(self, pdf_path: str) -> bool:
        """
        Load PDF and parse into problem sections
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.pdf_path = pdf_path
            
            # Check if file exists
            if not Path(pdf_path).exists():
                print(f"❌ PDF file not found: {pdf_path}")
                return False
            
            # Extract text from PDF
            print(f"📖 Loading PDF from: {pdf_path}")
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                page_count = len(pdf_reader.pages)
                print(f"📄 Found {page_count} pages")
                
                # Extract text from all pages
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    self.full_text += text + "\n"
                    print(f"  ✓ Extracted page {page_num}/{page_count}")
            
            print(f"✅ Extracted {len(self.full_text)} characters total")
            
            # Parse into problem sections
            self._parse_problem_sections()
            
            self.loaded = True
            print(f"🎯 Successfully parsed {len(self.problem_sections)} problem sections")
            return True
            
        except Exception as e:
            print(f"❌ Error loading PDF: {str(e)}")
            return False
    
    def _parse_problem_sections(self):
        """
        Parse full text into individual problem sections
        Uses regex to find "Problem 12-X" markers
        """
        # Pattern to find problem numbers (e.g., "Problem 12-1", "Problem 12-12")
        problem_pattern = r'Problem\s+12-(\d+)'
        
        # Find all problem numbers
        matches = list(re.finditer(problem_pattern, self.full_text, re.IGNORECASE))
        
        if not matches:
            print("⚠️  No problem markers found, will use full text as fallback")
            return
        
        print(f"🔍 Found {len(matches)} problem markers")
        
        # Extract sections between problem markers
        for i, match in enumerate(matches):
            problem_num = match.group(1)
            start_pos = match.start()
            
            # End position is start of next problem, or end of text
            if i + 1 < len(matches):
                end_pos = matches[i + 1].start()
            else:
                end_pos = len(self.full_text)
            
            # Extract section text (include some context before problem statement)
            context_start = max(0, start_pos - 500)  # Include 500 chars before
            section_text = self.full_text[context_start:end_pos].strip()
            
            # Store in dictionary with key format "12-X"
            key = f"12-{problem_num}"
            self.problem_sections[key] = section_text
            
            print(f"  ✓ Problem {key}: {len(section_text)} characters")
    
    def get_problem_section(self, problem_number: str) -> Optional[str]:
        """
        Get text for specific problem section
        
        Args:
            problem_number: Problem number (e.g., "12-12" or "12-1")
            
        Returns:
            str: Problem section text, or None if not found
        """
        # Normalize format (handle both "12-12" and "12.12")
        normalized = problem_number.replace(".", "-")
        if not normalized.startswith("12-"):
            normalized = f"12-{normalized}"
        
        return self.problem_sections.get(normalized)
    
    def get_full_text(self) -> str:
        """Get full textbook text (fallback when specific problem not found)"""
        return self.full_text
    
    def get_status(self) -> Dict:
        """Get service status"""
        return {
            "loaded": self.loaded,
            "pdf_path": self.pdf_path,
            "total_problems": len(self.problem_sections),
            "problem_numbers": sorted(self.problem_sections.keys()),
            "total_characters": len(self.full_text)
        }


# Global instance (singleton pattern)
pdf_service = PDFService()


def get_pdf_service() -> PDFService:
    """Get the global PDF service instance"""
    return pdf_service


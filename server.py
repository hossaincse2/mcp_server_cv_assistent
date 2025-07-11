# server.py
from mcp.server.fastmcp import FastMCP
import PyPDF2
import os
from typing import Dict, Any, Union
import json

# Create an MCP server
mcp = FastMCP(name="CV Assistant")

# Global variable to store PDF content
pdf_content = ""


def load_pdf_content():
    """Load PDF content at startup"""
    global pdf_content
    pdf_path = r"C:\Users\Ui Barn\Downloads\Mohammad_Hossain_CV_2025.pdf"

    try:
        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                pdf_content = ""
                for page in pdf_reader.pages:
                    pdf_content += page.extract_text() + "\n"
            print(f"PDF loaded successfully. Content length: {len(pdf_content)} characters")
        else:
            print(f"PDF file not found at: {pdf_path}")
            pdf_content = "PDF file not found"
    except Exception as e:
        print(f"Error loading PDF: {e}")
        pdf_content = f"Error loading PDF: {e}"


# Load PDF content when server starts
load_pdf_content()


@mcp.resource("file://cv/content")
def get_cv_content() -> str:
    """Get the full CV content from PDF."""
    return pdf_content


@mcp.resource("file://cv/summary")
def get_cv_summary() -> str:
    """Get a summary of the CV."""
    if pdf_content and len(pdf_content) > 100:
        # Return first 500 characters as summary
        return pdf_content[:500] + "..."
    return pdf_content


@mcp.tool("search_cv")
def search_cv(query: str) -> str:
    """Search for specific information in the CV."""
    if not pdf_content:
        return "CV content not available"

    query_lower = query.lower()
    lines = pdf_content.split('\n')
    relevant_lines = []

    for line in lines:
        if query_lower in line.lower():
            relevant_lines.append(line.strip())

    if relevant_lines:
        return "\n".join(relevant_lines[:5])  # Return top 5 matches
    else:
        return f"No information found for '{query}' in the CV"


@mcp.tool("ask_about_cv")
def ask_about_cv(question: str) -> str:
    """Answer questions about the CV content."""
    if not pdf_content:
        return "CV content not available"

    question_lower = question.lower()

    # Enhanced keyword-based responses
    if any(word in question_lower for word in ['programming', 'languages', 'coding', 'tech', 'skills']):
        # Look for programming languages and technical skills
        keywords = ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
                    'html', 'css', 'sql', 'react', 'angular', 'vue', 'node', 'django', 'flask']
        found_skills = []
        for keyword in keywords:
            if keyword.lower() in pdf_content.lower():
                found_skills.append(keyword)

        if found_skills:
            return f"Programming languages and technologies found in CV: {', '.join(found_skills)}"
        else:
            return search_cv("skills") or search_cv("technology") or "Programming languages not clearly identified"

    elif any(word in question_lower for word in ['experience', 'work', 'job']):
        return search_cv("experience") or search_cv("work") or "Experience information not found"

    elif any(word in question_lower for word in ['education', 'degree', 'university']):
        return search_cv("education") or search_cv("university") or "Education information not found"

    elif any(word in question_lower for word in ['contact', 'email', 'phone']):
        return search_cv("email") or search_cv("phone") or search_cv("contact") or "Contact information not found"

    else:
        # General search
        return search_cv(question)


@mcp.tool("get_cv_sections")
def get_cv_sections() -> Dict[str, Union[str, int]]:
    """Get different sections of the CV."""
    if not pdf_content:
        return {"error": "CV content not available"}

    sections = {
        "full_content": pdf_content,
        "length": len(pdf_content),  # This is an int
        "preview": pdf_content[:200] + "..." if len(pdf_content) > 200 else pdf_content
    }

    return sections


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
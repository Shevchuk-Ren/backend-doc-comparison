SUMMARY_SCHEMA = """
{
  "document_type": "string",
  "main_purpose": "short explanation of the document",
  "key_points": [
    "important point 1",
    "important point 2"
  ],
  "pros": [
    "advantages or beneficial conditions"
  ],
  "cons": [
    "disadvantages or limitations"
  ],
  "risk_flags": [
    "potential risks or problematic clauses"
  ],
  "decision_summary": "short summary explaining what a decision maker should know first"
}
"""

SYSTEM_PROMPT = """
You are an expert document analysis assistant.

You analyze business documents such as contracts, commercial offers, and technical specifications.

Your goal is to extract structured information that helps compare multiple documents and make
decisions.

Rules:
- Use ONLY information explicitly present in the document.
- Do NOT invent information.
- If something is not specified, return null or an empty list.
- Keep responses concise and factual.
- Always return valid JSON only.
"""


def build_document_prompt(document_text: str) -> str:
    return f"""
Analyze the following document and return a structured JSON response.

Extract the most important decision-relevant information.

Return JSON in this exact structure:
{SUMMARY_SCHEMA}

Document text:
{document_text}
"""

import os

script_dir = os.path.dirname(os.path.abspath(__file__))

CONTEXT_FILE = os.getenv("AIWRITER_CONTEXT_FILE", "context.txt")
CONTEXT_FULL_FILE = os.getenv("AIWRITER_CONTEXT_FULL_FILE", "full_context.txt")
CONTEXT_DIR = os.getenv("AIWRITER_CONTEXT_DIR", "context")

MODEL = os.getenv("AIWRITER_MODEL", "anthropic/claude-sonnet-4-20250514")
ESSAY_FILE = os.getenv("AIWRITER_ESSAY_FILE", "essay.txt")

CRITERIA = "clarity,conciseness,relevance,engagement,accuracy".split(",")
CRITERIA_FILE = os.getenv("AIWRITER_CRITERIA", "criteria.txt")
if os.path.exists(CRITERIA_FILE):
    with open(CRITERIA_FILE) as cf:
        CRITERIA = [c.strip() for c in cf.read().split(",") if c.strip()]

SCORES_FILE = os.getenv("AIWRITER_SCORES", "scores.txt")

DRAFTS_DIR = os.getenv("AIWRITER_DRAFTS_DIR", "drafts")


# ------ THINKER_SYSTEM_PROMPT ------
DEFAULT_THINKER_SYSTEM_PROMPT = """You are an expert analyst. Your task is to extract key insights from the provided text. 

Instructions:
- Read the text carefully.
- Identify and list the most important insights, findings, or conclusions.
- For each insight, provide a brief explanation or supporting evidence from the text.
- Present your answer as a numbered list.
- Do not include irrelevant details or copy large sections verbatim.
- If the text lacks clear insights, state "No significant insights found."
"""

THINKER_SYSTEM_PROMPT = (
    open("AIWRITER_THINKER_SYSTEM_PROMPT_FILE", "r").read()
    if os.path.exists("AIWRITER_THINKER_SYSTEM_PROMPT_FILE")
    else DEFAULT_THINKER_SYSTEM_PROMPT
)

# ------ WRITER_SYSTEM_PROMPT ------
DEFAULT_WRITER_SYSTEM_PROMPT = """You are an expert essay writer.

Context:
{{context}}

Task:
{{task}}

Requirements:
- Length: Up to {{length}} words (approximate)
- Style: {{style}} (e.g., formal, informal, persuasive, analytical)
- Audience: {{audience}}
- Structure: Introduction, body paragraphs, and conclusion
- Cite evidence or examples where appropriate

Criteria for assessment:
{{criteria}}
"""

WRITER_SYSTEM_PROMPT = (
    open("AIWRITER_WRITER_SYSTEM_PROMPT_FILE", "r").read()
    if os.path.exists("AIWRITER_WRITER_SYSTEM_PROMPT_FILE")
    else DEFAULT_WRITER_SYSTEM_PROMPT
)

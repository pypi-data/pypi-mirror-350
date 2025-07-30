import instructor
from pydantic import BaseModel
from aiwriter.env import MODEL, WRITER_SYSTEM_PROMPT, CRITERIA


class Essay(BaseModel):
    title: str
    content: str

    def __str__(self):
        return f"Title: {self.title}\n\nContent:\n{self.content}"

WRITE = "Based on the above context, write a comprehensive essay that addresses the main points, provides supporting arguments, and concludes with a thoughtful summary."
REWRITE = "Based on the above context, rewrite the essay to improve the aspects of the criteria below. The rewritten essay should maintain the original meaning and intent while enhancing its overall quality."

def write_essay(
    context: str,
    length: int = 1000,
    style: str = "informal and analytical",
    audience: str = "sophisticated readers",
    rewrite: bool = False,
) -> Essay:
    """Given a context, length, style, and audience, this function generates an essay using an LLM.
    
    Args:
        context (str): The context for the essay.
        length (int): The length of the essay in words. Default is 1000.
        style (str): The style of the essay. Default is "informal and analytical".
        audience (str): The target audience for the essay. Default is "sophisticated readers".
        rewrite (bool): If True, the function will rewrite the essay instead of writing a new one. Default is False.
    """
    from typing import cast

    llm = instructor.from_provider(MODEL)

    prompt = (
        WRITER_SYSTEM_PROMPT.replace("{{context}}", context)
        .replace("{{length}}", str(length))
        .replace("{{style}}", style)
        .replace("{{audience}}", audience)
        .replace("{{criteria}}", ", ".join(CRITERIA))
        .replace("{{task}}", REWRITE if rewrite else WRITE)
    )
    return cast(
        Essay,
        llm.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            response_model=Essay,
        ),
    )

import instructor
from pydantic import BaseModel
from aiwriter.env import MODEL, THINKER_SYSTEM_PROMPT


class Insight(BaseModel):
    explanation: str
    insight: str

    def __str__(self):
        return f"Explanation: {self.explanation}\n\nInsight:\n{self.insight}"


class Insights(BaseModel):
    insights: list[Insight]

    def __iter__(self):
        return iter(self.insights)
    
    def __str__(self):
        return "\n\n".join([str(insight) for insight in self.insights])


def extract_insights(context: str):
    """Pass context to LLM and return insights from prompt."""
    from typing import cast

    llm = instructor.from_provider(MODEL)
    return cast(
        Insights,
        llm.chat.completions.create(
            messages=[
                {"role": "system", "content": THINKER_SYSTEM_PROMPT},
                {"role": "user", "content": context},
            ],
            response_model=Insights,
        ),
    )

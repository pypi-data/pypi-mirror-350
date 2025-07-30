import instructor
from pydantic import create_model, Field, ConfigDict, BaseModel
from aiwriter.env import MODEL, CRITERIA


class BaseScore(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


def rank_essay(essay: str):
    """This function takes an essay and returns a score based on the criteria."""
    from typing import cast, Any

    RANKER_PROMPT = (
        "Score the essay based on the following criteria: "
        + ", ".join(CRITERIA)
        + ".\n\nEach criteria should be scored from 0 to 10.\n\nEssay:\n\n"
    )

    criteria_dict = {key: Field(ge=0, le=10) for key in CRITERIA}
    ScoreModel = create_model("ScoreModel", __base__=BaseScore, **criteria_dict)
    llm = instructor.from_provider(MODEL)
    response = cast(
        Any,
        llm.chat.completions.create(
            messages=[{"role": "user", "content": RANKER_PROMPT + essay}],
            response_model=ScoreModel,
        ),
    )

    return response

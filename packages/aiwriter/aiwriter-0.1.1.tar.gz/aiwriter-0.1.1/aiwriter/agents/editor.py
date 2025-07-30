import os
from aiwriter.agents.context_builder import build_context
from aiwriter.agents.writer import write_essay
from aiwriter.agents.ranker import rank_essay
from aiwriter.agents.thinker import extract_insights
from aiwriter.env import DRAFTS_DIR

SCORE_THRESHOLD = 8


def all_scores_greater_than_threshold(scores, threshold=SCORE_THRESHOLD):
    return all(
        float(v) > threshold
        for v in scores.__dict__.values()
        if isinstance(v, (int, float))
    )


def agent_loop(
    prompt: str,
    max_iters: int = 6,
    length: int = 1000,
    style: str = "informal and analytical",
    audience: str = "sophisticated readers",
):
    os.makedirs(DRAFTS_DIR, exist_ok=True)
    scores = None
    FULL_CONTEXT = build_context()
    curr_context = prompt + '\n\nCONTEXT\n' + FULL_CONTEXT
    for i in range(1, max_iters + 1):
        essay = write_essay(
            str(curr_context),
            length=length,
            style=style,
            audience=audience,
            rewrite=i != 1,
            )
        curr_context = essay
        draft_path = f"{DRAFTS_DIR}/draft_{i}.md"
        with open(draft_path, "w") as f:
            f.write(str(essay))

        scores = rank_essay(str(essay))
        score_path = f"{DRAFTS_DIR}/draft_score_{i}.md"
        with open(score_path, "w") as f:
            f.write(str(scores))

        print(f"Draft #{i} - {curr_context.title}")
        print(f"Scores:\n\n{scores}")

        if all_scores_greater_than_threshold(scores, threshold=SCORE_THRESHOLD):
            print(f"All scores above {SCORE_THRESHOLD} at iteration {i}. Exiting loop.")
            break

        if i > 2:
            insights = extract_insights("SOURCE MATERIAL\n\n" + FULL_CONTEXT + "\n\n---\n\n ESSAY TO BE REWRITTEN\n\n" + str(curr_context) + "\n\n" + str(scores))
            insights_path = f"{DRAFTS_DIR}/draft_insights_{i}.md"
            with open(insights_path, "w") as f:
                f.write(str(insights))
            curr_context = "INSIGHTS\n\n" + str(insights) + "\n\n---\n\n ESSAY TO BE REWRITTEN\n\n" + str(curr_context)

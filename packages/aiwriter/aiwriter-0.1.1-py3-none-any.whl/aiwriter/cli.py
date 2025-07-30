import click
import sys

from aiwriter.agents.editor import agent_loop
from aiwriter.agents.writer import write_essay
from aiwriter.agents.ranker import rank_essay
from aiwriter.agents.context_builder import build_context
from aiwriter.agents.thinker import extract_insights


@click.group()
def main():
    """CLI for the AI Writer."""
    pass

length_option = click.option(
    "--length",
    default=1000,
    help="Length of the essay in words. Default is 1000.",
)
style_option = click.option(
    "--style",
    default="informal and analytical",
    help="Style of the essay. Default is 'informal and analytical'.",
)
audience_option = click.option(
    "--audience",
    default="sophisticated readers",
    help="Target audience for the essay. Default is 'sophisticated readers'.",
)
rewrite_option = click.option(
    "--rewrite",
    is_flag=True,
    help="If set, the essay will be rewritten instead of written from scratch.",
)

@main.command()
@click.option(
    "--context",
    default=sys.stdin,
    help="Context for the essay. Default is to read from stdin.",
)
@length_option
@style_option
@audience_option
@rewrite_option
def write(context, length, style, audience, rewrite):
    """Write an essay based on the given prompt."""
    essay = write_essay(context, length, style, audience, rewrite)
    click.echo(essay)


@main.command()
def build():
    """Build context from URLs file."""
    context = build_context()
    click.echo(context)


@main.command()
@click.argument("essay")
def rank(essay):
    """Rank an essay based on the given criteria."""
    scores = rank_essay(essay)
    click.echo(scores)


@main.command()
@click.argument("prompt")
def think(prompt):
    """Extract insights from the given prompt."""
    insights = extract_insights(prompt)
    click.echo(insights)


DEFAULT_MAX_ITERS = 6


@main.command()
@click.argument("prompt")
@click.option(
    "--max-iters",
    default=DEFAULT_MAX_ITERS,
    help=f"Maximum number of iterations for the agent loop. Default is {DEFAULT_MAX_ITERS}.",
)
@length_option
@style_option
@audience_option
def editor(prompt, max_iters, length, style, audience):
    """Run the agent loop for the given prompt."""
    agent_loop(prompt, max_iters, length, style, audience)
    click.echo(f"Agent loop completed for prompt")


if __name__ == "__main__":
    main()

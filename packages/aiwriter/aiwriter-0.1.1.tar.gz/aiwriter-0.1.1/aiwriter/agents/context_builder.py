import os
import requests
import subprocess
from bs4 import BeautifulSoup
from aiwriter.env import CONTEXT_FILE, CONTEXT_FULL_FILE, CONTEXT_DIR


def parse_url(url) -> str:
    """This function takes a URL and returns the contents of the page in Markdown.

    Dependencies: `requests`, `BeautifulSoup`, `pandoc`
    """

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.content, "html.parser")
    html = str(soup.prettify())
    md = pandoc_html2md(html)
    save_to_file(f"{url.split('/')[-1] or url.split('/')[-2]}.md", md)
    return md

def pandoc_html2md(html: str) -> str:
    """This function takes HTML content and converts it to Markdown using pandoc."""
    cmd = ['pandoc', '-s', '-f', 'html', '-t', 'markdown', '--wrap=none']
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    md, err = proc.communicate(input=html.encode())
    md = md.decode()
    if err:
        raise Exception(f"Error converting HTML to Markdown: {err.decode()}")
    return md


def save_to_file(filename, md):
    """This function saves the content to a file in the context directory
    if AIWRITER_CONTEXT_DIR env var is not set to empty."""
    if not CONTEXT_DIR:
        return
    os.makedirs(CONTEXT_DIR, exist_ok=True)
    filepath = os.path.join(CONTEXT_DIR, filename)
    open(filepath, "w").write(md)


def build_context():
    """This function takes a prompt, reads a "context" file containing URLs
    and builds the full context for the AI writer."""
    SEPARATOR = "\n\n------------\n------------\n\n"

    with open(CONTEXT_FILE, "r") as f:
        urls = f.readlines()
    urls = [url.strip() for url in urls if url.strip()]

    context = []
    for url in urls:
        try:
            context.append(parse_url(url))
        except Exception as e:
            print(f"Error parsing URL {url}: {e}")

    context = f"{SEPARATOR}".join(context)
    save_to_file(CONTEXT_FULL_FILE, context)

    return context + SEPARATOR

# Agentic AI Writer

The agentic writer will take in a **prompt**, a list of URLs (**context**), and a list of writing **criteria** (e.g. conciseness, accuracy).

It will first parse all the **context** URLs to markdown, and include them with the input **prompt**. It will generate a draft and score it according to the **criteria**.

This loop will repeat until the draft achieves a sufficiently high score in all criteria or until the max number of iterations is reached.

## Get started

``` sh
# 1. set ANTHROPIC_API_KEY
export ANTHROPIC_API_KEY="sk-ant-..." # the default model is anthropic's
# if using an openai model, use OPENAI_API_KEY, if using another provider, use "<PROVIDER_NAME>_API_KEY"

# 2. running agent loop
aiwriter editor "write an article on software engineering management extracting the absolute best insights from these articles. be concise."

# (optional) running simple essay writer
aiwriter write "write a short poem"

# (optional) add context URLs to be parsed and included in the prompt
echo "
blog.com/post1
blog.com/post2
blog.com/post3" > context.txt

# (optional) add criteria to favor in the agent's writing
echo "clarity,conciseness,relevance,engagement,accuracy" > criteria.txt  # this is the default criteria

# (optional) change the LLM model
export AIWRITER_MODEL="anthropic/claude-3-7-sonnet-latest"  # this is the default model
```

## API

### Environment Variables
Required:
- `ANTHROPIC_API_KEY` or another model provider API Key if default `AIWRITER_MODEL` is changed

Optional:
- `AIWRITER_MODEL` determines the model to be used
- `AIWRITER_CONTEXT_FILE` filename for input context urls file to be used in the first prompt
- `AIWRITER_CONTEXT_FULL_FILE` filename for output markdown context from parsing context urls
- `AIWRITER_CONTEXT_DIR` directory where input and output context files
- `AIWRITER_CRITERIA` filename for criteria file with comma-separated list of criteria to use when scoring
- `AIWRITER_DRAFTS_DIR` directory for agent outputs

cli/non-agent use only:
- `AIWRITER_ESSAY_FILE` filename for outputs from ranker and writer functions
- `AIWRITER_SCORES` filename for output scores file

### Modules
```sh
# AI Writer Agent
aiwriter editor "<prompt>"
aiwriter writer "<prompt>"
aiwriter ranker "<essay>"
aiwriter context_builder "<prompt>"
```

## How it works

### Data Model
- Input
  - URLs
  - Prompt *(i.e. topic)*
  - Criteria
- Output
  - Content *(i.e. scored drafts)*

### Data Flow
```mermaid
flowchart TD
    A([URLs]) --> B(Context Builder)
    AA([Topic]) --> B(Context Builder)
    B --> C([Prompt])
    B --> J(Thinker)
    C --> D(Writer)
    D --> E([Draft])
    E --> F(Ranker)
    F --> FF([Scored Draft])
    H([Criteria]) --> F
    FF --> G{Editor}
    I([Past Runs]) --> G
    G --> B
    G --> J
    J --> G

    style B fill:#fd0795,color:black,font-weight:bold
    style D fill:#00b5d7,color:black,font-weight:bold
    style F fill:#ff9000,color:black,font-weight:bold
    style G fill:#ffb901,color:black,font-weight:bold
    style J fill:#2a9d8f,color:black,font-weight:bold
```

### Modules
- **Context Builder**
  - prompt builder
  - url parser
    - html-to-markdown
    - audio-to-text (podcasts) <- future
    - youtube-to-text <- future
- **Writer**
- **Ranker**
- **Thinker**
- **Editor (Agent Loop)**

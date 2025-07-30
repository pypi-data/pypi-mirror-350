import mlflow

# Use double curly braces for variables in the template
initial_template = """\
Summarize content you are provided with in {{ num_sentences }} sentences.

Sentences: {{ sentences }}
"""

# Register a new prompt
prompt = mlflow.register_prompt(
    name="summarization-prompt",
    template=initial_template,
    # Optional: Provide a commit message to describe the changes
    commit_message="Initial commit",
    # Optional: Specify any additional metadata about the prompt version
    version_metadata={
        "author": "author@example.com",
    },
    # Optional: Set tags applies to the prompt (across versions)
    tags={
        "task": "summarization",
        "language": "en",
    },
)

# The prompt object contains information about the registered prompt
print(f"Created prompt '{prompt.name}' (version {prompt.version})")
import argparse
from .prompt_template import PromptTemplate
from .llm import HttpLLM, LLMType


parser = argparse.ArgumentParser(
    prog="prompt-as-method",
    description="Executes a method that is programmed as a prompt for a generative model"
)
parser.add_argument(
    "--prompt-template", type=str, required=True,
    help="Prompt template file (.json or .mustache; can be a URL) according to OpenAI chat completion API with variables"
    " enclosed in double curly braces (see mustache syntax)"
)
parser.add_argument(
    "--values", type=str, default=None,
    help="File with value assignment for template variables (variable names are column headers for .csv and .tsv files, and"
    " attribute names for .ndjson files; can be a URL), with the model being called separately for the values in each row of"
    " the file (except the header for .csv and .tsv)"
)
parser.add_argument(
    "--repetitions", type=int, default=1,
    help="How often each prompt (row in values file) should be repeated (default: 1)"
)
parser.add_argument(
    "--model-api", type=str, default="http://localhost:11434/v1/chat/completions",
    help="URL of the chat completion API endpoint (default is local Ollama server)"
)

opts = parser.parse_args()

prompt_template = PromptTemplate(template_file_name=opts.prompt_template)
prompts = prompt_template.render_from_file(opts.values) if opts.values is not None else [prompt_template.render()].__iter__()
llm = HttpLLM.init(LLMType.openai, opts.model_api)

for response in llm.generate_all(prompts, repetitions=opts.repetitions):
    print(response.model_dump_json())

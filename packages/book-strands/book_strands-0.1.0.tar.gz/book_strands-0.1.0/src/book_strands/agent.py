from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.models.ollama import OllamaModel
from strands.types.models import Model
from strands_tools import http_request

from .tools import read_ebook_metadata, write_ebook_metadata


def agent(
    input_files: list[str],
    output_path: str,
    output_format: str,
    query: str = "Perform the tasks as requested.",
    ollama_config: dict = {},
):
    system_prompt = f"""
        You are in charge of making sure ebooks are tagged with the correct metadata.
        Use tools to gather the information required and then write it to the provided output folder ("{output_path}").
        The expected format and path of the output files is: "{output_format}"
        The list of books to process is: {input_files}
        Note that all series indexes should be in the format 1.0, 2.0, 2.5 etc based on common practice.
        For author names, initials and formatting, use the same format whenever that author is mentioned.
        Check the output directory for existing books by the same author to match that formatting.
        """
    model: Model

    if ollama_config and ollama_config["use_ollama"]:
        model = OllamaModel(host=ollama_config["url"], model_id=ollama_config["model"])
    else:
        model = BedrockModel()

    a = Agent(
        system_prompt=system_prompt,
        model=model,
        tools=[read_ebook_metadata, write_ebook_metadata, http_request],
    )
    return a(query)

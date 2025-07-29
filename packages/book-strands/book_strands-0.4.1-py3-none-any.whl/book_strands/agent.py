import logging

from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.models.ollama import OllamaModel
from strands.types.models import Model
from strands_tools import http_request

from .tools import read_ebook_metadata, write_ebook_metadata

log = logging.getLogger(__name__)


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
        The book title should be purely the title of the book, without any extra information such as series or series index.
        The series name should not contain the word 'series'. If there is no series name, leave it blank.
        Note that all series indexes should be in the format 1.0, 2.0, 2.5 etc based on common practice.
        For author names, use "firstname lastname" ordering.
        Check the output directory for existing books by the same author to match that formatting.
        For the description of the book, it should be 100-200 words, usi a style that would typically be found on the back cover of a book and in html format.
        """
    model: Model

    if ollama_config and ollama_config["use_ollama"]:
        model = OllamaModel(host=ollama_config["url"], model_id=ollama_config["model"])
    else:
        # Nova pro seems to be accurate enough for this task, and is significantly cheaper and faster.
        model = BedrockModel(model_id="us.amazon.nova-pro-v1:0")
        INPUT_COST_PER_THOUSAND_TOKENS = 0.0008
        OUTPUT_COST_PER_THOUSAND_TOKENS = 0.0032

    a = Agent(
        system_prompt=system_prompt,
        model=model,
        tools=[read_ebook_metadata, write_ebook_metadata, http_request],
    )

    response = a(query)
    log.info(f"Accumulated token usage: {response.metrics.accumulated_usage}")

    if not ollama_config or not ollama_config["use_ollama"]:
        total_cost = (
            response.metrics.accumulated_usage["inputTokens"]
            / 1000
            * INPUT_COST_PER_THOUSAND_TOKENS
            + response.metrics.accumulated_usage["outputTokens"]
            / 1000
            * OUTPUT_COST_PER_THOUSAND_TOKENS
        )
        log.info(f"Total cost: US${total_cost:.3f}")

    return response

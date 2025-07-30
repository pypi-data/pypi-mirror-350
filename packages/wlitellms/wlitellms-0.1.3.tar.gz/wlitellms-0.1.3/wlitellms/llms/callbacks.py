import logging
from langchain_core.callbacks import StdOutCallbackHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DebugCallback(StdOutCallbackHandler):
    def on_tool_start(self, serialized, input_str, **kwargs):
        logger.info(
            f"------ Tool Call Started: {serialized.get('name')} with input: {input_str}"
        )

    def on_tool_end(self, output, **kwargs):
        logger.info(f"------ Tool Call Ended with output: {output}")

    def on_llm_start(self, serialized, prompts, **kwargs):
        logger.info(f"====== LLM Interaction Started with prompt: {prompts}")

    def on_llm_end(self, output, **kwargs):
        logger.info(f"====== LLM Interaction Ended with output: {output.generations}")

from typing import List
from ..helpers.llm_helper import LLMHelper
from .answering_tool_base import AnsweringToolBase
from ..common.answer import Answer

from logging import getLogger
from opentelemetry import trace, baggage
from opentelemetry.propagate import extract

logger = getLogger(__name__ + ".base_package")
tracer = trace.get_tracer(__name__ + ".base_package")


class TextProcessingTool(AnsweringToolBase):
    def __init__(self) -> None:
        self.name = "TextProcessing"

    def answer_question(self, question: str, chat_history: List[dict] = [], **kwargs):
        with tracer.start_as_current_span("TextProcessingTool.answer_question"):
            logger.info(f"Answering question: {question}")
            llm_helper = LLMHelper()
            text = kwargs.get("text")
            operation = kwargs.get("operation")
            user_content = (
                f"{operation} the following TEXT: {text}"
                if (text and operation)
                else question
            )

            system_message = """You are an AI assistant for the user."""

            try:
                result = llm_helper.get_chat_completion(
                    [
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_content},
                    ]
                )

                answer = Answer(
                    question=question,
                    answer=result.choices[0].message.content,
                    source_documents=[],
                    prompt_tokens=result.usage.prompt_tokens,
                    completion_tokens=result.usage.completion_tokens,
                )
                logger.info(f"Answer generated successfully.")
                return answer
            except Exception as e:
                logger.error(f"Error during get_chat_completion: {e}", exc_info=True)
                raise

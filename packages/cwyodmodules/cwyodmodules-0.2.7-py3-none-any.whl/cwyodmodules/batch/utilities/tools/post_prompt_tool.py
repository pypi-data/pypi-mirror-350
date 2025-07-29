from ..common.answer import Answer
from ..helpers.llm_helper import LLMHelper
from ..helpers.config.config_helper import ConfigHelper

from logging import getLogger
from opentelemetry import trace, baggage
from opentelemetry.propagate import extract

logger = getLogger(__name__ + ".base_package")
tracer = trace.get_tracer(__name__ + ".base_package")


class PostPromptTool:
    def __init__(self) -> None:
        pass

    def validate_answer(self, answer: Answer) -> Answer:
        with tracer.start_as_current_span("PostPromptTool.validate_answer") as span:
            logger.info("Validating answer using post-answering prompt.")
            config = ConfigHelper.get_active_config_or_default()
            llm_helper = LLMHelper()

            sources = "\n".join(
                [
                    f"[doc{i+1}]: {source.content}"
                    for i, source in enumerate(answer.source_documents)
                ]
            )

            message = config.prompts.post_answering_prompt.format(
                question=answer.question,
                answer=answer.answer,
                sources=sources,
            )

            logger.debug(f"Post-answering prompt message: {message}")
            span.set_attribute("prompt_message", message)

            response = llm_helper.get_chat_completion(
                [
                    {
                        "role": "user",
                        "content": message,
                    }
                ]
            )

            result = response.choices[0].message.content
            logger.debug(f"LLM response content: {result}")
            span.set_attribute("llm_response", result)

            was_message_filtered = result.lower() not in ["true", "yes"]
            logger.debug(f"Was message filtered: {was_message_filtered}")
            span.set_attribute("message_filtered", was_message_filtered)

            # Return filtered answer or just the original one
            if was_message_filtered:
                logger.info("Message was filtered; returning filtered answer.")
                return Answer(
                    question=answer.question,
                    answer=config.messages.post_answering_filter,
                    source_documents=[],
                    prompt_tokens=response.usage.prompt_tokens,
                    completion_tokens=response.usage.completion_tokens,
                )
            else:
                logger.info("Message was not filtered; returning original answer.")
                return Answer(
                    question=answer.question,
                    answer=answer.answer,
                    source_documents=answer.source_documents,
                    prompt_tokens=response.usage.prompt_tokens,
                    completion_tokens=response.usage.completion_tokens,
                )

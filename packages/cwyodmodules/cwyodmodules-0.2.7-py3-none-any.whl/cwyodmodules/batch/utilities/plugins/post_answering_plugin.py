from semantic_kernel.functions import kernel_function
from semantic_kernel.functions.kernel_arguments import KernelArguments

from ..common.answer import Answer
from ..tools.post_prompt_tool import PostPromptTool


class PostAnsweringPlugin:
    """
    A plugin class for post-answering operations, specifically designed to validate answers.

    Methods
    -------
    validate_answer(arguments: KernelArguments) -> Answer
        Executes a post-answering prompt to validate the provided answer.

    Validates the given answer using a post-answering prompt.

    Parameters
    ----------
    arguments : KernelArguments
        A dictionary containing the arguments required for validation. 
        It must include the key "answer" which holds the answer to be validated.

    Returns
    -------
    Answer
        The validated answer after running the post-answering prompt.
    """
    @kernel_function(description="Run post answering prompt to validate the answer.")
    def validate_answer(self, arguments: KernelArguments) -> Answer:
        return PostPromptTool().validate_answer(arguments["answer"])

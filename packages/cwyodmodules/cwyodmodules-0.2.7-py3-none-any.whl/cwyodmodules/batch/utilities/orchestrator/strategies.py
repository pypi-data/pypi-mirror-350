from .orchestration_strategy import OrchestrationStrategy
from .open_ai_functions import OpenAIFunctionsOrchestrator
from .lang_chain_agent import LangChainAgent
from .semantic_kernel_orchestrator import SemanticKernelOrchestrator
from .prompt_flow import PromptFlowOrchestrator

def get_orchestrator(orchestration_strategy: str):
    """
    Returns an instance of the appropriate orchestrator based on the provided orchestration strategy.

    Parameters:
    orchestration_strategy (str): The strategy to use for orchestration. This should be one of the values defined in the OrchestrationStrategy enum.

    Returns:
    object: An instance of the orchestrator class corresponding to the provided strategy.

    Raises:
    Exception: If the provided orchestration strategy does not match any known strategy.
    """
    if orchestration_strategy == OrchestrationStrategy.OPENAI_FUNCTION.value:
        return OpenAIFunctionsOrchestrator()
    elif orchestration_strategy == OrchestrationStrategy.LANGCHAIN.value:
        return LangChainAgent()
    elif orchestration_strategy == OrchestrationStrategy.SEMANTIC_KERNEL.value:
        return SemanticKernelOrchestrator()
    elif orchestration_strategy == OrchestrationStrategy.PROMPT_FLOW.value:
        return PromptFlowOrchestrator()
    else:
        raise Exception(f"Unknown orchestration strategy: {orchestration_strategy}")
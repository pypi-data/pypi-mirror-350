from enum import Enum

class OrchestrationStrategy(Enum):
    """
    OrchestrationStrategy is an enumeration that defines various strategies 
    for orchestrating tasks in the system. Each strategy represents a different 
    approach or framework for handling orchestration logic.
    
    Attributes:
        OPENAI_FUNCTION (str): Represents the strategy using OpenAI functions.
        LANGCHAIN (str): Represents the strategy using LangChain framework.
        SEMANTIC_KERNEL (str): Represents the strategy using Semantic Kernel.
        PROMPT_FLOW (str): Represents the strategy using Prompt Flow.
    """
    OPENAI_FUNCTION = "openai_function"
    LANGCHAIN = "langchain"
    SEMANTIC_KERNEL = "semantic_kernel"
    PROMPT_FLOW = "prompt_flow"
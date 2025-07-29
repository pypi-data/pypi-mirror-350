import json
import os
import logging

import threading
# from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from ..orchestrator.orchestration_strategy import OrchestrationStrategy
from ..helpers.config.conversation_flow import ConversationFlow
from ..helpers.config.database_type import DatabaseType
from ..helpers.secret_helper import SecretHelper

logger = logging.getLogger(__name__ + ".base_package")


class EnvHelper:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                instance = super(EnvHelper, cls).__new__(cls)
                instance.__load_config()
                cls._instance = instance
            return cls._instance

    def __load_config(self, **kwargs) -> None:
        # load_dotenv()

        logger.info("Initializing EnvHelper")

        # Wrapper for Azure Key Vault
        os.environ["APPLICATIONINSIGHTS_ENABLED"] = "true"

        self.secretHelper = SecretHelper(keyvault_uri=os.environ["key_vault_uri"])

        self.secretHelperHead = SecretHelper(
            keyvault_uri=os.environ["head_key_vault_uri"]
        )

        # self.secretHelper = SecretHelper(
        #     keyvault_uri="https://www.kv-main-cwyod-res1.vault.azure.net/"
        # )
        # self.secretHelperHead = SecretHelper(
        #     keyvault_uri="https://www.kv-main-cwyod-hd-res1.vault.azure.net/"
        # )

        self.LOGLEVEL = self.secretHelper.get_secret("logging-level")

        # Azure
        self.AZURE_SUBSCRIPTION_ID = self.secretHelper.get_secret("subscription-id")
        self.AZURE_RESOURCE_GROUP = self.secretHelper.get_secret("resource-group-name")
        self.AZURE_HEAD_RESOURCE_GROUP = self.secretHelperHead.get_secret(
            "resource-group-name"
        )
        self.AZURE_RESOURCE_ENVIRONMENT = self.secretHelper.get_secret(
            "resource-group-environment"
        )
        self.AZURE_RESOURCE_PRIVATE = (
            self.secretHelper.get_secret("kv-run-private-endpoint").lower() == "true"
        )
        self.PROJECT_CODE = self.secretHelper.get_secret("project-code")
        self.APP_NAME = os.getenv("REFLECTION_NAME", "Default")
        self.POSTGRESQL_NAME = (
            f"psql-main-{self.PROJECT_CODE}-{self.AZURE_RESOURCE_ENVIRONMENT}"
        )
        self.AZURE_AUTH_TYPE = self.secretHelper.get_secret("auth-type")
        self.AZURE_TOKEN_PROVIDER = get_bearer_token_provider(
            DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
        )
        self.AZURE_BLOB_ACCOUNT_NAME = (
            f"stqueue{self.PROJECT_CODE}{self.AZURE_RESOURCE_ENVIRONMENT}"
        )
        self.AZURE_STORAGE_ACCOUNT_ENDPOINT = (
            f"https://{self.AZURE_BLOB_ACCOUNT_NAME}.blob.core.windows.net/"
        )

        self.AZURE_FUNCTION_APP_ENDPOINT = self.secretHelper.get_secret(
            f"func-backend-{self.PROJECT_CODE}-{self.AZURE_RESOURCE_ENVIRONMENT}-endpoint"
        )
        self.AZURE_BLOB_CONTAINER_NAME = self.secretHelper.get_secret(
            "documents-blob-name"
        )
        self.DOCUMENT_PROCESSING_QUEUE_NAME = self.secretHelper.get_secret(
            "documents-queue-name"
        )

        # PostgreSQL configuration
        self.DATABASE_TYPE = self.secretHelper.get_secret("database-type")
        # Chat History DB Integration Settings
        # Set default values based on DATABASE_TYPE

        # Cosmos DB configuration
        if self.DATABASE_TYPE == DatabaseType.COSMOSDB.value:
            azure_cosmosdb_info = self.get_info_from_env("AZURE_COSMOSDB_INFO", "")
            if azure_cosmosdb_info:
                self.AZURE_COSMOSDB_DATABASE = azure_cosmosdb_info.get(
                    "databaseName", ""
                )
                self.AZURE_COSMOSDB_ACCOUNT = azure_cosmosdb_info.get("accountName", "")
                self.AZURE_COSMOSDB_CONVERSATIONS_CONTAINER = azure_cosmosdb_info.get(
                    "containerName", ""
                )
            else:
                self.AZURE_COSMOSDB_DATABASE = os.getenv(
                    "AZURE_COSMOSDB_DATABASE_NAME", ""
                )
                self.AZURE_COSMOSDB_ACCOUNT = os.getenv(
                    "AZURE_COSMOSDB_ACCOUNT_NAME", ""
                )
                self.AZURE_COSMOSDB_CONVERSATIONS_CONTAINER = os.getenv(
                    "AZURE_COSMOSDB_CONVERSATIONS_CONTAINER_NAME", ""
                )
            self.AZURE_COSMOSDB_ACCOUNT_KEY = self.secretHelper.get_secret(
                "AZURE_COSMOSDB_ACCOUNT_KEY"
            )
            self.AZURE_COSMOSDB_ENABLE_FEEDBACK = (
                os.getenv("AZURE_COSMOSDB_ENABLE_FEEDBACK", "false").lower() == "true"
            )
            self.AZURE_SEARCH_USE_INTEGRATED_VECTORIZATION = self.get_env_var_bool(
                "AZURE_SEARCH_USE_INTEGRATED_VECTORIZATION", "False"
            )
            self.USE_ADVANCED_IMAGE_PROCESSING = self.get_env_var_bool(
                "USE_ADVANCED_IMAGE_PROCESSING", "False"
            )
            self.CONVERSATION_FLOW = os.getenv("CONVERSATION_FLOW", "custom")
            # Orchestration Settings
            self.ORCHESTRATION_STRATEGY = os.getenv(
                "ORCHESTRATION_STRATEGY", "openai_function"
            )
        # PostgreSQL configuration
        elif self.DATABASE_TYPE == DatabaseType.POSTGRESQL.value:
            self.AZURE_POSTGRES_SEARCH_TOP_K = 5
            azure_postgresql_info = self.get_info_from_env("AZURE_POSTGRESQL_INFO", "")
            if azure_postgresql_info:
                self.POSTGRESQL_USER = azure_postgresql_info.get("user", "")
                self.POSTGRESQL_DATABASE = azure_postgresql_info.get("dbname", "")
                self.POSTGRESQL_HOST = azure_postgresql_info.get("host", "")
            else:
                self.POSTGRESQL_USER = "cwyod_project_uai"
                self.POSTGRESQL_DATABASE = self.secretHelper.get_secret(
                    f"{self.POSTGRESQL_NAME}-default-database-name"
                )
                self.POSTGRESQL_HOST = self.secretHelper.get_secret(
                    f"{self.POSTGRESQL_NAME}-server-name"
                )
            # Ensure integrated vectorization is disabled for PostgreSQL
            self.AZURE_SEARCH_USE_INTEGRATED_VECTORIZATION = False
            self.USE_ADVANCED_IMAGE_PROCESSING = False
            self.CONVERSATION_FLOW = ConversationFlow.CUSTOM.value
            self.ORCHESTRATION_STRATEGY = OrchestrationStrategy.SEMANTIC_KERNEL.value
        else:
            raise ValueError(
                "Unsupported DATABASE_TYPE. Please set DATABASE_TYPE to 'CosmosDB' or 'PostgreSQL'."
            )

        # Azure OpenAI
        self.AZURE_OPENAI_MODEL = "gpt-4o-default"
        self.AZURE_OPENAI_MODEL_NAME = self.AZURE_OPENAI_MODEL
        self.AZURE_OPENAI_VISION_MODEL = "gpt-4"
        self.AZURE_OPENAI_TEMPERATURE = "0"
        self.AZURE_OPENAI_TOP_P = "1.0"
        self.AZURE_OPENAI_MAX_TOKENS = "1000"
        self.AZURE_OPENAI_STOP_SEQUENCE = ""
        self.AZURE_OPENAI_SYSTEM_MESSAGE = (
            "You are an AI assistant that helps people find information."
        )
        self.AZURE_OPENAI_API_VERSION = "2024-02-01"
        self.AZURE_OPENAI_STREAM = "true"
        self.AZURE_OPENAI_EMBEDDING_MODEL = "text-embedding-ada-002"

        self.SHOULD_STREAM = (
            True if self.AZURE_OPENAI_STREAM.lower() == "true" else False
        )

        # self.AZURE_COMPUTER_VISION_NAME = self.secretHelperHead.get_secret(
        #     "cognitive-kind-ComputerVision"
        # )
        self.AZURE_COMPUTER_VISION_NAME = ""
        # self.AZURE_COMPUTER_VISION_ENDPOINT = self.secretHelperHead.get_secret(
        #     f"{self.AZURE_COMPUTER_VISION_NAME}-endpoint"
        # )
        self.AZURE_COMPUTER_VISION_ENDPOINT = ""
        self.ADVANCED_IMAGE_PROCESSING_MAX_IMAGES = 1
        self.AZURE_COMPUTER_VISION_TIMEOUT = 30
        self.AZURE_COMPUTER_VISION_VECTORIZE_IMAGE_API_VERSION = "2024-02-01"
        self.AZURE_COMPUTER_VISION_VECTORIZE_IMAGE_MODEL_VERSION = "2023-04-15"

        # Initialize Azure keys based on authentication type and environment settings.
        # When AZURE_AUTH_TYPE is "rbac", azure keys are None or an empty string.
        if self.AZURE_AUTH_TYPE == "rbac":
            self.AZURE_SEARCH_KEY = None
            self.AZURE_OPENAI_API_KEY = ""
            self.AZURE_COMPUTER_VISION_KEY = None
        else:
            self.AZURE_SEARCH_KEY = self.secretHelper.get_secret("AZURE_SEARCH_KEY")
            self.AZURE_OPENAI_API_KEY = self.secretHelper.get_secret(
                "AZURE_OPENAI_API_KEY"
            )
            self.AZURE_COMPUTER_VISION_KEY = self.secretHelper.get_secret(
                "AZURE_COMPUTER_VISION_KEY"
            )

        # Set env for Azure OpenAI
        self.AZURE_AI_SERVICES_NAME = self.secretHelperHead.get_secret(
            "cognitive-kind-AIServices"
        )
        self.AZURE_OPENAI_ENDPOINT = (
            f"https://{self.AZURE_AI_SERVICES_NAME}.openai.azure.com/"
        )

        # Set env for OpenAI SDK
        self.OPENAI_API_TYPE = "azure" if self.AZURE_AUTH_TYPE == "keys" else "azure_ad"
        self.OPENAI_API_KEY = self.AZURE_OPENAI_API_KEY
        self.OPENAI_API_VERSION = self.AZURE_OPENAI_API_VERSION
        os.environ["OPENAI_API_TYPE"] = self.OPENAI_API_TYPE
        os.environ["OPENAI_API_KEY"] = self.OPENAI_API_KEY
        os.environ["OPENAI_API_VERSION"] = self.OPENAI_API_VERSION
        # Azure Functions - Batch processing
        self.BACKEND_URL = self.AZURE_FUNCTION_APP_ENDPOINT
        self.FUNCTION_KEY = None

        # Azure Form Recognizer

        self.AZURE_FORM_RECOGNIZER_NAME = self.secretHelper.get_secret(
            "cognitive-kind-FormRecognizer"
        )
        self.AZURE_FORM_RECOGNIZER_ENDPOINT = self.secretHelper.get_secret(
            f"{self.AZURE_FORM_RECOGNIZER_NAME}-endpoint"
        )

        # Azure App Insights
        # APPLICATIONINSIGHTS_ENABLED will be True when the application runs in App Service
        self.APPLICATIONINSIGHTS_ENABLED = "True"

        # Azure AI Content Safety
        self.AZURE_CONTENT_SAFETY_NAME = self.secretHelperHead.get_secret(
            "cognitive-kind-ContentSafety"
        )
        self.AZURE_CONTENT_SAFETY_ENDPOINT = self.secretHelperHead.get_secret(
            f"{self.AZURE_CONTENT_SAFETY_NAME}-endpoint"
        )

        # Speech Service
        self.AZURE_SPEECH_SERVICE_NAME = self.secretHelperHead.get_secret(
            "cognitive-kind-SpeechServices"
        )
        self.AZURE_SPEECH_ENDPOINT = self.secretHelperHead.get_secret(
            f"{self.AZURE_SPEECH_SERVICE_NAME}-endpoint"
        )

        self.AZURE_SPEECH_SERVICE_REGION = "westeurope"
        self.AZURE_SPEECH_RECOGNIZER_LANGUAGES = "en-US"
        self.AZURE_SPEECH_REGION_ENDPOINT = (
            f"https://{self.AZURE_SPEECH_SERVICE_REGION}.api.cognitive.microsoft.com/"
        )
        self.AZURE_SPEECH_KEY = self.secretHelperHead.get_secret(f"{self.AZURE_SPEECH_SERVICE_NAME}-key") # changed from None to allow private endpoint communication

        self.LOAD_CONFIG_FROM_BLOB_STORAGE = self.get_env_var_bool(
            "LOAD_CONFIG_FROM_BLOB_STORAGE"
        )
        # Azure Search
        self.AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE", "")
        self.AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX", "")
        self.AZURE_SEARCH_USE_SEMANTIC_SEARCH = "True"
        self.AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG = os.getenv(
            "AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG", "default"
        )
        self.AZURE_SEARCH_INDEX_IS_PRECHUNKED = os.getenv(
            "AZURE_SEARCH_INDEX_IS_PRECHUNKED", ""
        )
        self.AZURE_SEARCH_FILTER = os.getenv("AZURE_SEARCH_FILTER", "")
        self.AZURE_SEARCH_TOP_K = self.get_env_var_int("AZURE_SEARCH_TOP_K", 5)
        self.AZURE_SEARCH_ENABLE_IN_DOMAIN = (
            os.getenv("AZURE_SEARCH_ENABLE_IN_DOMAIN", "true").lower() == "true"
        )
        self.AZURE_SEARCH_FIELDS_ID = os.getenv("AZURE_SEARCH_FIELDS_ID", "id")
        self.AZURE_SEARCH_CONTENT_COLUMN = os.getenv(
            "AZURE_SEARCH_CONTENT_COLUMN", "content"
        )
        self.AZURE_SEARCH_CONTENT_VECTOR_COLUMN = os.getenv(
            "AZURE_SEARCH_CONTENT_VECTOR_COLUMN", "content_vector"
        )
        self.AZURE_SEARCH_DIMENSIONS = os.getenv("AZURE_SEARCH_DIMENSIONS", "1536")
        self.AZURE_SEARCH_FILENAME_COLUMN = os.getenv(
            "AZURE_SEARCH_FILENAME_COLUMN", "filepath"
        )
        self.AZURE_SEARCH_TITLE_COLUMN = os.getenv("AZURE_SEARCH_TITLE_COLUMN", "title")
        self.AZURE_SEARCH_URL_COLUMN = os.getenv("AZURE_SEARCH_URL_COLUMN", "url")
        self.AZURE_SEARCH_FIELDS_TAG = os.getenv("AZURE_SEARCH_FIELDS_TAG", "tag")
        self.AZURE_SEARCH_FIELDS_METADATA = os.getenv(
            "AZURE_SEARCH_FIELDS_METADATA", "metadata"
        )
        self.AZURE_SEARCH_SOURCE_COLUMN = os.getenv(
            "AZURE_SEARCH_SOURCE_COLUMN", "source"
        )
        self.AZURE_SEARCH_CHUNK_COLUMN = os.getenv("AZURE_SEARCH_CHUNK_COLUMN", "chunk")
        self.AZURE_SEARCH_OFFSET_COLUMN = os.getenv(
            "AZURE_SEARCH_OFFSET_COLUMN", "offset"
        )
        self.AZURE_SEARCH_CONVERSATIONS_LOG_INDEX = os.getenv(
            "AZURE_SEARCH_CONVERSATIONS_LOG_INDEX", "conversations"
        )
        self.AZURE_SEARCH_DOC_UPLOAD_BATCH_SIZE = os.getenv(
            "AZURE_SEARCH_DOC_UPLOAD_BATCH_SIZE", 100
        )
        # Integrated Vectorization
        self.AZURE_SEARCH_DATASOURCE_NAME = os.getenv(
            "AZURE_SEARCH_DATASOURCE_NAME", ""
        )
        self.AZURE_SEARCH_INDEXER_NAME = os.getenv("AZURE_SEARCH_INDEXER_NAME", "")

        self.AZURE_ML_WORKSPACE_NAME = ""

        self.PROMPT_FLOW_ENDPOINT_NAME = ""

        self.PROMPT_FLOW_DEPLOYMENT_NAME = ""

        self.OPEN_AI_FUNCTIONS_SYSTEM_PROMPT = ""
        self.SEMENTIC_KERNEL_SYSTEM_PROMPT = ""

        logger.info("Initializing EnvHelper completed")

    def is_chat_model(self):
        if "gpt-4" in self.AZURE_OPENAI_MODEL_NAME.lower():
            return True
        return False

    def get_env_var_bool(self, var_name: str, default: str = "True") -> bool:
        return os.getenv(var_name, default).lower() == "true"

    def get_env_var_array(self, var_name: str, default: str = ""):
        return os.getenv(var_name, default).split(",")

    def get_env_var_int(self, var_name: str, default: int):
        return int(os.getenv(var_name, default))

    def get_env_var_float(self, var_name: str, default: float):
        return float(os.getenv(var_name, default))

    def is_auth_type_keys(self):
        return self.AZURE_AUTH_TYPE == "keys"

    def get_info_from_env(self, env_var: str, default_info: str) -> dict:
        # Fetch and parse model info from the environment variable.
        info_str = os.getenv(env_var, default_info)
        # Handle escaped characters in the JSON string by wrapping it in double quotes for parsing.
        if "\\" in info_str:
            info_str = json.loads(f'"{info_str}"')
        return {} if not info_str else json.loads(info_str)

    @staticmethod
    def check_env():
        for attr, value in EnvHelper().__dict__.items():
            if value == "":
                logger.warning(f"{attr} is not set in the environment variables.")

    @classmethod
    def clear_instance(cls):
        if cls._instance is not None:
            cls._instance = None

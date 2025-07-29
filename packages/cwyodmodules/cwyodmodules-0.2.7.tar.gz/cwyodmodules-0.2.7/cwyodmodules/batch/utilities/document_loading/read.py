from typing import List
from .document_loading_base import DocumentLoadingBase
from ..helpers.azure_form_recognizer_helper import AzureFormRecognizerClient
from ..common.source_document import SourceDocument

from logging import getLogger
from opentelemetry import trace, baggage
from opentelemetry.propagate import extract

logger = getLogger(__name__ + ".base_package")
tracer = trace.get_tracer(__name__ + ".base_package")


class ReadDocumentLoading(DocumentLoadingBase):
    def __init__(self) -> None:
        super().__init__()

    def load(self, document_url: str) -> List[SourceDocument]:
        with tracer.start_as_current_span("ReadDocumentLoading.load") as span:
            logger.info(f"Loading document from URL: {document_url}")
            try:
                azure_form_recognizer_client = AzureFormRecognizerClient()
                pages_content = (
                    azure_form_recognizer_client.begin_analyze_document_from_url(
                        document_url, use_layout=False
                    )
                )
                documents = [
                    SourceDocument(
                        content=page["page_text"],
                        source=document_url,
                        page_number=page["page_number"],
                        offset=page["offset"],
                    )
                    for page in pages_content
                ]
                logger.info(
                    f"Successfully loaded {len(documents)} pages from {document_url}"
                )
                return documents
            except Exception as e:
                logger.error(
                    f"Error loading document from {document_url}: {e}", exc_info=True
                )
                span.record_exception(e)
                raise

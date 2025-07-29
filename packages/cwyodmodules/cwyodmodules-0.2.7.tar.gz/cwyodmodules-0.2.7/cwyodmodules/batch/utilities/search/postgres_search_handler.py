import json
from typing import List
import numpy as np

from .search_handler_base import SearchHandlerBase
from ..helpers.azure_postgres_helper import AzurePostgresHelper
from ..common.source_document import SourceDocument

from logging import getLogger
from opentelemetry import trace, baggage
from opentelemetry.propagate import extract


class AzurePostgresHandler(SearchHandlerBase):

    def __init__(self, env_helper):
        self.azure_postgres_helper = AzurePostgresHelper()
        self.logger = getLogger(__name__ + ".base_package")
        self.tracer = trace.get_tracer(__name__ + ".base_package")
        super().__init__(env_helper)

    def query_search(self, question) -> List[SourceDocument]:
        with self.tracer.start_as_current_span("query_search"):
            self.logger.info(f"Starting query search for question: {question}")
            user_input = question
            query_embedding = self.azure_postgres_helper.llm_helper.generate_embeddings(
                user_input
            )

            embedding_array = np.array(query_embedding).tolist()

            search_results = self.azure_postgres_helper.get_vector_store(
                embedding_array
            )

            source_documents = self._convert_to_source_documents(search_results)
            self.logger.info(f"Found {len(source_documents)} source documents.")
            return source_documents

    def _convert_to_source_documents(self, search_results) -> List[SourceDocument]:
        with self.tracer.start_as_current_span("_convert_to_source_documents"):
            source_documents = []
            for source in search_results:
                source_document = SourceDocument(
                    id=source["id"],
                    title=source["title"],
                    chunk=source["chunk"],
                    offset=source["offset"],
                    page_number=source["page_number"],
                    content=source["content"],
                    source=source["source"],
                )
                source_documents.append(source_document)
            return source_documents

    def create_search_client(self):
        with self.tracer.start_as_current_span("create_search_client"):
            return self.azure_postgres_helper.get_search_client()

    def create_vector_store(self, documents_to_upload):
        with self.tracer.start_as_current_span("create_vector_store"):
            self.logger.info(
                f"Creating vector store with {len(documents_to_upload)} documents."
            )
            return self.azure_postgres_helper.create_vector_store(documents_to_upload)

    def perform_search(self, filename):
        with self.tracer.start_as_current_span("perform_search"):
            self.logger.info(f"Performing search for filename: {filename}")
            return self.azure_postgres_helper.perform_search(filename)

    def process_results(self, results):
        with self.tracer.start_as_current_span("process_results"):
            if results is None:
                self.logger.info("No results to process.")
                return []
            data = [
                [json.loads(result["metadata"]).get("chunk", i), result["content"]]
                for i, result in enumerate(results)
            ]
            self.logger.info(f"Processed {len(data)} results.")
            return data

    def get_files(self):
        with self.tracer.start_as_current_span("get_files"):
            results = self.azure_postgres_helper.get_files()
            if results is None or len(results) == 0:
                self.logger.info("No files found.")
                return []
            self.logger.info(f"Found {len(results)} files.")
            return results

    def output_results(self, results):
        with self.tracer.start_as_current_span("output_results"):
            files = {}
            for result in results:
                id = result["id"]
                filename = result["title"]
                if filename in files:
                    files[filename].append(id)
                else:
                    files[filename] = [id]

            return files

    def delete_files(self, files):
        with self.tracer.start_as_current_span("delete_files"):
            ids_to_delete = []
            files_to_delete = []

            for filename, ids in files.items():
                files_to_delete.append(filename)
                ids_to_delete += [{"id": id} for id in ids]
            self.azure_postgres_helper.delete_documents(ids_to_delete)

            return ", ".join(files_to_delete)

    def search_by_blob_url(self, blob_url):
        with self.tracer.start_as_current_span("search_by_blob_url"):
            self.logger.info(f"Searching by blob URL: {blob_url}")
            return self.azure_postgres_helper.search_by_blob_url(blob_url)

    def delete_from_index(self, blob_url) -> None:
        with self.tracer.start_as_current_span("delete_from_index"):
            self.logger.info(f"Deleting from index for blob URL: {blob_url}")
            documents = self.search_by_blob_url(blob_url)
            if documents is None or len(documents) == 0:
                self.logger.info("No documents found for blob URL.")
                return
            files_to_delete = self.output_results(documents)
            self.delete_files(files_to_delete)

    def get_unique_files(self):
        with self.tracer.start_as_current_span("get_unique_files"):
            results = self.azure_postgres_helper.get_unique_files()
            unique_titles = [row["title"] for row in results]
            return unique_titles

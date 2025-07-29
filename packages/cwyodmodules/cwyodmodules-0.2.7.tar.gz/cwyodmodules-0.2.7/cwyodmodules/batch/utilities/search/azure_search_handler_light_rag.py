import logging
from typing import List
from ..helpers.lightrag_helper import LightRAGHelper
from .search_handler_base import SearchHandlerBase
from ..common.source_document import SourceDocument
import json

logger = logging.getLogger(__name__ + ".base_package")


class AzureSearchHandlerLightRag(SearchHandlerBase):
    def __init__(self, env_helper):
        super().__init__(env_helper)
        self.light_rag_helper = LightRAGHelper(env_helper)

    def create_search_client(self):
        return self.light_rag_helper.get_search_client()

    def perform_search(self, filename):
        return self.light_rag_helper.search(
            "*", select="title, content, metadata", filter=f"title eq '{filename}'"
        )

    def process_results(self, results):
        logger.info("Processing search results")
        if results is None:
            logger.warning("No results found")
            return []
        data = [
            [json.loads(result["metadata"]).get("chunk", i), result["content"]]
            for i, result in enumerate(results)
        ]
        logger.info("Processed results")
        return data

    def get_files(self):
        return self.light_rag_helper.get_files()

    def output_results(self, results):
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
        ids_to_delete = []
        files_to_delete = []

        for filename, ids in files.items():
            files_to_delete.append(filename)
            ids_to_delete += [{"id": id} for id in ids]
        self.light_rag_helper.delete_documents(ids_to_delete)

        return ", ".join(files_to_delete)

    def search_by_blob_url(self, blob_url):
        return self.light_rag_helper.search_by_blob_url(blob_url)

    def query_search(self, question) -> List[SourceDocument]:
        logger.info(f"Performing query search for question: {question}")
        results = self.light_rag_helper.query_search(question)
        logger.info("Converting search results to SourceDocument list")
        return self._convert_to_source_documents(results)

    def _convert_to_source_documents(self, search_results) -> List[SourceDocument]:
        source_documents = []
        for source in search_results:
            source_documents.append(
                SourceDocument(
                    id=source.get("id"),
                    content=source.get("content"),
                    title=source.get("title"),
                    source=source.get("source"),
                    chunk=source.get("chunk"),
                    offset=source.get("offset"),
                    page_number=source.get("page_number"),
                )
            )
        return source_documents
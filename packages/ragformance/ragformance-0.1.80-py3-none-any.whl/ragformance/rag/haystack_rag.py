from typing import Dict, List
import requests
import json

from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import EmbeddingRetriever, FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from haystack.schema import Document
from sentence_transformers import SentenceTransformer

from ragformance.rag.rag_interface import RagInterface
from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel, AnswerModel

class OllamaLLMReader:
    def __init__(self, base_url: str, model: str, temperature: float = 0.2, max_tokens: int = 3000):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def predict(self, query: str, context: str) -> str:
        payload = {
            "model": self.model,
            "prompt": f"Question: {query}\nContext: {context}\nAnswer:",
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": True
        }

        response = requests.post(f"{self.base_url}/api/generate", json=payload, stream=True)

        if response.status_code != 200:
            raise RuntimeError(f"Ollama API error: {response.status_code} {response.text}")

        output = ""
        for line in response.iter_lines():
            if not line:
                continue
            try:
                data = line.decode("utf-8")
                chunk = json.loads(data)
                output += chunk.get("response", "")
            except Exception as e:
                raise RuntimeError(f"Failed to parse Ollama output: {e}")

        return output.strip()

class HaystackRAG(RagInterface):
    def __init__(
        self,
        embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        ollama_model: str = None,
        ollama_url: str = None,
    ) -> None:
        self.embedding_model = SentenceTransformer(embedding_model_name)#("all-MiniLM-L6-v2")
        dummy_vector = self.embedding_model.encode(["dummy"])[0]
        embedding_dim = len(dummy_vector)
        self.document_store = InMemoryDocumentStore(use_bm25=False, embedding_dim=embedding_dim)
        self.retriever = EmbeddingRetriever(
            document_store=self.document_store,
            embedding_model=embedding_model_name,
            use_gpu=False
        )
        if ollama_model and ollama_url:
            self.reader = OllamaLLMReader(
                base_url=ollama_url,
                model=ollama_model
            )
            self.use_ollama = True
        else:
            self.reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False)
            self.pipeline = ExtractiveQAPipeline(reader=self.reader, retriever=self.retriever)
            self.use_ollama = False

    def upload_corpus(self, corpus: List[DocModel]) -> int:
        documents = [
            Document(
                content=doc.text,
                meta={"corpus_id": doc.id, "title": doc.title, **(doc.metadata or {})}
            )
            for doc in corpus
        ]
        self.document_store.write_documents(documents)
        self.document_store.update_embeddings(self.retriever)
        return len(documents)

    def ask_queries(self, queries: List[AnnotatedQueryModel], config: Dict = {}) -> List[AnswerModel]:
        results = []
        for query in queries:
            retrieved_docs = self.retriever.retrieve(query.query_text, top_k=3)

            if self.use_ollama:
                context = "\n".join([doc.content for doc in retrieved_docs])
                answer_text = self.reader.predict(query.query_text, context)

                doc_ids = [doc.meta.get("corpus_id") for doc in retrieved_docs]
                scores = [doc.score for doc in retrieved_docs]

            else:
                prediction = self.pipeline.run(
                    query=query.query_text,
                    params={"Retriever": {"top_k": 3}, "Reader": {"top_k": 1}}
                )

                answers = prediction.get("answers", [])
                documents = prediction.get("documents", [])
                answer_text = answers[0].answer if answers else ""

                doc_ids = [doc.meta.get("corpus_id") for doc in documents]
                scores = [doc.score for doc in documents]

            results.append(AnswerModel(
                _id=query.id,
                query=query,
                model_answer=answer_text,
                retrieved_documents_ids=doc_ids,
                retrieved_documents_distances=scores
            ))

        return results

from typing import Dict, List
import uuid
import requests

try:
    from sentence_transformers import SentenceTransformer
except ImportError:

    def SentenceTransformer(*args, **kwargs):
        raise ImportError(
            "'sentence-transformers' module is not installed. "
            "Please install ragformance with the [all] option:\n"
            "    pip install ragformance[all]"
        )


import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json

import logging

from ragformance.models.answer import AnnotatedQueryModel, AnswerModel
from ragformance.models.corpus import DocModel
from ragformance.rag.rag_interface import RagInterface

logger = logging.getLogger(__name__)

# Initialize embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# In-memory storage for document embeddings
document_embeddings = []
documents: List[DocModel] = []


class NaiveRag(RagInterface):
    def upload_corpus(self, corpus: List[DocModel], config: Dict = {}):
        document_embeddings.clear()
        documents.clear()
        documents.extend(corpus)

        # Look in the config file for the key of the dataframe where the text is stored
        batch_size = config.get("batch_size", 32)

        # Extract texts from the corpus list
        texts = [doc.text for doc in corpus]

        # Process documents in batches
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i : i + batch_size]

            # Generate embeddings for the batch
            batch_embeddings = embedding_model.encode(batch_texts)

            # Store embeddings
            document_embeddings.extend(batch_embeddings)

        logger.info(
            f"Document embeddings generated and stored in memory. {len(document_embeddings)} embeddings generated."
        )
        return len(document_embeddings)

    def ask_queries(
        self, queries: List[AnnotatedQueryModel], config: Dict = {}
    ) -> List[AnswerModel]:
        threshold = config.get("similarity_threshold", 0.5)

        batch_size = config.get("batch_size", 32)

        url = config.get("LLM_endpoint", "https://localhost:8000/v1/chat/completions")
        key = config.get("LLM_key", None)
        model = config.get("LLM_model", None)
        if url is None or key is None or model is None:
            logger.warning(
                "LLM endpoint, key or model not provided. Skipping LLM call."
            )

        # Generate embedding for the question
        # Extract texts from the corpus list
        texts = [query.query_text for query in queries]

        query_embeddings = []

        # Process documents in batches
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i : i + batch_size]

            # Generate embeddings for the batch
            batch_embeddings = embedding_model.encode(batch_texts)

            # Store embeddings
            query_embeddings.extend(batch_embeddings)

        answers = []

        for qindex, query in enumerate(queries):
            question = query.query_text
            question_embedding = query_embeddings[qindex]

            # Ensure question_embedding is a 2D array
            question_embedding = np.array([question_embedding])
            if question_embedding.ndim == 1:
                question_embedding = question_embedding.reshape(1, -1)

            # Ensure document_embeddings is a 2D array
            document_embeddings_array = np.array(document_embeddings)
            if document_embeddings_array.ndim == 1:
                document_embeddings_array = document_embeddings_array.reshape(1, -1)

            similarities = cosine_similarity(
                question_embedding, document_embeddings_array
            )
            relevant_documents = np.where(similarities > threshold)[1]

            logger.info(
                f"Query {qindex} : Found {len(relevant_documents)} relevant documents."
            )

            # Prepare the payload for the LLM API

            prompt_and_query = f"Answer the question based on the context below : \n QUESTION: {question}\n"
            for index, id in enumerate(relevant_documents):
                document: DocModel = documents[id]
                text = document.text
                prompt_and_query += f"CONTEXT {index + 1}: {text}\n"
            prompt_and_query += "ANSWER:"

            if url is None or key is None or model is None:
                answer = AnswerModel.model_validate(
                    {
                        "_id": str(uuid.uuid4()),
                        "query": query,
                        "model_answer": "",  # no answer because no LLM
                        "retrieved_documents_ids": [
                            documents[i].id for i in relevant_documents
                        ],
                    }
                )
                answers.append(answer)
            else:
                response = requests.post(
                    url=url,
                    headers={
                        "Authorization": "Bearer " + key,
                    },
                    data=json.dumps(
                        {
                            "model": model,
                            "messages": [{"role": "user", "content": prompt_and_query}],
                        }
                    ),
                )

                response_json = response.json()
                response_json = response_json["choices"][0]["message"]["content"]
                answer = AnswerModel.model_validate(
                    {
                        "_id": str(uuid.uuid4()),
                        "query": query,
                        "model_answer": response_json,
                        "retrieved_documents_ids": [
                            documents[i].id for i in relevant_documents
                        ],
                    }
                )
                answers.append(answer)

        return answers

import logging
from tqdm import tqdm
from typing import List, Dict
import uuid
import pandas as pd

from ragformance.rag.rag_interface import RagInterface
from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel, AnswerModel

from ragformance.rag.clients.ollama_client import OllamaClient
from ragformance.rag.clients.openwebui_client import OpenWebUIClient


logging.basicConfig(level=logging.INFO)


# SETUP

# Run the following docker command
# docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
# docker run -d -p 3000:8080 --gpus all --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:cuda

# You need to create an OpenWebUi user, either with the web Interface or with python
# With python :
# client = OpenWebUIClient(client_url)
# new_admin = client.create_user(
#    name="Admin user",
#    email="admin@example.com",
#    password="admin",
#    role="admin"
# )

# Add the email and password on the config file


class OpenwebuiRag(RagInterface):
    def upload_corpus(self, corpus: List[DocModel], config: Dict = {}):
        try:
            id_column = "id"
            content_column = "text"

            logging.info("Récupération du fichier de configuration :'.")
            if "rag" in config and isinstance(config["rag"], list):
                for rag_config in config["rag"]:
                    if (
                        isinstance(rag_config, dict)
                        and rag_config.get("name") == "rag_open-webui"
                    ):
                        logging.info(
                            "Configuration de rag_open-webui extraite avec succès'."
                        )
                        config = rag_config
                    else:
                        logging.error(
                            "Échec de la récupération de la configuration au niveau de rag_open-webui."
                        )
                        return []
            else:
                logging.error(
                    "Échec de la récupération de la configuration au niveau de rag."
                )
                return []

            model_name = config.get("llm_name")
            collection_name = config.get("collection_name", "not_referenced")
            client_email = config.get("client_email", "admin@example.com")
            client_mdp = config.get("client_mdp", "admin")
            client_url = config.get("openwebui_url", "http://localhost:3000")

            client = OpenWebUIClient(client_url)
            client.sign_in(client_email, client_mdp)

            coll_info = None

            logging.info(
                f"Début du benchmark sur la collection {collection_name} avec le modèle '{model_name}'."
            )
            coll_info = client.create_collection(
                name=collection_name,
                description="Collection pour benchmark",
            )

            if not coll_info or "id" not in coll_info:
                logging.error(
                    f"Échec de la création ou de la récupération de la collection '{collection_name}'."
                )
                return []  # Retourne une liste vide

            collection_id = coll_info["id"]
            logging.info(f"Utilisation de la collection ID: {collection_id}")

            df = pd.DataFrame([c.model_dump(by_alias=True) for c in corpus])

            add_results = client.add_documents_from_df_to_collection(
                df=df,
                collection_id=collection_id,
                doc_id_column=id_column,
                content_column=content_column,
            )

            logging.info(f"Résultats de l'ajout des documents du CSV: {add_results}")

            config["collection_id"] = collection_id

            return add_results["processed_count"], config

        except Exception as e:
            logging.error(
                f"Une erreur est survenue durant l'upload du corpus: {e}", exc_info=True
            )

            raise e

    def ask_queries(self, queries: List[AnnotatedQueryModel], config: Dict = {}):
        content_column = "query_text"

        collection_id = config.get("collection_id")
        client_email = config.get("client_email", "admin@example.com")
        client_mdp = config.get("client_mdp", "admin")

        client_url = config.get("openwebui_url", "http://localhost:3000")
        ollama_url = config.get("ollama_url", "http://localhost:11434")

        client = OpenWebUIClient(client_url)
        ollama_client = OllamaClient(ollama_url)

        client.sign_in(client_email, client_mdp)

        model_name = config.get("llm_name", "not_referenced")

        ollama_client.pull_model(model_name)

        answers = []
        df_queries = pd.DataFrame([c.model_dump(by_alias=True) for c in queries])

        try:
            for i, (df_index, row) in enumerate(
                tqdm(
                    df_queries.iterrows(),
                    total=df_queries.shape[0],
                    desc=f"Benchmarking ({model_name})",
                )
            ):
                query_text = row[content_column]

                raw_chat_output = client.chat_with_collection(
                    model_name, query_text, collection_id
                )

                model_answer_text, sourced_documents = client.parse_chat_response(
                    raw_chat_output
                )

                docs_retrieved = []
                docs_dist = []
                for doc in sourced_documents:
                    docs_retrieved.append(doc.get("name"))
                    docs_dist.append(doc.get("distance"))

                query = row.to_dict()
                answer = AnswerModel.model_validate(
                    {
                        "_id": str(uuid.uuid4()),
                        "query": query,
                        "model_answer": model_answer_text,
                        "retrieved_documents_ids": docs_retrieved,
                        "retrieved_documents_distances": docs_dist,
                    }
                )
                answers.append(answer)

            logging.info("Benchmark terminé.")
            client.delete_collection(collection_id)

        except Exception as e:
            logging.error(
                f"Une erreur est survenue durant le benchmark: {e}", exc_info=True
            )

        return answers

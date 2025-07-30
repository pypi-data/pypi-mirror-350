from fed_rag import RAGSystem
from fed_rag.exceptions import FedRAGError


def _validate_rag_system(rag_system: RAGSystem) -> None:
    # Skip validation if environment variable is set
    import os

    if os.environ.get("FEDRAG_SKIP_VALIDATION") == "1":
        return

    from fed_rag.generators.huggingface import (
        HFPeftModelGenerator,
        HFPretrainedModelGenerator,
    )
    from fed_rag.generators.unsloth import UnslothFastModelGenerator
    from fed_rag.retrievers.huggingface.hf_sentence_transformer import (
        HFSentenceTransformerRetriever,
    )

    if not isinstance(
        rag_system.generator,
        (
            HFPretrainedModelGenerator,
            HFPeftModelGenerator,
            UnslothFastModelGenerator,
        ),
    ):
        raise FedRAGError(
            "Generator must be HFPretrainedModelGenerator or HFPeftModelGenerator"
        )

    if not isinstance(rag_system.retriever, HFSentenceTransformerRetriever):
        raise FedRAGError("Retriever must be a HFSentenceTransformerRetriever")


from functools import lru_cache

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

try:
    import numpy as np
except ImportError:
    np = None


@lru_cache(maxsize=1)
def get_embedding_model():
    if SentenceTransformer is None:
        raise ImportError(
            "sentence-transformers is not installed. Please install via: pip install sentence-transformers"
        )
    print("Loading Sentence Transformer model...")

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2",
        device="cpu"
    )

    print("Embedding model loaded successfully!")
    return model


class EmbeddingModel:

    def __init__(self):
        self.model = get_embedding_model()

    def generate_embeddings(self, texts):

        if not texts:
            return np.empty((0, 384), dtype=np.float32)

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        return embeddings.astype(np.float32)


if __name__ == "__main__":

    embedding_model = EmbeddingModel()

    sample_texts = [
        "What is artificial intelligence?",
        "Artificial intelligence enables machines to perform intelligent tasks.",
        "The capital of India is New Delhi."
    ]

    vectors = embedding_model.generate_embeddings(sample_texts)

    print("\nEmbedding Results")
    print("-------------------------")
    print("Number of texts:", len(sample_texts))
    print("Embedding shape:", vectors.shape)
    print("Vector dimension:", vectors.shape[1])

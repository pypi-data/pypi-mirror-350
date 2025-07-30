from sentence_transformers import SentenceTransformer
from MetaRagTool.Encoders.Encoder import Encoder
import MetaRagTool.Constants as Constants

good_encoder_names = [
    'sentence-transformers/LaBSE',
    'codersan/FaLaBSE-v3',
    'intfloat/multilingual-e5-base',
    'sentence-transformers/use-cmlm-multilingual',
    'HIT-TMG/KaLM-embedding-multilingual-mini-instruct-v1',
    'myrkur/sentence-transformer-parsbert-fa',
    'BAAI/bge-m3',




    #  from https://huggingface.co/spaces/PartAI/pteb-leaderboard
    'jinaai/jina-embeddings-v3',
    'intfloat/multilingual-e5-large',
    'intfloat/multilingual-e5-base',
    'Alibaba-NLP/gte-multilingual-base',
    'PartAI/Tooka-SBERT',
    'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
    'sentence-transformers/LaBSE',
    'm3hrdadfi/bert-zwnj-wnli-mean-tokens',
    'm3hrdadfi/roberta-zwnj-wnli-mean-tokens',
    'myrkur/sentence-transformer-parsbert-fa',
    'WhereIsAI/UAE-Large-V1',
    'intfloat/e5-large-v2',
    'intfloat/e5-base-v2',
    'thenlper/gte-large',
]


class SentenceTransformerEncoder(Encoder):
    MODEL_NAME_LABSE = "sentence-transformers/LaBSE"
    def __init__(self, model_name: str, verbose=False):
        super().__init__(model_name, verbose)
        if Constants.trust_remote_code:
            self.model = SentenceTransformer(model_name,trust_remote_code=True)
        else:
            self.model = SentenceTransformer(model_name)
        print("Model loaded successfully")

    def encode(self, sentences, isQuery=True):
        embeddings = self.model.encode(sentences,
                                       # normalize_embeddings=True,
                                       # batch_size=256,
                                       show_progress_bar=not isQuery,

                                       convert_to_tensor=False)
        return embeddings

from sentence_transformers import SentenceTransformer, models
from transformers import pipeline
def init():
    model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
    global sentiment_task
    global model
    sentiment_task = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)
    model = SentenceTransformer('paraphrase-xlm-r-multilingual-v1', device='cuda')
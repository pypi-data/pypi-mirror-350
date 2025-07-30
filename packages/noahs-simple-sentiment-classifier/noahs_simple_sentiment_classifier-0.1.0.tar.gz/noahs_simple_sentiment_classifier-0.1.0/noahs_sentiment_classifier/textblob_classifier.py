from textblob import TextBlob
from textblob.download_corpora import download_all

def safe_download():
    try:
        _ = TextBlob("test").sentiment
    except:
        print("[TextBlob] Downloading corpora...")
        download_all()
        print("[TextBlob] Corpora downloaded.")

safe_download()

def classify(text, friendly_threshold=0.3, hostile_threshold=-0.3):
    polarity = TextBlob(text).sentiment.polarity
    if polarity < hostile_threshold:
        return "hostile"
    elif polarity > friendly_threshold:
        return "friendly"
    else:
        return "neutral"









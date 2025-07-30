



# Noah's Simple Sentiment Classifier

A super simple implementation of the textblob polarity classifier

## Installation

```bash
pip install noahs_simple_sentiment_classifier
```

## Code Sample

```python
from noahs_simple_sentiment_classifier import classify

value = classify("i hate you")
# value will be either "hostile","friendly","neutral"
print(value)

```
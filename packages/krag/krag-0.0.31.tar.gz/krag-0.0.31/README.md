# Krag

Krag is a Python package designed to evaluate RAG (Retrieval-Augmented Generation) systems. It provides various evaluation metrics including Hit Rate, Recall, Precision, MRR (Mean Reciprocal Rank), MAP (Mean Average Precision), and NDCG (Normalized Discounted Cumulative Gain).

## Installation

```bash
pip install krag
```

## Key Features

### 1. **Evaluation Metrics**

- **Hit Rate**: Measures ratio of correctly identified target documents
- **Recall**: Measures ratio of relevant documents found in top-k predictions
- **Precision**: Measures accuracy of top-k predictions
- **F1 Score**: Harmonic mean of Precision and Recall
- **MRR** (Mean Reciprocal Rank): Average of inverse rank for first relevant document
- **MAP** (Mean Average Precision): Average precision at ranks with relevant documents
- **NDCG** (Normalized Discounted Cumulative Gain): Measures ranking quality with position-weighted gains

### 2. **Document Matching Methods**

- Text Preprocessing

  - TokenizerType (**KIWI**(for Korean), **NLTK**, WHITESPACE)
  - TokenizerConfig for consistent normalization
  - Language-specific tokenization support (Korean/ English)

- Matching Methods
  - Exact text matching
  - ROUGE-based matching (rouge1, rouge2, rougeL)
  - Embedding-based similarity
    - Supports HuggingFace, OpenAI, Ollama
    - Configurable thresholds
    - Cached embeddings for efficiency

### 3. **Configuration Options**

- Tokenizer selection and settings
- Rouge/similarity thresholds
- Embedding model configuration
- Averaging methods (micro/macro)

### 4. **Visualization**

- Comparative bar charts for metrics

## Metric Details

```python
def calculate_hit_rate(k):
    """
    Hit rate = # queries with correct documents / total queries
    - ALL: Found all target docs
    - PARTIAL: Found at least one target doc
    """

def calculate_recall(k):
    """
    Recall = # relevant docs retrieved / total relevant docs
    - micro: Document-level average
    - macro: Query-level average
    """

def calculate_precision(k):
    """
    Precision = # relevant retrieved / # retrieved
    - micro: Document-level average
    - macro: Query-level average
    """

def calculate_f1_score(k):
    """F1 = 2 * (precision * recall)/(precision + recall)"""

def calculate_mrr(k):
    """MRR = mean(1/rank of first relevant doc)"""

def calculate_map(k):
    """MAP = mean(average precision per query)"""

def calculate_ndcg(k):
    """NDCG = DCG/IDCG with position discounting"""
```

## Usage Examples

### 1. Basic Evaluator

```python
from krag.document import KragDocument as Document
from krag.evaluators import OfflineRetrievalEvaluators, AveragingMethod, MatchingCriteria

actual_docs = [
    [Document(page_content="This is the first document."),
     Document(page_content="This is the second document.")],
]

predicted_docs = [
    [Document(page_content="This is the last document."),
     Document(page_content="This is the second document.")],
]

evaluator = OfflineRetrievalEvaluators(
    actual_docs,
    predicted_docs,
    averaging_method=AveragingMethod.MICRO,
    matching_criteria=MatchingCriteria.PARTIAL
)

# Calculate individual metrics
hit_rate = evaluator.calculate_hit_rate(k=2)
mrr = evaluator.calculate_mrr(k=2)
recall = evaluator.calculate_recall(k=2)
precision = evaluator.calculate_precision(k=2)
f1_score = evaluator.calculate_f1_score(k=2)
map_score = evaluator.calculate_map(k=2)
ndcg = evaluator.calculate_ndcg(k=2)

print(f"Hit Rate @2: {hit_rate}")
print(f"MRR @2: {mrr}")
print(f"Recall @2: {recall}")
print(f"Precision @2: {precision}")
print(f"F1 Score @2: {f1_score}")
print(f"MAP @2: {map_score}")
print(f"NDCG @2: {ndcg}")

# Visualize the evaluation results
evaluator.visualize_results(k=2)
```

#### Metric Values

```python
Hit Rate @2: {'hit_rate': 1.0}
MRR @2: {'mrr': 0.5}
Recall @2: {'micro_recall': 0.5}
Precision @2: {'micro_precision': 0.5}
F1 Score @2: {'micro_f1': 0.5}
MAP @2: {'map': 0.25}
NDCG @2: {'ndcg': 0.6309297535714575}
```

#### Visualization Result

![Evaluation Results Visualization](docs/sample_1.png)

### 2. ROUGE Evaluator

```python
from krag.evaluators import RougeOfflineRetrievalEvaluators

# Evaluation using ROUGE matching
evaluator = RougeOfflineRetrievalEvaluators(
    actual_docs,
    predicted_docs,
    averaging_method=AveragingMethod.MICRO,
    matching_criteria=MatchingCriteria.PARTIAL,
    match_method="rouge2",  # Choose from rouge1, rouge2, rougeL
    threshold=0.8  # ROUGE score threshold
)

# Calculate individual metrics
hit_rate = evaluator.calculate_hit_rate(k=2)
mrr = evaluator.calculate_mrr(k=2)
recall = evaluator.calculate_recall(k=2)
precision = evaluator.calculate_precision(k=2)
f1_score = evaluator.calculate_f1_score(k=2)
map_score = evaluator.calculate_map(k=2)
ndcg = evaluator.calculate_ndcg(k=2)

print(f"Hit Rate @2: {hit_rate}")
print(f"MRR @2: {mrr}")
print(f"Recall @2: {recall}")
print(f"Precision @2: {precision}")
print(f"F1 Score @2: {f1_score}")
print(f"MAP @2: {map_score}")
print(f"NDCG @2: {ndcg}")

# Visualize the evaluation results
evaluator.visualize_results(k=2)
```

#### Metric Values

```python
Hit Rate @2: {'hit_rate': 1.0}
MRR @2: {'mrr': 0.5}
Recall @2: {'micro_recall': 0.5}
Precision @2: {'micro_precision': 0.5}
F1 Score @2: {'micro_f1': 0.5}
MAP @2: {'map': 0.25}
NDCG @2: {'ndcg': 0.8651447273736845}
```

#### Visualization Result

![Evaluation Results Visualization](docs/sample_2.png)

### 3. Embedding-based ROUGE Evaluator

Performs initial filtering using text embeddings followed by detailed comparison using ROUGE scores.

```python
from krag.evaluators import EmbeddingRougeOfflineRetrievalEvaluators

# Using HuggingFace embeddings
evaluator = EmbeddingRougeOfflineRetrievalEvaluators(
    actual_docs,
    predicted_docs,
    averaging_method=AveragingMethod.MICRO,
    matching_criteria=MatchingCriteria.PARTIAL,
    embedding_type="huggingface",
    embedding_config={
        "model_name": "jhgan/ko-sroberta-multitask",
        "model_kwargs": {'device': 'cpu'},
        "encode_kwargs": {'normalize_embeddings': False}
    },
    similarity_threshold=0.7,  # Embedding similarity threshold
    rouge_threshold=0.8  # ROUGE score threshold
)

# Using OpenAI embeddings
evaluator = EmbeddingRougeOfflineRetrievalEvaluators(
    actual_docs,
    predicted_docs,
    averaging_method=AveragingMethod.MICRO,
    matching_criteria=MatchingCriteria.PARTIAL,
    embedding_type="openai",
    embedding_config={
        "model": "text-embedding-3-small",
        "dimensions": 1024  # Optional embedding dimensions
    },
    similarity_threshold=0.7,  # Embedding similarity threshold
    rouge_threshold=0.8  # ROUGE score threshold
)

# Using Ollama embeddings
evaluator = EmbeddingRougeOfflineRetrievalEvaluators(
    actual_docs,
    predicted_docs,
    averaging_method=AveragingMethod.MICRO,
    matching_criteria=MatchingCriteria.PARTIAL,
    embedding_type="ollama",
    embedding_config={"model": "bge-m3"},
    similarity_threshold=0.8,  # Embedding similarity threshold
    rouge_threshold=0.8  # ROUGE score threshold

)

# Calculate individual metrics
hit_rate = evaluator.calculate_hit_rate(k=2)
mrr = evaluator.calculate_mrr(k=2)
recall = evaluator.calculate_recall(k=2)
precision = evaluator.calculate_precision(k=2)
f1_score = evaluator.calculate_f1_score(k=2)
map_score = evaluator.calculate_map(k=2)
ndcg = evaluator.calculate_ndcg(k=2)

print(f"Hit Rate @2: {hit_rate}")
print(f"MRR @2: {mrr}")
print(f"Recall @2: {recall}")
print(f"Precision @2: {precision}")
print(f"F1 Score @2: {f1_score}")
print(f"MAP @2: {map_score}")
print(f"NDCG @2: {ndcg}")

# Visualize the evaluation results
evaluator.visualize_results(k=2)
```

#### Metric Values

```python
Hit Rate @2: {'hit_rate': 1.0}
MRR @2: {'mrr': 0.5}
Recall @2: {'micro_recall': 1.0}
Precision @2: {'micro_precision': 0.5}
F1 Score @2: {'micro_f1': 0.6666666666666666}
MAP @2: {'map': 0.25}
NDCG @2: {'ndcg': 0.6309297535714575}
```

#### Visualization Result

![Evaluation Results Visualization](docs/sample_3.png)

## Important Notes

1. Required packages for embedding models:

   - HuggingFace: `pip install langchain-huggingface`
   - OpenAI: `pip install langchain-openai`
   - Ollama: `pip install langchain-ollama`

2. OpenAI embeddings require an API key:
   ```python
   import os
   os.environ["OPENAI_API_KEY"] = "your-api-key"
   ```

## License

MIT License [MIT 라이선스](https://opensource.org/licenses/MIT)

## Contact

Questions: [ontofinances@gmail.com](mailto:ontofinances@gmail.com)

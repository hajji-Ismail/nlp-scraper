# NLP Scraper

A comprehensive pipeline for scraping news articles, enriching them with NLP analysis, and detecting environmental scandals.

## Overview

This project combines web scraping, natural language processing, and machine learning to:
1. **Scrape** news articles from Yahoo News
2. **Enrich** articles with entity detection, topic classification, and sentiment analysis
3. **Detect** environmental scandals using semantic similarity and crisis keywords

## Features

### News Scraping (`scraper_news.py`)
- Scrapes multiple pages from Yahoo News
- Extracts headlines, timestamps, and full article content
- Stores structured data in CSV format
- Implements URL deduplication and rate limiting
- Includes error handling and retry logic

### NLP Enrichment (`nlp_enriched_news.py`)
- **Entity Recognition**: Identifies organizations mentioned in articles
- **Topic Detection**: Classifies articles by topic using a pre-trained model
- **Sentiment Analysis**: Computes sentiment scores using VADER lexicon
- **Scandal Detection**: Detects environmental crisis mentions using semantic similarity
  - Uses embeddings to measure distance from environmental keywords
  - Flags high-risk articles (scandal distance ≥ 0.4)
  - Identifies implicated companies

## Installation

### Requirements
- Python 3.11+
- Dependencies listed in `requirement.txt`

### Setup

1. Create and activate a conda environment:
```bash
conda create --name nlp-scraper --file requirement.txt
conda activate nlp-scraper
```



## Usage

### Step 1: Scrape News Articles
```bash
python scraper_news.py
```

This generates `data/newsdata.csv` containing raw article data with columns:
- `unique ID`: Article identifier
- `URL`: Source URL
- `date`: Published date
- `headline`: Article title
- `body of the article`: Full article text

### Step 2: Enrich Articles with NLP
```bash
python nlp_enriched_news.py
```

This processes the scraped articles and generates `results/enhanced_news.csv` with enriched columns:
- `uuid`: Article ID
- `URL`: Article source
- `Date scraped`: Scrape timestamp
- `Headline`: Article title
- `Body`: Article content
- `Org`: Detected organizations
- `Topics`: Article topic classification
- `Sentiment`: Sentiment score (-1.0 to 1.0)
- `Scandal_distance`: Environmental scandal similarity (0.0 to 1.0)
- `Top_10`: Boolean flag for top 10 articles by scandal score

## Project Structure

```
.
├── scraper_news.py          # Web scraping module
├── nlp_enriched_news.py     # NLP enrichment pipeline
├── requirement.txt          # Conda environment specification
├── data/                    # Input data directory
│   └── newsdata.csv         # Raw scraped articles
└── results/                 # Output directory
    ├── enhanced_news.csv    # Enriched articles
    └── topic_classifier.pkl # Pre-trained topic model
```

## Environment Variables

No environment variables required. All paths are relative to the project root.

## Output

### Raw Articles (`data/newsdata.csv`)
CSV file with scraped article metadata and content.

### Enhanced Articles (`results/enhanced_news.csv`)
CSV file with NLP-enriched data sorted by scandal relevance. Top 10 articles flagged by scandal score.

## Key Technologies

- **Web Scraping**: BeautifulSoup, requests
- **NLP**: spaCy, NLTK (VADER sentiment), sentence-transformers
- **ML**: scikit-learn, PyTorch
- **Data Processing**: pandas, numpy
- **Serialization**: joblib

## Embeddings and Distance Metric Explanation

### Choice of Embedding Model: `all-MiniLM-L6-v2`

The project uses the **`all-MiniLM-L6-v2`** model from the Sentence-Transformers library for semantic text representation. This choice is motivated by:

1. **Efficiency & Speed**: MiniLM is a lightweight, distilled model (~22MB) that produces 384-dimensional embeddings, making it fast for real-time inference without sacrificing semantic quality.

2. **Semantic Quality**: Despite its small size, MiniLM achieves strong performance on semantic similarity tasks. It captures nuanced meanings in environmental crisis keywords effectively (e.g., distinguishing "oil spill" from "chemical contamination").

3. **Proven Performance**: The model is trained on a diverse corpus of 215M sentence pairs, making it robust for detecting semantic relationships between crisis descriptions and environmental keywords.

4. **Resource Constraints**: In production, lightweight models reduce computational overhead, memory footprint, and latency—critical for batch processing large article datasets.

### Choice of Distance Metric: Cosine Similarity

The scandal detection pipeline uses **cosine similarity** to measure semantic distance between article sentences and environmental crisis keywords. This choice reflects:

1. **Vector Space Geometry**: Cosine similarity measures the angle between embedding vectors in high-dimensional space, which is ideal for normalized embeddings. It ranges from -1 (opposite) to 1 (identical), normalized to 0-1 for this use case.

2. **Semantic Relevance**: Cosine similarity is invariant to vector magnitude, capturing semantic meaning rather than frequency. This prevents high-frequency crisis keywords from dominating the scoring.

3. **Interpretability**: A cosine similarity score of 0.4+ indicates meaningful semantic overlap between article content and environmental crisis patterns, providing a clear threshold for scandal flagging.

4. **Computational Efficiency**: Cosine similarity is computationally lightweight (dot product + normalization), enabling fast batch processing of thousands of articles.

### Implementation Details

- **Threshold**: Scandal detection triggers when cosine similarity ≥ 0.4 between an article sentence (containing a detected company) and environmental keywords.
- **Aggregation**: The maximum similarity across all sentences mentioning a company is used to identify the most relevant environmental scandal signal.
- **Keyword Set**: Five high-specificity crisis keywords ensure precision:
  - "environmental pollution"
  - "illegal deforestation"
  - "toxic waste dumping"
  - "oil spill disaster"
  - "chemical river contamination"

### Trade-offs and Alternatives

| Approach | Pros | Cons | Why Not Used |
|----------|------|------|-------------|
| **Cosine Similarity** (Current) | Fast, interpretable, semantic-focused | Limited to normalized vectors | — (Selected) |
| Euclidean Distance | Intuitive, common in ML | Magnitude-sensitive, slower | Inappropriate for normalized embeddings |
| Dot Product | Fastest | Not normalized, varies with vector magnitude | Would require manual scaling |
| Larger Models (e.g., all-mpnet-base-v2) | Higher semantic precision | 10x slower, higher memory (438MB) | Overkill for keyword matching; violates latency requirements |

## Notes

- Article scraping includes 1-second delays between article fetches to respect server load
- Environmental keywords are embedded using `all-MiniLM-L6-v2` model
- Sentiment scores: positive ≥ 0.05, negative ≤ -0.05, neutral otherwise
- Scandal detection threshold: similarity score ≥ 0.4

## Author

HAjji Ismail 
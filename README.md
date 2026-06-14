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

## Notes

- Article scraping includes 1-second delays between article fetches to respect server load
- Environmental keywords are embedded using `all-MiniLM-L6-v2` model
- Sentiment scores: positive ≥ 0.05, negative ≤ -0.05, neutral otherwise
- Scandal detection threshold: similarity score ≥ 0.4

## Author

HAjji Ismail 
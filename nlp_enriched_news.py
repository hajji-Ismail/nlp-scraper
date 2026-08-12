import os
import joblib
import numpy as np
import pandas as pd
import spacy
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sentence_transformers import SentenceTransformer, util
import sqlite3


print("Initializing pipeline models and resources...")
nltk.download('vader_lexicon', quiet=True)
sia = SentimentIntensityAnalyzer()
nlp = spacy.load("en_core_web_sm")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

ENVIRONMENTAL_KEYWORDS = [
    "environmental pollution", 
    "illegal deforestation", 
    "toxic waste dumping", 
    "oil spill disaster", 
    "chemical river contamination"
]
KEYWORD_EMBEDDINGS = embedding_model.encode(ENVIRONMENTAL_KEYWORDS, convert_to_tensor=True)

# Load your pre-trained topic classifier model
TOPIC_MODEL_PATH = "./results/topic_classifier.pkl"

loaded_pipeline = joblib.load(TOPIC_MODEL_PATH)



def detect_entities(text):
    doc = nlp(text)
    companies = {ent.text for ent in doc.ents if ent.label_ == "ORG"}
    return list(companies)

def detect_topic(text):
   
        predictions = loaded_pipeline.predict([text])
        return predictions


def analyze_sentiment_score(text):
    scores = sia.polarity_scores(text)
    return round(scores["compound"], 4)

def get_sentiment_label(score):
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    return "neutral"

def calculate_scandal_distance(article_body, target_companies):
    if not article_body or not isinstance(article_body, str) or not target_companies:
        return 0.0, "None"
        
    max_article_similarity = 0.0
    implicated_company = "None"
    
    sentences = [s.strip() for s in article_body.split(".") if s.strip()]
    if not sentences:
        sentences = [article_body]

    for sentence in sentences:
        company_in_sentence = next((comp for comp in target_companies if comp.lower() in sentence.lower()), None)
        
        if company_in_sentence:
            sentence_embedding = embedding_model.encode(sentence, convert_to_tensor=True)
            similarities = util.cos_sim(sentence_embedding, KEYWORD_EMBEDDINGS)[0]
            max_sentence_score = float(np.max(similarities.cpu().numpy()))
            
            if max_sentence_score > max_article_similarity:
                max_article_similarity = max_sentence_score
                implicated_company = company_in_sentence

    return round(max_article_similarity, 4), implicated_company


def main():
    input_path = "./data/newsdata.db"
    output_path = "./results/enhanced_news.csv"
    
    if not os.path.exists(input_path):
        print(f"Error: Input dataset file not found at {input_path}")
        return
   
    conn = sqlite3.connect("./data/newsdata.db")
    conn.row_factory = sqlite3.Row

    output_path = "./results/enhanced_news.csv"

    df = pd.read_sql_query("SELECT * FROM news", conn)

    df.to_csv(output_path, index=False)    
    processed_records = []
    
    print(f"\nProcessing {len(df)} articles...\n")
    
    for idx, row in df.iterrows():
        uuid_val = row.get("unique ID")
        url_val = row.get("URL")
        date_val = row.get("date")
        headline_val = str(row.get("headline", ""))
        body_val = str(row.get("body of the article", ""))
        
        full_document = f"{headline_val} {body_val}"
        
        print("Cleaning document ...")
        
        print("---------- Detect entities ----------")
        orgs = detect_entities(full_document)
        orgs_str = " and ".join(orgs) if orgs else "no"
        print(f"Detected {len(orgs)} companies which are {orgs_str}")
        
        print("---------- Topic detection ----------")
        print("Text preprocessing ...")
        topics = detect_topic(full_document)
        print(f"The topic of the article is: {topics[0]}")
        
        print("---------- Sentiment analysis ----------")
        print("Text preprocessing ...")
        sentiment_score = analyze_sentiment_score(full_document)
        sentiment_label = get_sentiment_label(sentiment_score)
        print(f"The article {headline_val} has a {sentiment_label} sentiment")
        
        print("---------- Scandal detection ----------")
        print("Computing embeddings and distance ...")
        scandal_dist, implicated_org = calculate_scandal_distance(body_val, orgs)
        
        if implicated_org != "None" and scandal_dist >= 0.4:
            print(f"Environmental scandal detected for {implicated_org}")
        print("-" * 50)
        
        record = {
            "uuid": uuid_val,
            "URL": url_val,
            "Date scraped": date_val,
            "Headline": headline_val,
            "Body": body_val,
            "Org": orgs,
            "Topics": topics,
            "Sentiment": sentiment_score,
            "Scandal_distance": scandal_dist,
            "Top_10": False # Set false initially; updated post-sorting below
        }
        processed_records.append(record)

 
    processed_records.sort(key=lambda x: x["Scandal_distance"], reverse=True)
    
  
    for idx in range(min(10, len(processed_records))):
        processed_records[idx]["Top_10"] = True
        

    output_df = pd.DataFrame(processed_records)
    output_df.to_csv(output_path, index=False)
    print(f"\nProcessing Complete! Enhanced dataset successfully stored in: {output_path}")

if __name__ == "__main__":
    main()
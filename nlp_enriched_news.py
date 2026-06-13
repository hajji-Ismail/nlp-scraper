
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy
import joblib
sia = SentimentIntensityAnalyzer()

nlp = spacy.load("en_core_web_sm")

def Entities_detection(text):
  
    doc = nlp(text)
    
   
  
    companies = {ent.text for ent in doc.ents if ent.label_ == "ORG"}
    
    return set(companies)

def Topic_detection(text):
  
  
    loaded_pipeline = joblib.load("./results/topic_classifier.pkl")
    
    predictions = loaded_pipeline.predict([text])
    return  predictions
    
   
   



def analyze_sentiment(text):
 
    
    # 1. Compute the structural scores under the hood
    scores = sia.polarity_scores(text)
    compound = scores['compound']
    
    # 2. Apply our threshold conditions
    if compound >= 0.05:
        category = "positive"
    elif compound <= -0.05:
        category = "negative"
    else:
        category = "neutral"
        
    return category
        
    
        
    
headline = "Apple Inc. acquires a new startup in London."
body = "The deal was finalized yesterday by Apple Inc. and DeepMind."

# Combine or process separately
full_document = f"{headline} {body}"
detected_orgs = analyze_sentiment(full_document)

print(f"Detected Companies: {detected_orgs}")


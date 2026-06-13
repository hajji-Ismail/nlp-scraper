import spacy
import joblib

nlp = spacy.load("en_core_web_sm")

def Entities_detection(text):
  
    doc = nlp(text)
    
   
  
    companies = {ent.text for ent in doc.ents if ent.label_ == "ORG"}
    
    return set(companies)

def Topic_detection(text):
  
  
    loaded_pipeline = joblib.load("./results/topic_classifier.pkl")
    
    predictions = loaded_pipeline.predict([text])
    return  predictions
    
   
   
        
    
headline = "Apple Inc. acquires a new startup in London."
body = "The deal was finalized yesterday by Apple Inc. and DeepMind."

# Combine or process separately
full_document = f"{headline} {body}"
detected_orgs = Topic_detection(full_document)

print(f"Detected Companies: {detected_orgs}")




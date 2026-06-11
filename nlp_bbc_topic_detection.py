import os
import joblib
import numpy as np
import pandas as pd
import spacy
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import learning_curve
import en_core_web_sm

os.makedirs("./results", exist_ok=True)

def Extract_X_Y(df):
    """Extracts raw feature strings and labels cleanly."""
    X = df["Text"]
    Y = df["Category"]
    return X, Y

def generate_and_save_learning_curves(pipeline, X, Y):
  
    print("Generating learning curves for audit verification...")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator=pipeline,
        X=X,
        y=Y,
        cv=5,                 
        n_jobs=-1,          
        train_sizes=np.linspace(0.1, 1.0, 5),
        scoring='accuracy'
    )
    
    # Calculate means and standard deviations
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)
   
    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, train_mean, 'o-', color="red", label="Training Score")
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1, color="red")
    
    plt.plot(train_sizes, test_mean, 'o-', color="green", label="Cross-Validation (Test) Score")
    plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, alpha=0.1, color="green")
    
    plt.title("NLP Model Learning Curves")
    plt.xlabel("Training Set Size Instances")
    plt.ylabel("Accuracy Score Metric")
    plt.legend(loc="best")
    plt.grid(True)
    
    plt.savefig("./results/learning_curves.png")
    plt.close()
    print("Learning curve saved: './results/learning_curves.png'")

def training(X, Y):
   
    text_clf = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', sublinear_tf=True)),
        ('clf', MultinomialNB(alpha=0.1)),
    ])
 
    generate_and_save_learning_curves(text_clf, X, Y)
    
    print("Fitting final pipeline architecture...")
    text_clf.fit(X, Y)
    
  
    joblib.dump(text_clf, './results/topic_classifier.pkl')
    print("Model persistent state exported successfully to './results/topic_classifier.pkl'")

def prediction_and_ner():
  
  
    df_test = pd.read_csv("./data/bbc_news_tests.csv")
    loaded_pipeline = joblib.load("./results/topic_classifier.pkl")
    
    predictions = loaded_pipeline.predict(df_test["Text"])
    df_test["Predicted_Topic"] = predictions
    
   
    if "Category" in df_test.columns:
        accuracy = (df_test["Predicted_Topic"] == df_test["Category"]).mean()
        print(f"\nTarget Evaluation Metric -> Test Set Accuracy Score: {accuracy * 100:.2f}%")
        
    
    
   
    

def main():
    df_train = pd.read_csv("./data/bbc_news_train.csv")
    df_train.set_index("ArticleId", inplace=True)
    
    X, Y = Extract_X_Y(df_train)
    training(X, Y)
    prediction_and_ner()

if __name__ == "__main__":
    main()
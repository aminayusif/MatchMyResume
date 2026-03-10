import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

# Set experiment name
mlflow.set_experiment("ResumeMatcher")

def train():

    with mlflow.start_run():

        # Dummy dataset for now
        resumes = [
            "Python SQL pandas NumPy Power BI",
            "Java Spring Boot microservices",
            "React frontend JavaScript HTML CSS"
        ]

        jobs = [
            "Data Analyst with Python and SQL",
            "Backend developer with Java",
            "Frontend React developer"
        ]

        # Parameter logging
        max_features = 500
        mlflow.log_param("max_features", max_features)

        vectorizer = TfidfVectorizer(max_features=max_features)
        X = vectorizer.fit_transform(resumes + jobs)

        # Log artifact
        os.makedirs("artifacts", exist_ok=True)

        with open("artifacts/vectorizer.pkl", "wb") as f:
            pickle.dump(vectorizer, f)

        mlflow.log_artifact("artifacts/vectorizer.pkl")

        # Simple similarity test metric
        sim = cosine_similarity(X[0], X[3])[0][0]

        mlflow.log_metric("sample_similarity", float(sim))

        print("Training complete. Similarity:", sim)


if __name__ == "__main__":
    train()
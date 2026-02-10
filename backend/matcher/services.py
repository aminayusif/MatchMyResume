from pathlib import Path
import joblib
from sklearn.metrics.pairwise import cosine_similarity
import re
import string
import numpy as np

# ------------------ preprocessing ------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text.strip()

# ------------------ correct BASE DIR ------------------
# services.py -> matcher -> backend -> project root
BASE_DIR = Path(__file__).resolve().parents[2]

VECTORIZER_PATH = BASE_DIR / "machine-learning" / "artifacts" / "tfidf_vectorizer.pkl"

if not VECTORIZER_PATH.exists():
    raise FileNotFoundError(f"Vectorizer not found at {VECTORIZER_PATH}")

vectorizer = joblib.load(VECTORIZER_PATH)

def extract_keywords(resume_text, job_text, top_n=15):
    feature_names = np.array(vectorizer.get_feature_names_out())

    resume_vec = vectorizer.transform([clean_text(resume_text)]).toarray()[0]
    job_vec = vectorizer.transform([clean_text(job_text)]).toarray()[0]

    resume_words = set(feature_names[resume_vec > 0])
    job_words = set(feature_names[job_vec > 0])

    matched_keywords = list(resume_words & job_words)
    missing_keywords = list(job_words - resume_words)

    return matched_keywords[:top_n], missing_keywords[:top_n]


def interpret_similarity(score):
    if score < 0.3:
        return "Poor match"
    elif score < 0.5:
        return "Weak match"
    elif score < 0.7:
        return "Good match"
    else:
        return "Strong match"


# ------------------ matcher ------------------
def match_resume_to_job(resume_text, job_text):
    resume_clean = clean_text(resume_text)
    job_clean = clean_text(job_text)

    resume_vec = vectorizer.transform([resume_clean])
    job_vec = vectorizer.transform([job_clean])

    score = cosine_similarity(resume_vec, job_vec)[0][0]

    matched, missing = extract_keywords(resume_text, job_text)

    return {
        "similarity_score": float(score),
        "match_level": interpret_similarity(score),
        "matched_keywords": matched,
        "missing_keywords": missing
    }

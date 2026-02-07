from pathlib import Path
import joblib
from sklearn.metrics.pairwise import cosine_similarity
import re
import string

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

# ------------------ matcher ------------------
def match_resume_to_job(resume_text, job_text):
    resume_vec = vectorizer.transform([clean_text(resume_text)])
    job_vec = vectorizer.transform([clean_text(job_text)])

    score = cosine_similarity(resume_vec, job_vec)[0][0]
    return float(score)

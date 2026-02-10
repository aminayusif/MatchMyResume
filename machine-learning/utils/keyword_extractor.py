import numpy as np

def extract_keywords(vectorizer, resume_text, job_text, top_n=15):
    feature_names = np.array(vectorizer.get_feature_names_out())

    resume_vec = vectorizer.transform([resume_text]).toarray()[0]
    job_vec = vectorizer.transform([job_text]).toarray()[0]

    resume_words = set(feature_names[resume_vec > 0])
    job_words = set(feature_names[job_vec > 0])

    matched_keywords = list(resume_words & job_words)
    missing_keywords = list(job_words - resume_words)

    return matched_keywords[:top_n], missing_keywords[:top_n]

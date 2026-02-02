def dummy_match_score(resume_text: str, job_text: str) -> float:
    """
    Temporary placeholder for ML logic.
    Simple word overlap ratio.
    """

    if not resume_text or not job_text:
        return 0.0

    resume_words = set(resume_text.lower().split())
    job_words = set(job_text.lower().split())

    overlap = resume_words.intersection(job_words)

    score = len(overlap) / max(len(job_words), 1)
    return round(score, 2)

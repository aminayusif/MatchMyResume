import sys
import os

ML_SRC_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../machine-learning/src")
)

if ML_SRC_PATH not in sys.path:
    sys.path.append(ML_SRC_PATH)

from dummy_matcher import dummy_match_score


def compute_match_score(resume_text, job_text):
    return dummy_match_score(resume_text, job_text)

import { useState } from "react";

function MatcherForm() {
  const [resumeText, setResumeText] = useState("");
  const [jobText, setJobText] = useState("");
  const [score, setScore] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(process.env.REACT_APP_API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          resume_text: resumeText,
          job_description: jobText,
        }),
      });

      const data = await response.json();
      setScore(data.similarity_score);
    } catch (err) {
      setError("Failed to connect to server");
    } finally {
      setLoading(false);
    }
  };
const interpretScore = (score) => {
  if (score >= 0.75) return "Strong match ✅";
  if (score >= 0.5) return "Moderate match ⚠️";
  if (score >= 0.3) return "Weak match ❌";
  return "Poor match ❌❌";
};

  return (
    <div>
      <h2>Resume–Job Matcher</h2>

      <form onSubmit={handleSubmit}>
        <textarea
          placeholder="Paste resume text here..."
          value={resumeText}
          onChange={(e) => setResumeText(e.target.value)}
          rows={6}
        />

        <textarea
          placeholder="Paste job description here..."
          value={jobText}
          onChange={(e) => setJobText(e.target.value)}
          rows={6}
        />

        <button type="submit" disabled={loading}>
          {loading ? "Matching..." : "Match Resume"}
        </button>
      </form>

      {score !== null && (
  <div>
    <p>
      Similarity Score: <strong>{score.toFixed(2)}</strong>
    </p>
    <p>
      Interpretation: <strong>{interpretScore(score)}</strong>
    </p>
  </div>
)}

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default MatcherForm;

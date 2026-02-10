import { useState } from "react";

function MatcherForm() {
  const [resumeText, setResumeText] = useState("");
  const [jobText, setJobText] = useState("");
  const [result, setResult] = useState(null);
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
      setResult(data); // ✅ store full response
    } catch (err) {
      setError("Failed to connect to server");
    } finally {
      setLoading(false);
    }
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

      {result && (
        <div>
          <h3>
            Similarity Score: {result.similarity_score.toFixed(2)}
          </h3>

          <p><strong>{result.match_level}</strong></p>

          <h4>Matched Skills</h4>
          <ul>
            {result.matched_keywords.map((skill, i) => (
              <li key={i} style={{ color: "green" }}>{skill}</li>
            ))}
          </ul>

          <h4>Missing Skills</h4>
          <ul>
            {result.missing_keywords.map((skill, i) => (
              <li key={i} style={{ color: "red" }}>{skill}</li>
            ))}
          </ul>
        </div>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default MatcherForm;

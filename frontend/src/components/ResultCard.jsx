function getBiasColor(score) {
  if (score < 0.3) return '#27ae60'
  if (score < 0.6) return '#f39c12'
  return '#e74c3c'
}

function getSentimentColor(overall) {
  if (overall === 'positive') return '#27ae60'
  if (overall === 'negative') return '#e74c3c'
  return '#7f8c8d'
}

function getSeverityColor(severity) {
  if (severity === 'low') return '#27ae60'
  if (severity === 'medium') return '#f39c12'
  return '#e74c3c'
}

function ResultCard({ result }) {
  const { title, source, word_count, analysis } = result

  return (
    <div className="result-card">
      <div className="result-header">
        <h2>{title}</h2>
        <div className="meta">
          <span className="source-tag">{source}</span>
          <span className="word-count">{word_count} words</span>
          <span className="language-tag">{analysis.language}</span>
        </div>
      </div>

      <div className="summary-section">
        <h3>Summary</h3>
        <p>{analysis.summary}</p>
      </div>

      <div className="metrics-grid">
        <div className="metric-card">
          <h4>Sentiment</h4>
          <div
            className="metric-value"
            style={{ color: getSentimentColor(analysis.sentiment.overall) }}
          >
            {analysis.sentiment.overall.toUpperCase()}
          </div>
          <div className="metric-score">
            Score: {analysis.sentiment.score.toFixed(2)}
          </div>
        </div>

        <div className="metric-card">
          <h4>Bias</h4>
          <div
            className="metric-value"
            style={{ color: getBiasColor(analysis.bias.score) }}
          >
            {analysis.bias.detected ? analysis.bias.lean.toUpperCase() : 'NONE'}
          </div>
          <div className="metric-score">
            Score: {analysis.bias.score.toFixed(2)}
          </div>
        </div>

        <div className="metric-card">
          <h4>Credibility</h4>
          <div
            className="metric-value"
            style={{ color: getBiasColor(1 - analysis.credibility_indicators.credibility_score) }}
          >
            {(analysis.credibility_indicators.credibility_score * 100).toFixed(0)}%
          </div>
          <div className="metric-score">
            {analysis.credibility_indicators.has_sources ? '✓ Sources' : '✗ Sources'} &nbsp;
            {analysis.credibility_indicators.has_quotes ? '✓ Quotes' : '✗ Quotes'}
          </div>
        </div>
      </div>

      <div className="bias-explanation">
        <h3>Bias Analysis</h3>
        <p>{analysis.bias.explanation}</p>
      </div>

      {analysis.propaganda_techniques.length > 0 &&
        analysis.propaganda_techniques[0].technique !== 'None' && (
          <div className="propaganda-section">
            <h3>Propaganda Techniques Detected</h3>
            {analysis.propaganda_techniques.map((t, i) => (
              <div key={i} className="propaganda-item">
                <div className="propaganda-header">
                  <span className="technique-name">{t.technique}</span>
                  <span
                    className="severity-badge"
                    style={{ background: getSeverityColor(t.severity) }}
                  >
                    {t.severity}
                  </span>
                </div>
                <p>{t.explanation}</p>
              </div>
            ))}
          </div>
        )}

      {analysis.loaded_language.length > 0 && (
        <div className="loaded-language-section">
          <h3>Loaded Language</h3>
          <div className="tags">
            {analysis.loaded_language.map((word, i) => (
              <span key={i} className="tag">{word}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default ResultCard
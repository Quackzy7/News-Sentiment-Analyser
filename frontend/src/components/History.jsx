import { useState, useEffect } from 'react'
import axios from 'axios'
import { getToken } from '../auth'

const API_BASE = import.meta.env.VITE_API_BASE

function History({ onClose }) {
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchHistory()
  }, [])

  const fetchHistory = async () => {
    try {
      const response = await axios.get(`${API_BASE}/history`, {
        headers: { Authorization: `Bearer ${getToken()}` }
      })
      setHistory(response.data.history)
    } catch (err) {
      setError('Failed to load history')
    } finally {
      setLoading(false)
    }
  }

  const getBiasColor = (lean) => {
    if (lean === 'left') return '#3b82f6'
    if (lean === 'right') return '#ef4444'
    if (lean === 'center') return '#22c55e'
    return '#6b7280'
  }

  const getSentimentColor = (sentiment) => {
    if (sentiment === 'positive') return '#22c55e'
    if (sentiment === 'negative') return '#ef4444'
    return '#6b7280'
  }

  const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="history-overlay">
      <div className="history-panel">
        <div className="history-header">
          <h2>Analysis History</h2>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        {loading && <p className="history-loading">Loading history...</p>}
        {error && <p className="error">{error}</p>}

        {!loading && history.length === 0 && (
          <div className="history-empty">
            <p>No analyses yet.</p>
            <p>Analyze an article to see it here.</p>
          </div>
        )}

        {!loading && history.length > 0 && (
          <div className="history-list">
            {history.map((item) => (
              <div key={item.id} className="history-item">
                <div className="history-item-title">
                  <a href={item.url} target="_blank" rel="noreferrer">
                    {item.title}
                  </a>
                </div>

                <div className="history-item-meta">
                  <span className="history-source">{item.source}</span>
                  <span className="history-date">{formatDate(item.analyzed_at)}</span>
                </div>

                <div className="history-item-badges">
                  <span
                    className="history-badge"
                    style={{ color: getSentimentColor(item.sentiment) }}
                  >
                    {item.sentiment}
                  </span>
                  <span
                    className="history-badge"
                    style={{ color: getBiasColor(item.bias_lean) }}
                  >
                    {item.bias_detected ? `${item.bias_lean} bias` : 'no bias'}
                  </span>
                  <span className="history-badge" style={{ color: '#f59e0b' }}>
                    {item.credibility_score
                      ? `${(item.credibility_score * 100).toFixed(0)}% credible`
                      : 'n/a'}
                  </span>
                </div>

                {item.summary && (
                  <p className="history-summary">{item.summary}</p>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default History
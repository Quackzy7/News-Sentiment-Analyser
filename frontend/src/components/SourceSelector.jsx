import { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE

function SourceSelector({ source, setSource }) {
  const [sources, setSources] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    axios.get(`${API_BASE}/sources`)
      .then(res => {
        setSources(res.data.supported_sources)
      })
      .catch(err => {
        console.error('Failed to fetch sources', err)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  if (loading) return <p style={{ color: '#888', fontSize: '0.9rem' }}>Loading sources...</p>

  return (
    <div className="source-selector">
      <p>Select news source:</p>
      <div className="source-buttons">
        {sources.map((s) => (
          <button
            key={s}
            className={`source-btn ${source === s ? 'active' : ''}`}
            onClick={() => setSource(s)}
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  )
}

export default SourceSelector
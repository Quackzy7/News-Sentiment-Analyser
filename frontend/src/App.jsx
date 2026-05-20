import { useState } from 'react'
import axios from 'axios'
import SourceSelector from './components/SourceSelector'
import ResultCard from './components/ResultCard'
import LoadingSpinner from './components/LoadingSpinner'
import './App.css'

const API_BASE = import.meta.env.VITE_API_BASE

function App() {
  const [source, setSource] = useState('')
  const [url, setUrl] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleAnalyze = async () => {
    if (!source || !url) {
      setError('Please select a source and enter a URL')
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await axios.post(`${API_BASE}/analyze`, {
        source,
        url
      })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>News Sentiment Analyser</h1>
        <p>Analyze bias, sentiment and propaganda in Nepali news articles</p>
      </header>

      <main className="main">
        <div className="input-section">
          <SourceSelector source={source} setSource={setSource} />

          <input
            type="text"
            className="url-input"
            placeholder="Paste article URL here..."
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />

          <button
            className="analyze-btn"
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? 'Analyzing...' : 'Analyze Article'}
          </button>

          {error && <p className="error">{error}</p>}
        </div>

        {loading && <LoadingSpinner />}
        {result && <ResultCard result={result} />}
      </main>
    </div>
  )
}

export default App
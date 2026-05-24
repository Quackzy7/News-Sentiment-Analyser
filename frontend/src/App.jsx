import { useState, useEffect } from 'react'
import axios from 'axios'
import SourceSelector from './components/SourceSelector'
import ResultCard from './components/ResultCard'
import LoadingSpinner from './components/LoadingSpinner'
import Login from './components/Login'
import { saveToken, getToken, removeToken, isAuthenticated } from './auth'
import './App.css'

const API_BASE = import.meta.env.VITE_API_BASE

function App() {
  const [source, setSource] = useState('')
  const [url, setUrl] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [user, setUser] = useState(null)

  useEffect(() => {

    const params = new URLSearchParams(window.location.search)
    const token = params.get('token')

    if (token) {
      saveToken(token)

      window.history.replaceState({}, document.title, '/')

      fetchUser(token)
    } else if (isAuthenticated()) {
      fetchUser(getToken())
    }
  }, [])

  const fetchUser = async (token) => {
    try {
      const response = await axios.get(`${API_BASE}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setUser(response.data)
    } catch (err) {
      removeToken()
    }
  }

  const handleLogout = () => {
    removeToken()
    setUser(null)
    setResult(null)
  }

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
      }, {
        headers: { Authorization: `Bearer ${getToken()}` }
      })
      setResult(response.data)
    } catch (err) {
      if (err.response?.status === 401) {
      removeToken()
      setUser(null)
    } else {
      setError(err.response?.data?.detail || 'Something went wrong')
    }
      
    } finally {
      setLoading(false)
    }
  }
  if (!user) return <Login />
   return (
    <div className="app">
      <header className="header">
        <div className="header-top">
          <div>
            <h1>News Sentiment Analyser</h1>
            <p>Analyze bias, sentiment and propaganda in Nepali news articles</p>
          </div>
          <div className="user-info">
            {user.picture && (
              <img src={user.picture} alt={user.name} className="user-avatar" />
            )}
            <span className="user-name">{user.name}</span>
            <button className="logout-btn" onClick={handleLogout}>Logout</button>
          </div>
        </div>
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
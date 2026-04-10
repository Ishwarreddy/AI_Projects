import { useState, useEffect, useRef } from 'react'
import axios from 'axios'

const API = 'http://localhost:8000'//import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

const styles = `
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg:        #0a0a0f;
    --surface:   #111118;
    --border:    #1e1e2e;
    --accent:    #e8ff47;
    --accent2:   #47ffe0;
    --danger:    #ff4747;
    --text:      #e8e8f0;
    --muted:     #5a5a7a;
    --sent:      #47ffe0;
    --failed:    #ff4747;
    --info:      #e8ff47;
    --radius:    12px;
    --font-head: 'Syne', sans-serif;
    --font-mono: 'Space Mono', monospace;
  }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--font-mono);
    min-height: 100vh;
    overflow-x: hidden;
  }

  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(rgba(232,255,71,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(232,255,71,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
  }

  .app {
    position: relative;
    z-index: 1;
    display: grid;
    grid-template-columns: 340px 1fr;
    grid-template-rows: 64px 1fr;
    height: 100vh;
  }

  .header {
    grid-column: 1 / -1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 28px;
    border-bottom: 1px solid var(--border);
    background: var(--surface);
  }

  .header-brand { display: flex; align-items: center; gap: 12px; }

  .header-logo {
    width: 32px; height: 32px;
    background: var(--accent);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
  }

  .header-title {
    font-family: var(--font-head);
    font-size: 18px; font-weight: 800;
    letter-spacing: -0.5px;
  }
  .header-title span { color: var(--accent); }

  .header-status {
    display: flex; align-items: center; gap: 8px;
    font-size: 11px; color: var(--muted);
    text-transform: uppercase; letter-spacing: 1px;
  }

  .status-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--sent);
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(71,255,224,0.4); }
    50%       { opacity: 0.7; box-shadow: 0 0 0 6px rgba(71,255,224,0); }
  }

  .header-stats { display: flex; gap: 24px; }
  .stat { text-align: right; }
  .stat-val {
    font-family: var(--font-head);
    font-size: 20px; font-weight: 800;
    color: var(--accent); line-height: 1;
  }
  .stat-label {
    font-size: 10px; color: var(--muted);
    text-transform: uppercase; letter-spacing: 1px;
  }

  .sidebar {
    background: var(--surface);
    border-right: 1px solid var(--border);
    display: flex; flex-direction: column;
    overflow: hidden;
  }

  .sidebar-section {
    padding: 20px;
    border-bottom: 1px solid var(--border);
  }

  .sidebar-label {
    font-size: 10px; text-transform: uppercase;
    letter-spacing: 2px; color: var(--muted);
    margin-bottom: 14px;
    font-family: var(--font-head);
  }

  .chat-input-wrap { display: flex; flex-direction: column; gap: 10px; }

  textarea {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    color: var(--text);
    font-family: var(--font-mono);
    font-size: 13px;
    padding: 12px 14px;
    resize: none; height: 100px;
    transition: border-color 0.2s;
    outline: none; line-height: 1.6;
  }
  textarea:focus { border-color: var(--accent); }
  textarea::placeholder { color: var(--muted); }

  .send-btn {
    background: var(--accent);
    color: #0a0a0f;
    border: none; border-radius: var(--radius);
    font-family: var(--font-head);
    font-size: 13px; font-weight: 700;
    padding: 11px 20px; cursor: pointer;
    display: flex; align-items: center;
    justify-content: center; gap: 8px;
    letter-spacing: 0.5px;
    transition: all 0.15s;
    text-transform: uppercase;
  }
  .send-btn:hover:not(:disabled) {
    background: #f5ff7a;
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(232,255,71,0.3);
  }
  .send-btn:disabled { opacity: 0.5; cursor: not-allowed; }

  .spinner {
    width: 14px; height: 14px;
    border: 2px solid rgba(0,0,0,0.3);
    border-top-color: #000;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  .agent-response {
    background: rgba(71,255,224,0.04);
    border: 1px solid rgba(71,255,224,0.15);
    border-radius: var(--radius);
    font-size: 12px; line-height: 1.7;
    color: var(--accent2);
    padding: 16px; min-height: 60px;
    white-space: pre-wrap; word-break: break-word;
  }
  .agent-response.empty { color: var(--muted); font-style: italic; }

  .filter-tabs { display: flex; gap: 6px; }

  .tab {
    flex: 1; padding: 7px 10px;
    border-radius: 8px; border: 1px solid var(--border);
    background: transparent; color: var(--muted);
    font-family: var(--font-mono); font-size: 11px;
    cursor: pointer; text-transform: uppercase;
    letter-spacing: 0.5px; transition: all 0.15s;
  }
  .tab.active {
    background: var(--accent); color: #0a0a0f;
    border-color: var(--accent); font-weight: 700;
  }
  .tab:hover:not(.active) { border-color: var(--muted); color: var(--text); }

  .clear-btn {
    width: 100%; padding: 9px;
    border-radius: 8px;
    border: 1px solid rgba(255,71,71,0.3);
    background: transparent; color: var(--danger);
    font-family: var(--font-mono); font-size: 11px;
    cursor: pointer; text-transform: uppercase;
    letter-spacing: 1px; transition: all 0.15s;
  }
  .clear-btn:hover { background: rgba(255,71,71,0.1); border-color: var(--danger); }

  .main { display: flex; flex-direction: column; overflow: hidden; background: var(--bg); }

  .main-header {
    padding: 20px 28px 16px;
    border-bottom: 1px solid var(--border);
    display: flex; align-items: center; justify-content: space-between;
  }

  .main-title {
    font-family: var(--font-head);
    font-size: 22px; font-weight: 800; letter-spacing: -0.5px;
  }
  .main-title span { color: var(--accent); }

  .record-count {
    font-size: 11px; color: var(--muted);
    background: var(--surface);
    padding: 4px 12px; border-radius: 20px;
    border: 1px solid var(--border);
  }

  .history-list {
    flex: 1; overflow-y: auto;
    padding: 20px 28px;
    display: flex; flex-direction: column; gap: 12px;
  }
  .history-list::-webkit-scrollbar { width: 4px; }
  .history-list::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

  .email-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px; padding: 16px 20px;
    display: grid;
    grid-template-columns: auto 1fr auto;
    gap: 14px; align-items: start;
    transition: border-color 0.2s, transform 0.2s;
    animation: slideIn 0.3s ease;
  }
  @keyframes slideIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .email-card:hover { border-color: rgba(232,255,71,0.2); transform: translateX(2px); }
  .email-card.sent   { border-left: 3px solid var(--sent); }
  .email-card.failed { border-left: 3px solid var(--failed); }
  .email-card.info   { border-left: 3px solid var(--info); }

  .card-icon {
    width: 38px; height: 38px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0;
  }
  .card-icon.sent   { background: rgba(71,255,224,0.1); }
  .card-icon.failed { background: rgba(255,71,71,0.1); }
  .card-icon.info   { background: rgba(232,255,71,0.1); }

  .card-body { min-width: 0; }
  .card-user-msg {
    font-size: 13px; color: var(--text); margin-bottom: 6px;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }
  .card-agent-resp {
    font-size: 12px; color: var(--muted); line-height: 1.5;
    display: -webkit-box; -webkit-line-clamp: 2;
    -webkit-box-orient: vertical; overflow: hidden;
  }
  .card-recipient {
    display: inline-flex; align-items: center; gap: 5px;
    font-size: 11px; color: var(--accent2);
    background: rgba(71,255,224,0.08);
    padding: 2px 8px; border-radius: 4px; margin-top: 6px;
  }

  .card-meta { text-align: right; flex-shrink: 0; }
  .card-time { font-size: 11px; color: var(--muted); white-space: nowrap; }

  .badge {
    display: inline-block; padding: 3px 8px;
    border-radius: 6px; font-size: 10px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.5px; margin-top: 6px;
  }
  .badge.sent   { background: rgba(71,255,224,0.15); color: var(--sent); }
  .badge.failed { background: rgba(255,71,71,0.15);  color: var(--failed); }
  .badge.info   { background: rgba(232,255,71,0.15); color: var(--info); }

  .empty-state {
    flex: 1; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    gap: 12px; color: var(--muted);
  }
  .empty-icon { font-size: 48px; opacity: 0.3; }
  .empty-text { font-family: var(--font-head); font-size: 16px; font-weight: 600; }
  .empty-sub { font-size: 12px; text-align: center; max-width: 260px; line-height: 1.6; }
`

function formatTime(iso) {
  const d = new Date(iso)
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) +
    ' · ' + d.toLocaleDateString([], { month: 'short', day: 'numeric' })
}

function EmailCard({ record }) {
  const icons = { sent: '✉️', failed: '⚠️', info: '🤖' }
  return (
    <div className={`email-card ${record.status}`}>
      <div className={`card-icon ${record.status}`}>
        {icons[record.status] || '💬'}
      </div>
      <div className="card-body">
        <div className="card-user-msg">"{record.user_message}"</div>
        <div className="card-agent-resp">{record.agent_response}</div>
        {record.recipient && (
          <div className="card-recipient">📬 {record.recipient}</div>
        )}
      </div>
      <div className="card-meta">
        <div className="card-time">{formatTime(record.timestamp)}</div>
        <div className={`badge ${record.status}`}>{record.status}</div>
      </div>
    </div>
  )
}

export default function App() {
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [agentReply, setAgentReply] = useState('')
  const [history, setHistory] = useState([])
  const [filter, setFilter] = useState('all')
  const bottomRef = useRef(null)

  const fetchHistory = async () => {
    try {
      const res = await axios.get(`${API}/history`)
      setHistory(res.data)
    } catch (e) {
      console.error('Could not fetch history', e)
    }
  }

  useEffect(() => { fetchHistory() }, [])
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [history])

  const handleSend = async () => {
    if (!message.trim() || loading) return
    setLoading(true)
    setAgentReply('')
    try {
      const res = await axios.post(`${API}/chat`, { message })
      setAgentReply(res.data.response)
      setHistory(prev => [...prev, res.data.record])
      setMessage('')
    } catch (e) {
      const err = e.response?.data?.detail || 'Connection error. Is the backend running?'
      setAgentReply('⚠️ ' + err)
    } finally {
      setLoading(false)
    }
  }

  const handleClear = async () => {
    await axios.delete(`${API}/history`)
    setHistory([])
    setAgentReply('')
  }

  const filtered = filter === 'all' ? history : history.filter(r => r.status === filter)
  const sentCount = history.filter(r => r.status === 'sent').length
  const failedCount = history.filter(r => r.status === 'failed').length

  return (
    <>
      <style>{styles}</style>
      <div className="app">

        <header className="header">
          <div className="header-brand">
            <div className="header-logo">⚡</div>
            <div className="header-title">Ishwar's <span>Email Agent</span></div>
          </div>
          <div className="header-status">
            <div className="status-dot" />
            Agent Online
          </div>
          <div className="header-stats">
            <div className="stat">
              <div className="stat-val">{sentCount}</div>
              <div className="stat-label">Sent</div>
            </div>
            <div className="stat">
              <div className="stat-val" style={{ color: failedCount > 0 ? 'var(--danger)' : 'var(--accent)' }}>
                {failedCount}
              </div>
              <div className="stat-label">Failed</div>
            </div>
            <div className="stat">
              <div className="stat-val">{history.length}</div>
              <div className="stat-label">Total</div>
            </div>
          </div>
        </header>

        <aside className="sidebar">
          <div className="sidebar-section">
            <div className="sidebar-label">Compose Message</div>
            <div className="chat-input-wrap">
              <textarea
                value={message}
                onChange={e => setMessage(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && e.ctrlKey && handleSend()}
                placeholder={'Send an email to alice@example.com\ntelling her the meeting is at 3pm'}
              />
              <button className="send-btn" onClick={handleSend} disabled={loading || !message.trim()}>
                {loading ? <><div className="spinner" /> Processing...</> : <>⚡ Send (Ctrl+Enter)</>}
              </button>
            </div>
          </div>

          <div className="sidebar-section">
            <div className="sidebar-label">Agent Response</div>
            <div className={`agent-response ${!agentReply ? 'empty' : ''}`}>
              {agentReply || 'Agent reply will appear here…'}
            </div>
          </div>

          <div className="sidebar-section">
            <div className="sidebar-label">Filter History</div>
            <div className="filter-tabs">
              {['all', 'sent', 'failed', 'info'].map(f => (
                <button key={f} className={`tab ${filter === f ? 'active' : ''}`} onClick={() => setFilter(f)}>
                  {f}
                </button>
              ))}
            </div>
          </div>

          <div className="sidebar-section">
            <button className="clear-btn" onClick={handleClear}>⊘ Clear all history</button>
          </div>
        </aside>

        <main className="main">
          <div className="main-header">
            <div className="main-title">Email <span>History Log</span></div>
            <div className="record-count">{filtered.length} records</div>
          </div>

          {filtered.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">📭</div>
              <div className="empty-text">No records yet</div>
              <div className="empty-sub">
                Type a message in the sidebar to send your first email via the AI agent.
              </div>
            </div>
          ) : (
            <div className="history-list">
              {[...filtered].reverse().map(record => (
                <EmailCard key={record.id} record={record} />
              ))}
              <div ref={bottomRef} />
            </div>
          )}
        </main>

      </div>
    </>
  )
}
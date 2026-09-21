import { useState } from 'react'
import { SendHorizonal } from 'lucide-react'
import './styles.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? ''

function App() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Welcome to WayFinder. Ask me anything and I will help you find the next step.' },
  ])
  const [input, setInput] = useState('')
  const [isSending, setIsSending] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(event) {
    event.preventDefault()

    const trimmedInput = input.trim()
    if (!trimmedInput || isSending) return

    const userMessage = { role: 'user', content: trimmedInput }
    const nextMessages = [...messages, userMessage]
    setMessages([...nextMessages, { role: 'assistant', content: '' }])
    setInput('')
    setError('')
    setIsSending(true)

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: nextMessages }),
      })

      if (!response.ok || !response.body) {
        throw new Error('The backend did not return a usable response.')
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value, { stream: true })
        setMessages((currentMessages) => {
          const updatedMessages = [...currentMessages]
          const lastMessage = updatedMessages[updatedMessages.length - 1]
          updatedMessages[updatedMessages.length - 1] = {
            ...lastMessage,
            content: lastMessage.content + chunk,
          }
          return updatedMessages
        })
      }
    } catch (caughtError) {
      setError(caughtError.message)
      setMessages((currentMessages) => currentMessages.slice(0, -1))
    } finally {
      setIsSending(false)
    }
  }

  return (
    <main className="app-shell">
      <section className="chat-panel" aria-label="WayFinder chat">
        <header className="chat-header">
          <div>
            <p className="eyebrow">WayFinder</p>
            <h1>AI conversation pathfinder</h1>
          </div>
          <span className="status-pill">Local</span>
        </header>

        <div className="messages" aria-live="polite">
          {messages.map((message, index) => (
            <article className={`message ${message.role}`} key={`${message.role}-${index}`}>
              <div className="message-label">{message.role === 'user' ? 'You' : 'WayFinder'}</div>
              <p>{message.content || 'Thinking...'}</p>
            </article>
          ))}
        </div>

        {error && <p className="error-message">{error}</p>}

        <form className="composer" onSubmit={handleSubmit}>
          <textarea
            aria-label="Message"
            value={input}
            onChange={(event) => setInput(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault()
                event.currentTarget.form.requestSubmit()
              }
            }}
            placeholder="Ask WayFinder..."
            rows="2"
          />
          <button type="submit" disabled={isSending || !input.trim()} aria-label="Send message">
            <SendHorizonal size={20} aria-hidden="true" />
          </button>
        </form>
      </section>
    </main>
  )
}

export default App
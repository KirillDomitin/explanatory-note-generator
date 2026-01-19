import { useState } from 'react'
const APP_VERSION = import.meta.env.VITE_APP_VERSION

function App() {
  const [inn, setInn] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [downloadLink, setDownloadLink] = useState(null)
  const [generatedFileName, setGeneratedFileName] = useState('')


  const generate = async () => {
    if (!inn.trim() || inn.length !== 10 && inn.length !== 12) {
      setMessage('ИНН должен быть 10 или 12 цифр')
      return
    }

    setLoading(true)
    setMessage('')
    setDownloadLink(null)

    try {
      const res = await fetch(`/api/v1/generate/?inn=${inn}`)

      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || 'Ошибка сервера')
      }

      const blob = await res.blob()
      const url = URL.createObjectURL(blob)
      setGeneratedFileName(`Пояснения_${inn}.docx`)
      setDownloadLink(url)
      setInn(``)
      setMessage('Файл готов!')
    } catch (err) {
      setMessage(`Ошибка: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: '40px', maxWidth: '500px', margin: '0 auto' }}>
      <h1>Генератор пояснительной записки</h1>

      <input
        type="text"
        value={inn}
        onChange={e => setInn(e.target.value.replace(/\D/g, ''))} // только цифры
        placeholder="Введите ИНН"
        maxLength={12}
        style={{ width: '100%', padding: '12px', fontSize: '18px', marginBottom: '20px' }}
      />

      <button
        onClick={generate}
        disabled={loading || !inn.trim()}
        style={{
          padding: '12px 24px',
          fontSize: '18px',
          background: loading ? '#ccc' : '#4CAF50',
          color: 'white',
          border: 'none',
          borderRadius: '6px',
          cursor: loading ? 'not-allowed' : 'pointer'
        }}
      >
        {loading ? 'Генерируется...' : 'Сгенерировать'}
      </button>

      {message && (
        <p style={{ marginTop: '20px', color: message.includes('Ошибка') ? 'red' : 'green' }}>
          {message}
        </p>
      )}

      {downloadLink && (
        <div style={{ marginTop: '20px' }}>
          <a
            href={downloadLink}
            download={generatedFileName}
            style={{ color: '#0066cc', fontSize: '18px', textDecoration: 'underline' }}
          >
            Скачать готовый файл ({generatedFileName})
          </a>
        </div>
      )}
      <footer style={{ textAlign: 'center', padding: '12px', fontSize: '12px', color: '#999'}}>
        v{APP_VERSION}
      </footer>
    </div>
  )
}

export default App
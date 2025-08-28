import './globals.css'

export const metadata = {
  title: 'Music Genre Classifier',
  description: 'AI-powered music genre classification using Ollama',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  )
}

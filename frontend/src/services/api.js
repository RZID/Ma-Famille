import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 8000,
})

export async function fetchHealth() {
  const res = await api.get('/api/v1/health')
  return res.data
}

export async function fetchRoot() {
  const res = await api.get('/')
  return res.data
}

export default api

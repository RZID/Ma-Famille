import { defineStore } from 'pinia'
import { ref } from 'vue'

import { fetchHealth } from '../services/api.js'

// App-level store (foundation). Domain stores (venue, court, booking...)
// will live next to this file in follow-up iterations.
export const useAppStore = defineStore('app', () => {
  const backendStatus = ref('unknown')
  const backendService = ref('')
  const lastChecked = ref(null)
  const loading = ref(false)
  const error = ref('')

  async function checkBackend() {
    loading.value = true
    error.value = ''
    try {
      const data = await fetchHealth()
      backendStatus.value = data.status ?? 'unknown'
      backendService.value = data.service ?? ''
      lastChecked.value = new Date().toISOString()
    } catch (e) {
      backendStatus.value = 'unreachable'
      error.value = e?.message ?? 'Failed to reach backend'
    } finally {
      loading.value = false
    }
  }

  return { backendStatus, backendService, lastChecked, loading, error, checkBackend }
})

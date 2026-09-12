<script setup>
import { onMounted } from 'vue'
import { useAppStore } from '../stores/app.js'

const store = useAppStore()

onMounted(() => {
  store.checkBackend()
})
</script>

<template>
  <section class="card">
    <h2>Backend connectivity</h2>
    <p>
      Service: <code>{{ store.backendService || 'ma-famille-api' }}</code>
      · status: <strong>{{ store.backendStatus }}</strong>
    </p>
    <p v-if="store.lastChecked">
      <small>last checked: {{ store.lastChecked }}</small>
    </p>
    <p v-if="store.error" class="error">
      {{ store.error }}
    </p>
    <button :disabled="store.loading" @click="store.checkBackend()">
      {{ store.loading ? 'Checking…' : 'Re-check' }}
    </button>
  </section>
</template>

<style scoped>
.card {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  margin-top: 16px;
}
.error {
  color: #dc2626;
}
button {
  margin-top: 8px;
  padding: 8px 14px;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  cursor: pointer;
}
</style>

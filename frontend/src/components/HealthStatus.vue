<script setup>
import { onMounted } from 'vue'
import { useAppStore } from '../stores/app.js'

const store = useAppStore()

onMounted(() => {
  store.checkBackend()
})
</script>

<template>
  <section class="mt-4 rounded-lg border border-gray-200 p-4">
    <h2 class="mb-2 text-lg font-medium">Backend connectivity</h2>
    <p class="text-sm text-gray-700">
      Service: <code class="rounded bg-gray-100 px-1.5 py-0.5 font-mono text-[13px]">{{ store.backendService || 'ma-famille-api' }}</code>
      · status: <strong>{{ store.backendStatus }}</strong>
    </p>
    <p v-if="store.lastChecked" class="mt-1 text-xs text-gray-500">
      last checked: {{ store.lastChecked }}
    </p>
    <p v-if="store.error" class="mt-1 text-sm text-red-600">
      {{ store.error }}
    </p>
    <button
      :disabled="store.loading"
      class="mt-2 rounded-md border border-gray-300 px-3.5 py-2 text-sm hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-60"
      @click="store.checkBackend()"
    >
      {{ store.loading ? 'Checking…' : 'Re-check' }}
    </button>
  </section>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAppStore } from '../stores/app.js'

const store = useAppStore()

const dotClass = computed(() => {
  if (store.backendStatus === 'ok') return 'bg-green-600'
  if (store.backendStatus === 'unknown') return 'bg-gray-400'
  return 'bg-red-600'
})

onMounted(() => {
  store.checkBackend()
})
</script>

<template>
  <header class="flex items-center gap-4 border-b border-gray-200 px-4 py-3">
    <RouterLink to="/" class="font-bold text-gray-900 no-underline">ma-famille</RouterLink>
    <nav class="flex flex-1 gap-3">
      <RouterLink to="/" class="text-gray-600 no-underline hover:text-gray-900" active-class="font-semibold text-gray-900!">Home</RouterLink>
      <RouterLink to="/health" class="text-gray-600 no-underline hover:text-gray-900" active-class="font-semibold text-gray-900!">Health</RouterLink>
    </nav>
    <span :class="['h-2.5 w-2.5 rounded-full', dotClass]" :title="`backend: ${store.backendStatus}`" />
  </header>
</template>

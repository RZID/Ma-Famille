<script setup>
import { computed, onMounted } from 'vue'
import { useAppStore } from '../stores/app.js'

const store = useAppStore()

const dotClass = computed(() => {
  if (store.backendStatus === 'ok') return 'dot ok'
  if (store.backendStatus === 'unknown') return 'dot idle'
  return 'dot bad'
})

onMounted(() => {
  store.checkBackend()
})
</script>

<template>
  <header class="nav">
    <RouterLink to="/" class="brand">ma-famille</RouterLink>
    <nav class="links">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/health">Health</RouterLink>
    </nav>
    <span :class="dotClass" :title="`backend: ${store.backendStatus}`" />
  </header>
</template>

<style scoped>
.nav {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 16px;
  border-bottom: 1px solid #e5e7eb;
}
.brand {
  font-weight: 700;
  text-decoration: none;
  color: inherit;
}
.links {
  display: flex;
  gap: 12px;
  flex: 1;
}
.links a {
  text-decoration: none;
  color: #374151;
}
.links a.router-link-active {
  font-weight: 600;
  color: #111827;
}
.dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: #9ca3af;
}
.dot.ok {
  background: #16a34a;
}
.dot.bad {
  background: #dc2626;
}
</style>

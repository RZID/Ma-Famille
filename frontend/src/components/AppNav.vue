<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useAppStore } from '../stores/app.js'
import '../styles/header.css'

const store = useAppStore()
const isSidebarOpen = ref(false)

const dotClass = computed(() => {
  if (store.backendStatus === 'ok') return 'bg-green-600'
  if (store.backendStatus === 'unknown') return 'bg-gray-400'
  return 'bg-red-600'
})

onMounted(() => {
  store.checkBackend()
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})

function toggleSidebar() {
  isSidebarOpen.value = !isSidebarOpen.value
}

function closeSidebar() {
  isSidebarOpen.value = false
}

function handleKeydown(event) {
  if (event.key === 'Escape') closeSidebar()
}
</script>

<template>
  <header class="app-header">
    <div class="app-header-bar flex items-center justify-between border-b px-4 py-3">
      <RouterLink to="/" class="app-header-brand font-bold no-underline">Ma-Famille</RouterLink>
      <div class="flex items-center gap-4">
        <span :class="['h-2.5 w-2.5 rounded-full', dotClass]" :title="`backend: ${store.backendStatus}`" />
        <button
          type="button"
          class="app-header-menu-button rounded-lg p-2 transition focus:outline-none focus:ring-2 focus:ring-gray-400"
          aria-label="Open menu"
          :aria-expanded="isSidebarOpen"
          aria-controls="app-sidebar"
          @click="toggleSidebar"
        >
          <span class="flex flex-col items-center gap-1" aria-hidden="true">
            <span class="h-1 w-1 rounded-full bg-current" />
            <span class="h-1 w-1 rounded-full bg-current" />
            <span class="h-1 w-1 rounded-full bg-current" />
          </span>
        </button>
      </div>
    </div>

    <div
      v-if="isSidebarOpen"
      class="app-header-backdrop fixed inset-0 z-40"
      aria-hidden="true"
      @click="closeSidebar"
    />

    <aside
      id="app-sidebar"
      class="app-sidebar fixed right-0 top-0 z-50 flex h-full w-72 max-w-[85vw] flex-col border-l p-6 shadow-xl"
      :class="{ 'is-open': isSidebarOpen }"
      :aria-hidden="!isSidebarOpen"
      :inert="!isSidebarOpen"
    >
      <div class="mb-8 flex items-center justify-between">
        <h2 class="text-lg font-semibold text-gray-900">Menu</h2>
        <button
          type="button"
          class="rounded-lg p-2 text-gray-600 transition hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-400"
          aria-label="Close menu"
          @click="closeSidebar"
        >
          <span class="text-2xl leading-none" aria-hidden="true">&times;</span>
        </button>
      </div>

      <nav class="flex flex-col gap-2">
        <RouterLink to="/" class="app-sidebar-link rounded-lg px-3 py-2 no-underline" @click="closeSidebar">Home</RouterLink>
        <RouterLink to="/health" class="app-sidebar-link rounded-lg px-3 py-2 no-underline" @click="closeSidebar">Health</RouterLink>
        <button type="button" class="app-sidebar-link rounded-lg px-3 py-2 text-left">Log out</button>
      </nav>
    </aside>
  </header>
</template>

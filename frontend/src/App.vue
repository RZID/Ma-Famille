<script setup>
import AppNav from './components/AppNav.vue'
</script>

<template>
  <div class="flex min-h-screen flex-col bg-white text-gray-900">
    <AppNav />
    <main class="mx-auto w-full max-w-4xl flex-1 px-4 py-6">
      <RouterView />
    </main>
    <footer class="border-t border-gray-200 py-4 text-center text-sm text-gray-500">
      ma-famille · Sports Venue Booking · foundation iteration
    </footer>
  </div>
</template>

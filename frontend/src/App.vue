<script setup>
import AppNav from './components/AppNav.vue'
</script>

<template>
  <AppNav />
  <main class="container">
    <RouterView />
  </main>
  <footer class="footer">
    <small>ma-famille · Sports Venue Booking · foundation iteration</small>
  </footer>
</template>

<style scoped>
.container {
  max-width: 960px;
  margin: 0 auto;
  padding: 24px 16px;
  min-height: 70vh;
}
.footer {
  text-align: center;
  padding: 16px;
  color: #6b7280;
  border-top: 1px solid #e5e7eb;
}
</style>

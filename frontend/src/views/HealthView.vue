<script setup>
import HealthStatus from '../components/HealthStatus.vue'
</script>

<template>
  <section>
    <h1>Health</h1>
    <p>Verifies <code>GET /api/v1/health</code> on the FastAPI backend.</p>
    <HealthStatus />
  </section>
</template>

<script setup>
import HealthStatus from '../components/HealthStatus.vue'
</script>

<template>
  <section class="space-y-3">
    <h1 class="text-3xl font-semibold tracking-tight">Health</h1>
    <p class="text-gray-600">Verifies <code class="rounded bg-gray-100 px-1.5 py-0.5 font-mono text-[13px]">GET /api/v1/health</code> on the FastAPI backend.</p>
    <HealthStatus />
  </section>
</template>

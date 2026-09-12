<template>
  <section class="space-y-4">
    <h1 class="text-3xl font-semibold tracking-tight">Sports Venue Booking</h1>
    <p class="text-gray-600">
      Foundation iteration — mono-repo structure, API client, and health check only.
      Domain entities (<code class="rounded bg-gray-100 px-1.5 py-0.5 font-mono text-[13px]">Venue</code>,
      <code class="rounded bg-gray-100 px-1.5 py-0.5 font-mono text-[13px]">Court</code>,
      <code class="rounded bg-gray-100 px-1.5 py-0.5 font-mono text-[13px]">Slot</code>,
      <code class="rounded bg-gray-100 px-1.5 py-0.5 font-mono text-[13px]">Booking</code>,
      <code class="rounded bg-gray-100 px-1.5 py-0.5 font-mono text-[13px]">Payment</code>) land in follow-up iterations.
    </p>
    <ul class="list-disc space-y-1 pl-5 text-gray-700">
      <li>Customer books a court.</li>
      <li>Venue Manager manages courts, pricing, schedules.</li>
    </ul>
    <p>
      <RouterLink to="/health" class="font-medium text-blue-600 hover:underline">Check backend health →</RouterLink>
    </p>
  </section>
</template>

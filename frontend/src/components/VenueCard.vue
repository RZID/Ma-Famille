<script setup>
import '../styles/venue-card.css'

defineProps({
  image: { type: String, default: '' },
  title: { type: String, default: '' },
  location: { type: String, default: '' },
  openTime: { type: String, default: '' },
  closeTime: { type: String, default: '' },
  tags: { type: Array, default: () => [] },
})
</script>

<template>
  <article class="venue-card">
    <div class="venue-card-image">
      <img v-if="image" :src="image" :alt="title" class="venue-card-image-el" />
    </div>

    <div class="venue-card-body">
      <h3 class="venue-card-title">{{ title }}</h3>
      <p class="venue-card-location">{{ location }}</p>

      <div class="venue-card-hours">
        <svg
          class="venue-card-clock-icon"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          aria-hidden="true"
        >
          <circle cx="12" cy="12" r="9" />
          <path d="M12 7v5l3 2" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
        <span class="venue-card-hours-text">{{ openTime }} - {{ closeTime }}</span>
      </div>

      <div class="venue-card-tags">
        <span v-for="tag in tags" :key="tag" class="venue-card-tag">{{ tag }}</span>
      </div>

      <div class="venue-card-divider" aria-hidden="true" />

      <div class="venue-card-action">
        <button type="button" class="venue-card-button">Check availability</button>
      </div>
    </div>
  </article>
</template>

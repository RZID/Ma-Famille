<script setup>
import mapOfJakartaCinere from '../assets/MapofJakartaCinere.svg'
import '../styles/location.css'
</script>

<template>
  <section class="location-panel" aria-labelledby="location-panel-title">
    <h2 id="location-panel-title" class="location-panel-title">Map & Filter</h2>

    <div class="location-layout">
      <div class="location-preview">
        <div class="location-map-frame">
          <img
            :src="mapOfJakartaCinere"
            alt="Map showing the Jakarta and Cinere area"
            class="location-map-image"
          />
        </div>
        <button type="button" class="location-button">See all locations</button>
      </div>

      <div class="location-filter" aria-label="Location filter, coming soon" />
    </div>
  </section>
</template>
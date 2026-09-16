<script setup>
import { reactive } from 'vue'
import '../styles/venue-filters.css'

const filterGroups = [
  {
    key: 'venueType',
    title: 'Venue Type',
    options: ['Padel court', 'Private Office', 'Cafe'],
  },
  {
    key: 'areaType',
    title: 'Area Type',
    options: ['Outdoors', 'Indoors', 'Open Concept'],
  },
  {
    key: 'popularFor',
    title: 'Popular For',
    options: ['Birthdays', 'Corporate', 'Event'],
  },
]

const selectedFilters = reactive({
  venueType: [],
  areaType: [],
  popularFor: [],
})
</script>

<template>
  <div class="venue-filters" aria-label="Venue filters">
    <fieldset v-for="(group, groupIndex) in filterGroups" :key="group.key" class="venue-filter-group">
      <legend class="venue-filter-title">{{ group.title }}</legend>

      <div class="venue-filter-options">
        <label v-for="option in group.options" :key="option" class="venue-filter-option">
          <input v-model="selectedFilters[group.key]" type="checkbox" :value="option" />
          <span class="venue-filter-checkbox" aria-hidden="true" />
          <span>{{ option }}</span>
        </label>
      </div>

      <div v-if="groupIndex < filterGroups.length - 1" class="venue-filter-divider" aria-hidden="true" />
    </fieldset>
  </div>
</template>
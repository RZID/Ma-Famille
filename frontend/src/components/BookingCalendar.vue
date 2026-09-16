<script setup>
import { computed, ref } from 'vue'
import '../styles/calendar.css'

const today = new Date()
const selectedDate = ref(createDate(today))
const displayedMonth = ref(new Date(today.getFullYear(), today.getMonth(), 1))
const currentMonth = new Date(today.getFullYear(), today.getMonth(), 1)

const isPreviousMonthDisabled = computed(() => displayedMonth.value <= currentMonth)

const monthLabel = computed(() => displayedMonth.value.toLocaleDateString('en-US', {
  month: 'long',
  year: 'numeric',
}))

const calendarDays = computed(() => {
  const year = displayedMonth.value.getFullYear()
  const month = displayedMonth.value.getMonth()
  const firstDayIndex = (new Date(year, month, 1).getDay() + 6) % 7
  const daysInMonth = new Date(year, month + 1, 0).getDate()

  return Array.from({ length: 42 }, (_, index) => {
    const dayNumber = index - firstDayIndex + 1
    if (dayNumber < 1 || dayNumber > daysInMonth) return null

    const date = new Date(year, month, dayNumber)
    return {
      date,
      dayNumber,
      isToday: isSameDate(date, today),
      isSelected: isSameDate(date, selectedDate.value),
    }
  })
})

function createDate(date) {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate())
}

function isSameDate(firstDate, secondDate) {
  return firstDate.toDateString() === secondDate.toDateString()
}

function changeMonth(monthOffset) {
  if (monthOffset < 0 && isPreviousMonthDisabled.value) return

  displayedMonth.value = new Date(
    displayedMonth.value.getFullYear(),
    displayedMonth.value.getMonth() + monthOffset,
    1,
  )
}

function selectDate(day) {
  if (day) selectedDate.value = day.date
}
</script>

<template>
  <section class="calendar" aria-labelledby="calendar-title">
    <div class="calendar-header">
      <div>
        <p class="calendar-eyebrow">Availability</p>
        <h2 id="calendar-title" class="calendar-title">Choose a date</h2>
      </div>
      <div class="calendar-navigation">
        <button
          type="button"
          class="calendar-nav-button"
          aria-label="Previous month unavailable"
          :disabled="isPreviousMonthDisabled"
          @click="changeMonth(-1)"
        >
          <span aria-hidden="true">&#8249;</span>
        </button>
        <p class="calendar-month" aria-live="polite">{{ monthLabel }}</p>
        <button type="button" class="calendar-nav-button" aria-label="Next month" @click="changeMonth(1)">
          <span aria-hidden="true">&#8250;</span>
        </button>
      </div>
    </div>

    <div class="calendar-weekdays" aria-hidden="true">
      <span v-for="weekday in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']" :key="weekday">
        {{ weekday }}
      </span>
    </div>

    <div class="calendar-grid" role="grid" aria-label="Calendar dates">
      <button
        v-for="(day, index) in calendarDays"
        :key="day ? day.date.toISOString() : `empty-${index}`"
        type="button"
        class="calendar-day"
        :class="{ 'is-today': day?.isToday, 'is-selected': day?.isSelected }"
        :disabled="!day"
        :aria-label="day ? day.date.toLocaleDateString('en-US', { dateStyle: 'full' }) : undefined"
        :aria-pressed="day?.isSelected"
        @click="selectDate(day)"
      >
        <span class="calendar-day-number">{{ day?.dayNumber }}</span>
      </button>
    </div>

    <p class="calendar-selection" aria-live="polite">
      Selected: {{ selectedDate.toLocaleDateString('en-US', { dateStyle: 'long' }) }}
    </p>
  </section>
</template>
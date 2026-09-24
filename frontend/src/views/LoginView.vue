<script setup>
import { ref } from 'vue'
import loginBackground from '../assets/loginbg.avif'
import '../styles/login.css'

const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const submitted = ref(false)

function handleSubmit() {
  submitted.value = true
}
</script>

<template>
  <section class="login-page relative isolate -mx-4 -my-6 flex min-h-[calc(100vh-10rem)] max-w-none items-center justify-center overflow-hidden px-4 py-10">
    <div
      class="absolute inset-0 -z-20 bg-cover bg-center bg-no-repeat"
      :style="{ backgroundImage: `url(${loginBackground})` }"
      aria-hidden="true"
    />
    <div class="login-overlay absolute inset-0 -z-10" aria-hidden="true" />

    <div class="w-full max-w-md space-y-8">
      <div class="space-y-3 text-center">
        <p class="login-eyebrow text-sm font-semibold uppercase tracking-[0.2em]">Welcome,</p>
        <h1 class="login-title text-3xl tracking-tight">Ma Famille!</h1>
        <p class="login-description">Book your next court session in a few clicks</p>
      </div>

      <form class="login-card space-y-5 rounded-2xl border p-6 shadow-sm" @submit.prevent="handleSubmit">
        <div class="space-y-2">
          <label for="email" class="login-label block text-sm font-medium">Email address</label>
          <input
            id="email"
            v-model="email"
            type="email"
            name="email"
            autocomplete="email"
            required
            placeholder="you@example.com"
            class="login-input w-full rounded-lg border px-3 py-2.5 outline-none transition"
          />
        </div>

        <div class="space-y-2">
          <label for="password" class="login-label block text-sm font-medium">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            name="password"
            autocomplete="current-password"
            required
            placeholder="Enter your password"
            class="login-input w-full rounded-lg border px-3 py-2.5 outline-none transition"
          />
        </div>

        <div class="flex items-center justify-between gap-4 text-sm">
          <label class="login-body-text flex items-center gap-2">
            <input v-model="rememberMe" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
            Remember me
          </label>
          <a href="#" class="login-link font-medium">Forgot password?</a>
        </div>

        <button
          type="submit"
          class="login-button w-full rounded-lg px-4 py-2.5 font-semibold transition"
        >
          Sign in
        </button>

        <p v-if="submitted" class="login-body-text text-center text-sm" role="status">
          Login connection is ready for backend integration.
        </p>
      </form>

      <p class="login-body-text-acc text-center text-sm">
        Don't have an account?
        <a href="#" class="login-link font-semibold">Create one</a>
      </p>
    </div>
  </section>
</template>
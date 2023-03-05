<template>
  <layout title="Login">
    <div class="flex-1 flex flex-col justify-center py-12 px-4 sm:px-6 lg:flex-none lg:px-20 xl:px-24">
      <div class="mx-auto w-full max-w-sm lg:w-96">
        <div>
          <img
            class="h-20 w-auto"
            :src="$page.props.globalSettings.appLogo"
            :alt="$page.props.globalSettings.appName"
          >
          <h2 class="mt-6 text-2xl font-extrabold text-gray-900">
            {{ $_("Confirm Email") }}
          </h2>
        </div>

        <div class="mt-8">
          <p class="font-medium text-red-600 leading-relaxed">
            {{ $_("Your token is invalid or was expired.") }}
          </p>
          <p class="pt-4 leading-relaxed">
            {{ $_("To send another confirmation email, click") }}
            <inertia-link
              :href="route('accounts:email_verification_sent')"
              class="font-medium text-app-600 hover:text-app-500"
            >
              {{ $_("resend") }}
            </inertia-link>
          </p>
        </div>
      </div>
    </div>
  </layout>
</template>

<script>
import Layout from '@components/Layouts/LayoutAuth.vue'

export default {
  components: {
    Layout,
  },
}
</script>
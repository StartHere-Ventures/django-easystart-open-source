<template>
  <div class="min-h-screen bg-white flex flex-col justify-center py-8 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md -mt-48">
      <inertia-link
        :href="route('core:index')"
      >
        <img
          class="mx-auto h-20 w-auto"
          :src="$page.props.global_settings.appLogo"
          :alt="$page.props.global_settings.appName"
        >
      </inertia-link>
    </div>
    <div class="mt-8 sm:mx-auto sm:w-full">
      <slot name="content" />
    </div>
    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <p class="text-app-600 text-center flex justify-center">
        <inertia-link
          :href="route('core:index')"
          class="text-app-600 hover:text-app-500"
        >
          {{ $_("Go back home") }}
        </inertia-link>
        <ArrowNarrowRightIcon class="ml-2 h-4 w-4" />
      </p>
    </div>
  </div>
</template>

<script>
import { ArrowNarrowRightIcon } from '@heroicons/vue/solid'

export default {
  components: {
    ArrowNarrowRightIcon
  },
  created() {
    if(this.$page.props.user_language){
      this.$setlang(this.$page.props.user_language)
    }
  }
}
</script>

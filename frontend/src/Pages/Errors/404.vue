<template>
  <layout>
    <template #content>
      <div>
        <p class="text-app-600 font-bold text-center">
          {{ $_('404 ERROR') }}
        </p>
        <p class="pt-4 text-5xl text-gray-900 font-bold text-center">
          {{ $_('Page not found') }}.
        </p>
        <p class="pt-4 text-gray-500 text-center">
          {{ $_("Sorry, we couldn't find the page you're looking for") }}.
        </p>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from '@components/Layouts/LayoutErrors.vue'
   
export default {
  name: 'Error404Page',
  components: {
    Layout,
  }
}
</script>
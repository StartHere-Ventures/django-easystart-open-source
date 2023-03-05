<template>
  <layout>
    <template #content>
      <div>
        <p class="text-app-600 font-bold text-center">
          {{ $_('500 ERROR') }}
        </p>
        <p class="pt-4 text-5xl text-gray-900 font-bold text-center">
          {{ $_('Internal server error') }}.
        </p>
        <p class="pt-4 text-gray-500 text-center">
          {{ $_("Something went wrong. Don't worry, it's not you, it's us") }}.
        </p>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from '@components/Layouts/LayoutErrors.vue'
   
export default {
  name: 'Error500Page',
  components: {
    Layout,
  }
}
</script>
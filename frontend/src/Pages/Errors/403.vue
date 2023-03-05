<template>
  <layout>
    <template #content>
      <div>
        <p class="text-app-600 font-bold text-center">
          {{ $_('403 ERROR') }}
        </p>
        <p class="pt-4 text-5xl text-gray-900 font-bold text-center">
          {{ $_('Access forbidden') }}.
        </p>
        <p class="pt-4 text-gray-500 text-center">
          {{ $_("You tried to access a page you did not have prior authorization for") }}.
        </p>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from '@components/Layouts/LayoutErrors.vue'
   
export default {
  name: 'Error403Page',
  components: {
    Layout,
  }
}
</script>
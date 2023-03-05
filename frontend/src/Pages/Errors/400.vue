<template>
  <layout>
    <template #content>
      <div>
        <p class="text-app-600 font-bold text-center">
          {{ $_('400 ERROR') }}
        </p>
        <p class="pt-4 text-5xl text-gray-900 font-bold text-center">
          {{ $_('Bad request') }}.
        </p>
        <p class="pt-4 text-gray-500 text-center">
          {{ $_("Your request resulted in a error") }}.
        </p>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from '@components/Layouts/LayoutErrors.vue'
   
export default {
  name: 'Error400Page',
  components: {
    Layout,
  }
}
</script>
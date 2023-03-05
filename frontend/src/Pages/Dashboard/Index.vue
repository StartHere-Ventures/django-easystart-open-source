<template>
  <layout nav-active="home">
    <template #content>
      <div class="px-4 sm:px-6 md:px-0">
        <h1 class="text-3xl font-extrabold text-gray-900">
          Dashboard
        </h1>
      </div>
      <div class="px-4 sm:px-6 md:px-0">
        <div class="py-6">
          {{ $_("Welcome to") }} <span class="font-medium">easystart</span>, {{ $page.props.auth.user.email }}!
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from '@components/Layouts/Layout.vue'

export default {
  name: 'IndexPage',
  components: {
    Layout,
  },
}
</script>

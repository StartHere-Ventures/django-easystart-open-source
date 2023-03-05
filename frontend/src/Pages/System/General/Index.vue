<template>
  <layout tabs-active="general">
    <template #settings-content>
      <appearance
        :app-name="globalSettings.appName"
        :app-logo="globalSettings.appLogo"
        :flash="flash"
        :errors="errors"
      />

      <registration
        :flash="flash"
        :errors="errors"
        :registration-active="globalSettings.activeRegistration"
      />
    </template>
  </layout>
</template>

<script>
import Layout from '@components/Layouts/LayoutGlobalSettings.vue'
import Appearance from './Appearance.vue'
import Registration from './Registration.vue'

export default {
  name: 'GeneralIndex',
  components: {
    Layout,
    Appearance,
    Registration,
  },
  props: {
    auth: {
      type: Object,
      default: () => { }
    },
    flash: {
      type: Object,
      default: () => { }
    },
    errors: {
      type: Object,
      default: () => { }
    },
    globalSettings: {
      type: Object,
      default: () => { }
    },
  }
}
</script>

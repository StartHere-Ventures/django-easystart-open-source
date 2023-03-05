<template>
  <layout tabs-active="security">
    <template #settings-content>
      <security
        :session-expire-time="globalSettings.timeExpiredSession"
        :flash="flash"
        :errors="errors"
      />
    </template>
  </layout>
</template>

<script>
import Layout from '@components/Layouts/LayoutGlobalSettings.vue'
import Security from './Security.vue'

export default {
  name: "SecurityIndex",
  components: {
    Layout,
    Security
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
    auditInstalled: {
      type: Boolean,
      default: () => false
    }
  }
}
</script>

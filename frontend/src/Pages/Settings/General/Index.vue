<template>
  <layout>
    <template #settings-content>
      <profile
        :auth="auth"
        :tfa="tfa"
        :success="success"
        :unconfirmed-email="unconfirmedEmail"
        :user-profile="userProfile"
        :max-size-file="maxSizeFile"
        :time-resend-email="timeResendEmail"
        :errors="errors"
      />

      <account
        :auth="auth"
        :success="success"
        :user-profile="userProfile"
        :available-languages="availableLanguages"
        :available-countries="availableCountries"
        :available-date-formats="availableDateFormats"
        :errors="errors"
      />
    </template>
  </layout>
</template>

<script>
import Layout from '@components/Layouts/LayoutSettings.vue'
import Profile from './Profile.vue'
import Account from './Account.vue'

export default {
  name: 'GeneralIndex',
  components: {
    Layout,
    Profile,
    Account
  },
  props: {
    auth: {
      type: Object,
      default: () => { }
    },
    tfa: {
      type: Object,
      default: () => {
        return {
          enabled: false,
          userSetup: false
        }
      }
    },
    success: {
      type: Object,
      default: () => { }
    },
    errors: {
      type: Object,
      default: () => { }
    },
    unconfirmedEmail: {
      type: String,
      default: () => ""
    },
    userProfile: {
      type: Object,
      default: () => { }
    },
    maxSizeFile: {
      type: Number,
      default: 10
    },
    availableLanguages: {
      type: Object,
      default: () => {}
    },
    availableCountries: {
      type: Object,
      default: () => { }
    },
    availableDateFormats: {
      type: Object,
      default: () => {}
    },
    timeResendEmail: {
      type: Number,
      default: () => 0
    },
  }
}
</script>

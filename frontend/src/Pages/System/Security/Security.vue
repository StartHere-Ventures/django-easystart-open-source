<template>
  <div>
    <div v-show="showNotification">
      <notification-success
        v-if="showNotification"
        :primary-text="textNotification"
        @show-notification="value => showNotification = value"
      />
    </div>
    <div class="mt-10 divide-y divide-gray-200">
      <div class="space-y-1">
        <h2 class="text-lg leading-6 font-medium text-gray-900">
          {{ $_("Security") }}
        </h2>
        <p class="max-w-2xl text-sm text-gray-500">
          {{ $_("Set security values") }}
        </p>
      </div>
      <div class="mt-6">
        <div class="divide-y divide-gray-200">
          <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4">
            <div class="text-sm font-medium text-gray-500">
              {{ $_("Session expiration time") }}
            </div>
            <div class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              <span
                v-if="!editExpireTime"
                class="flex-grow"
              >{{ sessionExpireTime }} min</span>
              <span
                v-else
                class="flex-grow"
              >
                <session-expired-time-form 
                  :success="success"
                  :errors="errors"
                  :time="sessionExpireTime"
                  @close-update-name="editExpireTime = false"
                  @show-notification="value => showNotification = value"
                  @text-notitication="text => textNotification = text"
                />
              </span>
              <span
                v-if="!editExpireTime"
                class="ml-4 flex-shrink-0"
              >
                <button
                  type="button"
                  class="bg-white rounded-md font-medium text-app-600 hover:text-app-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-app-500"
                  @click="editExpireTime = true"
                >
                  {{ $_("Update") }}
                </button>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NotificationSuccess from '@components/Utils/NotificationSuccess.vue'
import SessionExpireTimeForm from '@components/Forms/SystemExpiredSessionForm.vue'

export default {
  name: "SecuritySection",
  components: {
    'notification-success': NotificationSuccess,
    'session-expired-time-form': SessionExpireTimeForm,
  },
  props: {
    success: {
      type: Object,
      default: () => { }
    },
    errors: {
      type: Object,
      default: () => { }
    },
    sessionExpireTime: {
      type: Number,
      default: () => 60
    },
    auditActive: {
      type: Boolean,
      default: () => false
    },
    auditInstalled: {
      type: Boolean,
      default: () => false
    },
    ipAuthActive: {
      type: Boolean,
      default: () => false
    },
    captchaActive: {
      type: Boolean,
      default: () => false
    },
    tfaActive: {
      type: Boolean,
      default: () => false
    }
  },
  data () {
    return {
      showNotification: false,
      textNotification: "",
      editExpireTime: false,
    }
  },
  mounted (){
    if(this.success) {
      var vue = this;
      this.textNotification = this.success;
      this.showNotification = true
      setTimeout(function () { vue.showNotification = false }, 2000)
    }
  },
  methods: {
    changeAuditActive() {
      this.$inertia.get(this.route('management:system_active_audit'))
    },
    changeIPAuthActive() {
      this.$inertia.get(this.route('management:system_active_ip_auth'))
    },
    changeCaptchaActive() {
      this.$inertia.get(this.route('management:system_active_captcha'))
    },
    changeTFAActive() {
      this.$inertia.get(this.route('management:system_active_tfa'))
    }
  }
}
</script>

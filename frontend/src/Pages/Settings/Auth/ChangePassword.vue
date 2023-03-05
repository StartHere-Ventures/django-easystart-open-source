<template>
  <layout tabs-active="password">
    <template #settings-content>
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
            {{ $_('Change Password') }}
          </h2>
          <p class="max-w-2xl text-sm text-gray-500">
            {{ $_('Set up a new password') }}
          </p>
        </div>
        <div class="mt-6">
          <div class="divide-y divide-gray-200">
            <div 
              v-if="auth.emailAddress.emailMethod != 'none' && !$page.props.auth.emailAddress.verified"
              class="mx-auto py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4"
            >
              <div class="text-gray-500 sm:col-span-3">
                <p class="mb-2 leading-relaxed">
                  {{ $_("To do this operation need confirm your email.") }}
                </p>
              </div>
              <div class="mt-4 sm:mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-3">
                <button 
                  class="flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 bg-app-600 hover:bg-app-700 focus:ring-app-500"
                  :disabled="isSendingConfirmEmail"
                  @click="resendEmail"
                >
                  {{ $_("Resend confirm email") }}
                </button>
              </div>
              <div class="text-gray-500 sm:col-span-3">
                <p 
                  v-if="errorSendConfirmEmail"
                  class="mt-1 text-xs text-red-600"
                >
                  {{ $_(errorSendConfirmEmail) }}
                </p>
              </div>
              <div class="mt-4 sm:mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-3" />
            </div>
            <div
              v-else
              class="mx-auto py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4"
            >
              <div class="text-gray-500 sm:col-span-3">
                <p class="mb-2 leading-relaxed">
                  {{ $_("Need to change your password? We will send you a link to reset it.") }}
                </p>
              </div>
              <div class="mt-4 sm:mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-3">
                <button 
                  class="flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 bg-gray-600 hover:bg-gray-700 focus:ring-gray-500"
                  @click="resetPassword"
                >
                  {{ $_("Reset your password by email") }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from '@components/Layouts/LayoutSettings.vue'
import NotificationSuccess from '@components/Utils/NotificationSuccess.vue'

export default {
  components: {
    Layout,
    'notification-success': NotificationSuccess,
  },
  props: {
    auth: {
      type: Object,
      default: () => {}
    },
    flash: {
      type: Object,
      default: () => {}
    }
  },
  data () {
    return {
      isSendingConfirmEmail: false,
      errorSendConfirmEmail: '',
      isSendingPasswordReset: false,
      showNotification: false,
      textNotification: "",
    }
  },
  methods: {
    resendEmail(){
      this.$inertia.get(this.route("accounts:resend_email_verification"), { "email": this.auth.user.email }, {
        onStart: () => this.isSendingConfirmEmail = true,
        onFinish: () => {
          this.isSendingConfirmEmail = false;
          this.errorSendConfirmEmail = "";
          if (this.flash.success) {
            var vue = this;
            this.showNotification = true;
            this.textNotification = this.$_("Email send successfully");
            setTimeout(function () { vue.showNotification = false }, 2000)
          }
        }
      });
    },
    resetPassword() {
      this.sendEmailResetPassword();
    },
    sendEmailResetPassword(){
      this.$inertia.post(this.route("accounts:change_password"), { "email": this.auth.user.email }, {
        onStart: () => this.isSendingPasswordReset = true,
        onFinish: () => {
          this.isSendingPasswordReset = false;
          if (this.flash.success) {
            var vue = this;
            this.showNotification = true;
            this.textNotification = this.$_(this.flash.success);
            setTimeout(function () { vue.showNotification = false }, 2000)
          }
        }
      });
    }
  }
}
</script>

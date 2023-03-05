<template>
  <layout tabs-active="scripts">
    <template #settings-content>
      <div v-show="showNotification">
        <notification-success
          v-if="showNotification"
          :primary-text="textNotification"
          @show-notification="value => showNotification = value"
        />
      </div>
      <div>
        <div class="mt-10 divide-y divide-gray-200">
          <div class="space-y-1">
            <h2 class="text-lg leading-6 font-medium text-gray-900">
              {{ $_("Scripts") }}
            </h2>
            <p class="max-w-2xl text-sm text-gray-500">
              {{ $_("Insert scripts into header and footer") }}
            </p>
          </div>
          <div class="mt-6">
            <form @submit="onSubmit">
              <div class="divide-y divide-gray-200">
                <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4">
                  <div class="text-sm font-medium text-gray-500">
                    <label for="header-script">{{ $_("Scripts in Header") }}</label>
                  </div>
                  <div class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    <span
                      class="flex-grow"
                    >
                      <textarea-input 
                        name="header-script"
                        :value="form.header"
                        :error="fieldsErrors.header"
                        :text-error="fieldsErrors.header ? textErrors.header : ['']"
                        rows="10"
                        @input-return="value => form.header = value"
                      />
                      <p>
                        {{ $_("These script will be printed in the &#60;head&#62; section") }}
                      </p>
                    </span>
                  </div>
                </div>
                <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4">
                  <div class="text-sm font-medium text-gray-500">
                    <label for="body-script">{{ $_("Scripts in Body") }}</label>
                  </div>
                  <div class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    <span
                      class="flex-grow"
                    >
                      <textarea-input
                        name="body-script"
                        :value="form.body"
                        :error="fieldsErrors.body"
                        :text-error="fieldsErrors.body ? textErrors.body : ['']"
                        rows="10"
                        @input-return="value => form.body = value"
                      />
                      <p>
                        {{ $_("These script will be printed below the &#60;body&#62; tag") }}
                      </p>
                    </span>
                  </div>
                </div>
                <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4">
                  <div class="text-sm font-medium text-gray-500">
                    <label for="footer-script">{{ $_("Scripts in Footer") }}</label>
                  </div>
                  <div class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    <span
                      class="flex-grow"
                    >
                      <textarea-input
                        name="footer-script"
                        :value="form.footer"
                        :error="fieldsErrors.footer"
                        :text-error="fieldsErrors.footer ? textErrors.footer : ['']"
                        rows="10"
                        @input-return="value => form.footer = value"
                      />
                      <p>
                        {{ $_("These script will be printed above the &#60;/body&#62; tag") }}
                      </p>
                    </span>
                  </div>
                </div>
                <div class="py-4 sm:py-5 grid grid-cols-1 sm:gap-4">
                  <div class="mt-2 sm:mt-0">
                    <button 
                      type="submit"
                      :disabled="isSendingForm"
                      class="w-full my-auto flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2"
                      :class="[isSendingForm ? 
                        'bg-app-200 hover:bg-app-200 focus:ring-app-200' : 
                        'bg-app-600 hover:bg-app-700 focus:ring-app-500']"
                    >
                      <svg
                        v-show="isSendingForm"
                        class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                      >
                        <circle
                          class="opacity-25"
                          cx="12"
                          cy="12"
                          r="10"
                          stroke="currentColor"
                          stroke-widivh="4"
                        />
                        <path
                          class="opacity-75"
                          fill="currentColor"
                          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                        />
                      </svg>
                      {{ $_("Save") }}
                    </button>
                  </div>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from '@components/Layouts/LayoutGlobalSettings.vue'
import TextareaInput from '@components/Forms/TextareaInput.vue'
import NotificationSuccess from '@components/Utils/NotificationSuccess.vue'

export default {
  name: "ScriptIndex",
  components: {
    Layout,
    'textarea-input': TextareaInput,
    'notification-success': NotificationSuccess,
  },
  props:{
    flash: {
      type: Object,
      default: () => { }
    },
    errors: {
      type: Object,
      default: () => { }
    },
    header: {
      type: String,
      default: () => ""
    },
    footer: {
      type: String,
      default: () => ""
    },
    body: {
      type: String,
      default: () => ""
    },
  },
  data () {
    return {
      isSendingForm: false,
      textNotification: "",
      showNotification: false,
      form: {
        header: this.header,
        footer: this.footer,
        body: this.body,
      },
      fieldsErrors: {
        header: false,
        footer: false,
        body: false,
      },
      textErrors: {
        header: [],
        footer: [],
        body: [],
      },
    }
  },
  methods: {
    onSubmit(event) {
      event.preventDefault();
      this.$inertia.post(this.route('management:global_settings_scripts'), this.form, {
        onStart: () => this.isSendingForm = true,
        onFinish: () => {
          this.isSendingForm = false;
          if(this.flash.success) {
            var vue = this;
            this.textNotification = this.flash.success;
            this.showNotification = true
            setTimeout(function () { 
              vue.showNotification = false;
              window.location.reload();
            }, 2000)
          }
        }
      })
    },
  }
}
</script>

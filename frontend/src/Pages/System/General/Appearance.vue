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
          {{ $_("Appearance") }}
        </h2>
        <p class="max-w-2xl text-sm text-gray-500">
          {{ $_("Change the appearence of the app") }}
        </p>
      </div>
      <div class="mt-6">
        <div class="divide-y divide-gray-200">
          <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4">
            <div class="text-sm font-medium text-gray-500">
              {{ $_("App name") }}
            </div>
            <div class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              <span
                v-if="!editAppName"
                class="flex-grow"
              >{{ appName }}</span>
              <span
                v-else
                class="flex-grow"
              >
                <app-name-form 
                  :name="appName"
                  :flash="flash"
                  :errors="errors"
                  @close-update-name="editAppName = false"
                  @show-notification="value => showNotification = value"
                  @text-notitication="text => textNotification = text"
                />
              </span>
              <span
                v-if="!editAppName"
                class="ml-4 flex-shrink-0"
              >
                <button
                  type="button"
                  class="bg-white rounded-md font-medium text-app-600 hover:text-app-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-app-500"
                  @click="editAppName = true"
                >
                  {{ $_("Update") }}
                </button>
              </span>
            </div>
          </div>

          <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4">
            <div class="text-sm font-medium text-gray-500">
              {{ $_("App logo") }}
            </div>
            <div class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              <span
                v-if="!editLogo"
                class="flex-grow"
              >
                <inertia-link
                  :href="route('core:index')"
                >
                  <img
                    class="h-10 w-auto"
                    :src="appLogo"
                    :alt="appName"
                  >
                </inertia-link>
              </span>
              <span
                v-else
                class="flex-grow"
              >
                <app-logo-form 
                  :app-logo="appLogo"
                  :flash="flash"
                  :errors="errors"
                  @close-update-name="editLogo = false"
                  @show-notification="value => showNotification = value"
                  @text-notitication="text => textNotification = text"
                />
              </span>
              <span
                v-if="!editLogo"
                class="ml-4 flex-shrink-0 flex items-start space-x-4"
              >
                <button
                  type="button"
                  class="bg-white rounded-md font-medium text-app-600 hover:text-app-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-app-500"
                  @click="editLogo = true"
                >
                  {{ $_("Update") }}
                </button>
                <span
                  class="text-gray-300"
                  aria-hidden="true"
                >|</span>
                <button
                  type="button"
                  class="bg-white rounded-md font-medium text-app-600 hover:text-app-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-app-500"
                  @click="removeLogo"
                >
                  {{ $_("Remove") }}
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
import AppNameForm from '@components/Forms/SystemAppNameForm.vue'
import AppLogoForm from '@components/Forms/SystemAppLogoForm.vue'

export default {
  name: "GeneralAppearance",
  components: {
    'notification-success': NotificationSuccess,
    'app-name-form': AppNameForm,
    'app-logo-form': AppLogoForm
  },
  props: {
    flash: {
      type: Object,
      default: () => { }
    },
    errors: {
      type: Object,
      default: () => { }
    },
    appName: {
      type: String,
      default: () => "Django Easystart"
    },
    appLogo: {
      type: String,
      default: () => ""
    }
  },
  data () {
    return {
      showNotification: false,
      textNotification: "",
      editAppName: false,
      editLogo: false
    }
  },
  mounted (){
    if(this.flash.success) {
      var vue = this;
      this.textNotification = this.flash.success;
      this.showNotification = true
      setTimeout(function () { vue.showNotification = false }, 2000)
    }
  },
  methods: {
    removeLogo (){
      this.$inertia.get(this.route('management:system_remove_app_logo'), {
        onStart: () => this.showNotification = false,
        onFinish: () => {
          if(this.flash.success) {
            var vue = this;
            this.textNotification = this.flash.success;
            this.showNotification = true
            setTimeout(function () { vue.showNotification = false }, 2000)
          }
        }
      })
    }
  }
}
</script>

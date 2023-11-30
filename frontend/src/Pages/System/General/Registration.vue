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
          {{ $_("Registration Settings") }}
        </h2>
        <p class="max-w-2xl text-sm text-gray-500">
          {{ $_("You can activate/deactivate user registration") }}
        </p>
      </div>
      <div class="mt-6">
        <div class="divide-y divide-gray-200">
          <SwitchGroup
            as="div"
            class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4"
          >
            <div class="text-sm font-medium text-gray-500">
              <SwitchLabel>{{ $_("Enable user registration") }}</SwitchLabel>
            </div>
            <div class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              <div class="flex-grow">
                <span
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                  :class="registrationActive ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                >
                  {{ $_(registrationActive ? "Active" : "No active") }}
                </span>
              </div>
              <Switch
                :class="[registrationActive ? 'bg-app-600' : 'bg-gray-200', 'relative ml-4 inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-app-500']"
                @click="changeRegistrationActive"
              >
                <span
                  aria-hidden="true"
                  :class="[registrationActive ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']"
                />
              </Switch>
            </div>
          </SwitchGroup>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NotificationSuccess from '@components/Utils/NotificationSuccess.vue'
import { Switch, SwitchGroup, SwitchLabel } from '@headlessui/vue'

export default {
  name: "GeneralRegistration",
  components: {
    'notification-success': NotificationSuccess,
    Switch,
    SwitchGroup,
    SwitchLabel,
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
    registrationActive: {
      type: Boolean,
      default: () => false
    },
  },
  data () {
    return {
      showNotification: false,
      textNotification: "",
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
    changeRegistrationActive() {
      this.$inertia.get(this.route('management:system_active_registration'))
    }
  }
}
</script>

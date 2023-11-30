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
          {{ $_("Reset password or 2fa, and activate/disactivate user.") }}
        </p>
      </div>
      <div class="mt-6">
        <div class="divide-y divide-gray-200">
          <div 
            v-if="canEditUser"
            class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4"
          >
            <div class="text-sm font-medium text-gray-500">
              {{ $_("Reset password") }}
            </div>
            <div class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              <span
                class="flex-grow"
              />
              <span
                class="ml-4 flex-shrink-0"
              >
                <span
                  v-if="$page.props.tfa && $page.props.tfa.enable && !$page.props.tfa.userSetup"
                  class="flex-grow text-red-500 font-medium"
                >
                  {{ $_("You need activate 2fa for this action") }}
                </span>
                <inertia-link
                  v-else
                  :href="route('management:user_reset_password', user.user_id)"
                  class="bg-white rounded-md font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-app-500'"
                >
                  <span
                    class="text-app-600 hover:text-app-500"
                  >{{ $_("Send email") }}</span>
                </inertia-link>
              </span>
            </div>
          </div>
          <SwitchGroup
            as="div"
            class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:pt-5"
          >
            <div class="text-sm font-medium text-gray-500">
              <SwitchLabel>{{ $_("Status") }}</SwitchLabel>
            </div>
            <div class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              <div class="flex-grow">
                <span
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                  :class="user.isActive ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                >
                  {{ $_(user.isActive ? "Active" : "No active") }}
                </span>
              </div>
              <Switch
                :class="[user.isActive ? 'bg-app-600' : 'bg-gray-200', 'relative ml-4 inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-app-500']"
                @click="changeUserStatus"
              >
                <span
                  aria-hidden="true"
                  :class="[user.isActive ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']"
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
  components: {
    Switch,
    SwitchGroup,
    SwitchLabel,
    'notification-success': NotificationSuccess,
  },
  props: {
    user: {
      type: Object,
      default: () => {}
    },
    errors: {
      type: Object,
      default: () => {}
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
      openModal: false
    }
  },

  computed: {
    canEditUser() {
      return this.$page.props.auth.user.permissions.includes("core.can_edit_user");
    }
  },

  methods: {
    changeUserStatus () {
      this.$inertia.get(this.route("management:user_change_status", this.user.user_id));
    }
  }
}
</script>

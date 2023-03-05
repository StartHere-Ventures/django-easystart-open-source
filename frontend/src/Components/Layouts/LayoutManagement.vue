<template>
  <div>
    <div class="h-screen bg-white overflow-hidden flex">
      <TransitionRoot
        as="template"
        :show="sidebarOpen"
      >
        <Dialog
          as="div"
          static
          class="fixed inset-0 z-40 flex md:hidden"
          :open="sidebarOpen"
          @close="sidebarOpen = false"
        >
          <TransitionChild
            as="template"
            enter="transition-opacity ease-linear duration-300"
            enter-from="opacity-0"
            enter-to="opacity-100"
            leave="transition-opacity ease-linear duration-300"
            leave-from="opacity-100"
            leave-to="opacity-0"
          >
            <DialogOverlay class="fixed inset-0 bg-gray-600 bg-opacity-75" />
          </TransitionChild>
          <TransitionChild
            as="template"
            enter="transition ease-in-out duration-300 transform"
            enter-from="-translate-x-full"
            enter-to="translate-x-0"
            leave="transition ease-in-out duration-300 transform"
            leave-from="translate-x-0"
            leave-to="-translate-x-full"
          >
            <div class="relative max-w-xs w-full bg-white pt-5 pb-4 flex-1 flex flex-col">
              <TransitionChild
                as="template"
                enter="ease-in-out duration-300"
                enter-from="opacity-0"
                enter-to="opacity-100"
                leave="ease-in-out duration-300"
                leave-from="opacity-100"
                leave-to="opacity-0"
              >
                <div class="absolute top-0 right-0 -mr-14 p-1">
                  <button
                    class="h-12 w-12 rounded-full flex items-center justify-center focus:outline-none focus:bg-gray-600"
                    @click="sidebarOpen = false"
                  >
                    <XIcon
                      class="h-6 w-6 text-white"
                      aria-hidden="true"
                    />
                    <span class="sr-only">Close sidebar</span>
                  </button>
                </div>
              </TransitionChild>
              <div class="flex-shrink-0 px-4 flex items-center">
                <inertia-link
                  :href="route('core:index')"
                >
                  <img
                    class="h-16 w-auto"
                    :src="$page.props.globalSettings.appLogo"
                    :alt="$page.props.globalSettings.appName"
                  >
                </inertia-link>
              </div>
              <div class="mt-5 flex-1 h-0 overflow-y-auto">
                <nav
                  class="h-full flex flex-col"
                  aria-label="Site navigation"
                >
                  <div class="space-y-1">
                    <inertia-link
                      v-for="item in navigation"
                      :key="item.name"
                      :href="route(item.href)"
                      :class="[item.current ? 'bg-app-50 border-app-600 text-app-600' : 'border-transparent text-gray-600 hover:text-gray-900 hover:bg-gray-50', 'group border-l-4 py-2 px-3 flex items-center text-sm font-medium']"
                    >
                      <component
                        :is="item.icon"
                        :class="[item.current ? 'text-app-500' : 'text-gray-400 group-hover:text-gray-500', 'mr-3 flex-shrink-0 h-6 w-6']"
                        aria-hidden="true"
                      />
                      {{ $_(item.name) }}
                    </inertia-link>
                  </div>
                  <div class="mt-auto pt-10 space-y-1">
                    <inertia-link
                      v-for="item in secondaryNavigation"
                      :key="item.name"
                      :href="route(item.href)"
                      class="group border-l-4 border-transparent py-2 px-3 flex items-center text-sm font-medium"
                      :class="item.current ? 'bg-app-50 border-app-600 text-app-600' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'"
                    >
                      <component
                        :is="item.icon"
                        class="text-gray-400 group-hover:text-gray-500 mr-3 h-6 w-6"
                        aria-hidden="true"
                      />
                      {{ $_(item.name) }}
                    </inertia-link>
                  </div>
                </nav>
              </div>
            </div>
          </TransitionChild>
          <div
            class="flex-shrink-0 w-14"
            aria-hidden="true"
          >
            <!-- Dummy element to force sidebar to shrink to fit close icon -->
          </div>
        </Dialog>
      </TransitionRoot>

      <!-- Static sidebar for desktop -->
      <div class="hidden md:flex md:flex-shrink-0">
        <div class="w-64 flex flex-col">
          <!-- Sidebar component, swap this element with another sidebar if you like -->
          <nav
            class="bg-gray-50 border-r border-gray-200 pt-5 pb-4 flex flex-col flex-grow overflow-y-auto"
            aria-label="Site navigation"
          >
            <div class="flex-shrink-0 px-4 flex items-center">
              <inertia-link
                :href="route('core:index')"
              >
                <img
                  class="h-16 w-auto"
                  :src="$page.props.globalSettings.appLogo"
                  :alt="$page.props.globalSettings.appName"
                >
              </inertia-link>
            </div>
            <div class="flex-grow mt-5 flex flex-col">
              <div class="flex-1 space-y-1">
                <inertia-link
                  v-for="item in navigation"
                  :key="item.name"
                  :href="route(item.href)"
                  :class="[item.current ? 'bg-app-50 border-app-600 text-app-600' : 'border-transparent text-gray-600 hover:text-gray-900 hover:bg-gray-50', 'group border-l-4 py-2 px-3 flex items-center text-sm font-medium']"
                >
                  <component
                    :is="item.icon"
                    :class="[item.current ? 'text-app-500' : 'text-gray-400 group-hover:text-gray-500', 'mr-3 flex-shrink-0 h-6 w-6']"
                    aria-hidden="true"
                  />
                  {{ $_(item.name) }}
                </inertia-link>
              </div>
            </div>
            <div class="flex-shrink-0 block w-full">
              <inertia-link
                v-for="item in secondaryNavigation"
                :key="item.name"
                :href="route(item.href)"
                class="group border-l-4 border-transparent py-2 px-3 flex items-center text-sm font-medium"
                :class="item.current ? 'bg-app-50 border-app-600 text-app-600' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'"
              >
                <component
                  :is="item.icon"
                  class="text-gray-400 group-hover:text-gray-500 mr-3 h-6 w-6"
                  aria-hidden="true"
                />
                {{ $_(item.name) }}
              </inertia-link>
            </div>
          </nav>
        </div>
      </div>

      <!-- Content area -->
      <div class="flex-1 flex flex-col">
        <message
          v-if="$page.props.auth.emailAddress.emailMethod == 'optional' && !$page.props.auth.emailAddress.verified"
        >
          {{ $_("Your email has not been confirmed.") }}
        </message>
        <message
          v-if="$page.props.tfa && $page.props.tfa.enable && !$page.props.tfa.userSetup"
        >
          {{ $_("Oops, you don't have two factor authentication active. To configure it click") }} 
          <inertia-link
            class="font-medium"
            :href="route('2fa:settings')"
          >
            here
          </inertia-link> 
        </message>
        <div class="w-full max-w-4xl mx-auto md:px-8 xl:px-0">
          <div class="md:hidden relative z-10 flex-shrink-0 h-16 bg-white border-b border-gray-200 flex">
            <button
              class="border-r border-gray-200 px-4 text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-app-500 md:hidden"
              @click="sidebarOpen = true"
            >
              <span class="sr-only">Open sidebar</span>
              <MenuAlt2Icon
                class="h-5 w-5"
                aria-hidden="true"
              />
            </button>
            <div class="flex-1 flex justify-center my-auto text-app-900">
              <h1 class="font-medium text-xl">
                {{ $page.props.globalSettings.appName }}
              </h1>
            </div>
          </div>
        </div>

        <main class="flex-1 overflow-y-auto focus:outline-none">
          <div class="relative max-w-4xl mx-auto md:px-8 xl:px-0">
            <div class="pt-10 pb-16">
              <slot name="content" />
            </div>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>


<script>
import { ref } from 'vue'
import {
  Dialog,
  DialogOverlay,
  Switch,
  SwitchGroup,
  SwitchLabel,
  TransitionChild,
  TransitionRoot,
} from '@headlessui/vue'
import {
  BellIcon,
  CogIcon,
  AdjustmentsIcon,
  UsersIcon,
  HomeIcon,
  MenuAlt2Icon,
  QuestionMarkCircleIcon,
  XIcon,
  MailIcon,
  AnnotationIcon,
  DocumentReportIcon,
  LogoutIcon,
  UserGroupIcon,
  BriefcaseIcon
} from '@heroicons/vue/outline'
import { SearchIcon } from '@heroicons/vue/solid'
import Message from '@components/Utils/MessageInfo.vue'
import NotificationSuccess from '@components/Utils/NotificationSuccess.vue'

export default {
  components: {
    Dialog,
    DialogOverlay,
    Switch,
    SwitchGroup,
    SwitchLabel,
    TransitionChild,
    TransitionRoot,
    BellIcon,
    MenuAlt2Icon,
    SearchIcon,
    XIcon,
    AnnotationIcon,
    DocumentReportIcon,
    MailIcon,
    LogoutIcon,
    Message,
    UserGroupIcon,
    BriefcaseIcon,
    'notification-success': NotificationSuccess,
  },
  props: {
    navActive: {
      type: String,
      default: () => 'home'
    },
  },
  setup(props) {
    const defaultNavigation = [
      {
        name: "Home",
        href: "core:index",
        icon: HomeIcon,
        current: props.navActive == "home" ? true : false,
      },
      {
        name: "Users",
        href: "management:users",
        permissionRequired: "core.can_view_users",
        icon: UsersIcon,
        current: props.navActive == "users" ? true : false,
      },
      {
        name: "Global Settings",
        href: "management:global_settings_general",
        permissionRequired: "core.can_management_global_settings",
        icon: AdjustmentsIcon,
        current: props.navActive == "settings-global" ? true : false,
      },
    ]
    const secondaryNavigation = [
      {
        name: "Help",
        href: "core:index",
        icon: QuestionMarkCircleIcon,
        current: false,
      },
      {
        name: "Account Settings",
        href: "management:settings",
        icon: CogIcon,
        current: props.navActive == "settings" ? true : false,
      },
      {
        name: "Logout",
        href: "accounts:logout",
        icon: LogoutIcon,
        current: false,
      },
    ]

    const sidebarOpen = ref(false)
    const automaticTimezoneEnabled = ref(true)
    const autoUpdateApplicantDataEnabled = ref(false)

    return {
      sidebarOpen,
      automaticTimezoneEnabled,
      autoUpdateApplicantDataEnabled,
      defaultNavigation,
      secondaryNavigation,
    }
  },
  data() {
    return {
      showNotification: false,
      navigation: []
    }
  },
  mounted (){
    let navigation = this.defaultNavigation;
    let nav = [];
    let userPermissions = this.$page.props.auth.user.permissions;
    navigation.map(item => {
      var addItemToList = true;
      if (
        item.permissionRequired && !userPermissions.includes(item.permissionRequired)
      ) {
        addItemToList = false;
      }

      if (addItemToList) {
        nav.push(item);
      }
    })
    this.navigation = nav;
  },
  created() {
    if (this.$page.props.userLanguage){
      this.$setlang(this.$page.props.userLanguage)
    }
    setTimeout(function(){ window.location.reload() }, (this.$page.props.globalSettings.timeExpiredSession * 60 + 5) * 1000);
  }
}
</script>

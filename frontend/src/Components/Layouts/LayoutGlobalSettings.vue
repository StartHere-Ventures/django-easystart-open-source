<template>
  <layout nav-active="settings-global">
    <template #content>
      <div class="px-4 sm:px-6 md:px-0">
        <h1 class="text-3xl font-extrabold text-gray-900">
          {{ $_("Global Settings") }}
        </h1>
      </div>
      <div class="px-4 sm:px-6 md:px-0">
        <div class="py-6">
          <!-- Tabs -->
          <div class="lg:hidden">
            <label
              for="selected-tab"
              class="sr-only"
            >Select a tab</label>
            <select
              id="selected-tab"
              name="selected-tab"
              class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-app-500 focus:border-app-500 sm:text-sm rounded-md"
              @change="redirectTab"
            >
              <option
                v-for="tab in tabsDefault"
                :key="tab.name"
                :selected="tab.current"
                :value="tab.href"
              >
                {{ $_(tab.name) }}
              </option>
            </select>
          </div>
          <div class="hidden lg:block">
            <div class="border-b border-gray-200">
              <nav class="-mb-px flex space-x-8">
                <inertia-link
                  v-for="tab in tabsDefault"
                  :key="tab.name"
                  :href="route(tab.href)"
                  :class="[tab.current ? 'border-app-500 text-app-600' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700', 'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm']"
                >
                  {{ $_(tab.name) }}
                </inertia-link>
              </nav>
            </div>
          </div>

          <slot name="settings-content" />
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from './Layout.vue'
   
export default {
  components: {
    Layout,
  },
  props: {
    tabsActive: {
      type: String,
      default: () => 'appearance'
    },
  },
  setup(props){
    const tabsDefault = [
      { name: 'General', href: 'management:global_settings_general', current: props.tabsActive == "general" ? true : false },
      { name: 'Security', href: 'management:global_settings_security', current: props.tabsActive == "security" ? true : false },
      { name: 'Scripts', href: 'management:global_settings_scripts', current: props.tabsActive == "scripts" ? true : false },
    ];
    return {
      tabsDefault,
    }
  },
  data () {
    return {
      tabs: [],
      tfaSettings: {
        enable: '',
        userSetup: '',
        method: ''
      },
      editName: false,
      formName: {
        firstName: "",
        lastName: "",
      }
    }
  },
  methods: {
    redirectTab(e) {
      this.$inertia.get(this.route(e.target.value))
    }
  }
}
</script>

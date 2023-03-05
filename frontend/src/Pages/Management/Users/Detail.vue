<template>
  <layout nav-active="users">
    <template #content>
      <div class="px-4 sm:px-6 md:px-0">
        <h1 class="text-3xl font-extrabold text-gray-900">
          {{ $_("User Detail") }}
        </h1>
      </div>
      <div class="px-4 pt-4 sm:px-6 md:px-0">
        <breadcrumb 
          :pages="pages"
        />
      </div>
      <div class="px-4 py-6 sm:px-6 md:px-0">
        <user-profile
          :user="user"
          :flash="flash"
          :user-profile="user.profile"
          :errors="errors"
        />

        <user-account 
          :user="user"
          :flash="flash"
          :user-profile="user.profile"
          :available-languages="availableLanguages"
          :available-countries="availableCountries"
          :available-date-formats="availableDateFormats"
          :available-groups="availableGroups"
          :errors="errors"
        />

        <user-security 
          :user="user"
          :tfa-active="tfaActive"
          :flash="flash"
          :errors="errors"
        />
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from '@components/Layouts/Layout.vue'
import Breadcrumb from '@components/Utils/Breadcrumbs.vue'
import UserProfile from './UserProfile.vue'
import UserAccount from './UserAccount.vue'
import UserSecurity from './UserSecurity.vue'

const pagesDefault = [
  { name: 'Users', href: 'management:users', current: false },
  { name: 'User Detail', href: 'management:users', current: true },
]

export default {
  name: 'UserDetail',
  components: {
    Layout,
    Breadcrumb,
    UserProfile,
    UserAccount,
    UserSecurity,
  },
  props: {
    user: {
      type: Object,
      default: () => {}
    },
    flash: {
      type: Object,
      default: () => { }
    },
    errors: {
      type: Object,
      default: () => { }
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
    availableGroups: {
      type: Object,
      default: () => {}
    },
    tfaActive: {
      type: Boolean,
      default: () => false
    },
    assets: {
      type: Array,
      default: () => [] 
    },
    assetsBalance: {
      type: Object,
      default: () => {}
    },
    assetsSettings: {
      type: Object,
      default: () => {}
    },
  },
  data () {
    return {
      pages: pagesDefault
    }
  },
  computed: {
    canViewUserBalance() {
      return this.$page.props.auth.user.permissions.includes("core.can_view_user_balance");
    },
    isActiveWalletSettings() {
      return this.$page.props.globalSettings.activeWallet;
    },
  },
  created(){
    this.pages.map(item => {
      if(item.current){
        item.name = this.user.user_id
      }
    })
  },
}
</script>

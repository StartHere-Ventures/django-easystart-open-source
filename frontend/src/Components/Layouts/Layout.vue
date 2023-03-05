<template>
  <div>
    <layout-user
      v-if="isCustomer"
      :nav-active="navActive"
    >
      <template #content>
        <slot name="content" />
      </template>
    </layout-user>

    <layout-management
      v-else
      :nav-active="navActive"
    >
      <template #content>
        <slot name="content" />
      </template>
    </layout-management>
  </div>
</template>


<script>
import LayoutUser from './LayoutUser.vue';
import LayoutManagement from './LayoutManagement.vue';

export default {
  name: 'MainLayout',
  components: {
    LayoutUser,
    LayoutManagement
  },
  props: {
    navActive: {
      type: String,
      default: () => 'home'
    },
  },
  computed: {
    isCustomer () {
      return this.$page.props.auth.user.groups.includes("customer")
    }
  }
}
</script>

<template>
  <layout nav-active="users">
    <template #content>
      <div class="px-4 sm:px-6 md:px-0">
        <h1 class="text-3xl font-extrabold text-gray-900">
          {{ $_("Users") }}
        </h1>
      </div>
      <div class="px-4 pt-4 sm:px-6 md:px-0">
        <breadcrumb 
          :pages="breadcrumpsPages"
        />
      </div>
      <div class="px-4 py-6 sm:px-6 md:px-0">
        <search-input
          :link="route('management:users')"
          :search="search"
          class="mb-4"
        />

        <div class="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg">
          <table class="min-w-full shadow-lg rounded">
            <thead class="bg-gray-100">
              <tr class="uppercase">
                <th class="px-6 py-6 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  <span class="hidden lg:table-cell">{{ $_("Email") }}</span>
                  <span class="lg:hidden">{{ $_("User") }}</span>
                </th>
                <th class="hidden lg:table-cell px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ $_("Name") }}
                </th>
                <th class="hidden lg:table-cell px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ $_("Status") }}
                </th>
                <th 
                  v-if="canCreateUser || canViewUserDetail"
                  class="relative px-6 py-3"
                >
                  <inertia-link
                    v-if="canCreateUser"
                    :href="route('management:user_create')"
                    class="group flex items-center justify-center text-sm font-medium py-2 text-white rounded-md bg-app-600 hover:bg-app-700 focus:ring-app-500'"
                  >
                    {{ $_('Create') }}
                  </inertia-link>
                </th>
              </tr>
            </thead>
            <tbody
              v-if="users.length != 0"
              class="bg-white"
            >
              <tr
                v-for="(user, userIdx) in users"
                :key="user.user_id"
                class="accordion border-b border-grey-light hover:bg-gray-100"
                :class="userIdx % 2 === 0 ? 'bg-white' : 'bg-gray-50'"
              >
                <td class="flex inline-flex items-center px-6 py-4 whitespace-nowrap text-sm">
                  <span class="w-40">
                    <p class="font-medium text-gray-900">{{ user.email }}</p>
                    <p class="lg:hidden text-xs text-gray-500">{{ user.firstName }} {{ user.lastName }}</p>
                    <p
                      v-for="group in user.groups"
                      :key="group.name"
                      class="lg:table-cell text-xs text-gray-500"
                    >{{ group.name }}</p>
                    <p class="lg:hidden text-xs text-gray-500">
                      <span
                        v-if="user.isActive"
                        class="text-xs font-medium text-green-500"
                      >
                        {{ $_("Active") }}
                      </span>
                      <span
                        v-else
                        class="text-xs font-medium text-red-500"
                      >
                        {{ $_("No active") }}
                      </span>
                    </p>
                  </span>
                </td>
                <td class="hidden lg:table-cell px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ user.firstName }} {{ user.lastName }}
                </td>
                <td class="hidden lg:table-cell px-6 py-4 whitespace-nowrap text-xs text-gray-500">
                  <span
                    v-if="user.isActive"
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"
                  >
                    {{ $_("Active") }}
                  </span>
                  <span
                    v-else
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800"
                  >
                    {{ $_("No active") }}
                  </span>
                </td>
                <td 
                  v-if="canCreateUser || canViewUserDetail"
                  class="table-cell px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                >
                  <p class="flex items-center justify-center">
                    <inertia-link
                      v-if="canViewUserDetail"
                      :href="route('management:user_detail', user.user_id)"
                      class="group border-l-4 border-transparent py-2 px-3 flex items-center text-sm font-medium text-gray-500 hover:text-app-500"
                    >
                      <PencilIcon
                        class="flex-shrink-0 h-5 w-5"
                        aria-hidden="true"
                      />
                      <span class="sr-only">{{ $_("View user detail") }}</span>
                    </inertia-link>
                  </p>
                </td>
              </tr>
            </tbody>
            <tbody
              v-else
              class="bg-white"
            >
              <tr>
                <td
                  colspan="3"
                  class="py-4 items-center text-center text-sm font-medium text-gray-500"
                >
                  {{ $_("No data, try again") }}
                </td>
              </tr>
            </tbody>
          </table>
          <pagination
            :link="route('management:users')"
            :count="count"
            :paginate-by="paginateBy"
            :pages="pages"
            :current-page="currentPage"
            :search="search"
          />
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import SearchInput from '@components/Utils/SearchInput.vue'
import Pagination from '@components/Utils/Pagination.vue'
import Layout from '@components/Layouts/Layout.vue'
import Breadcrumb from '@components/Utils/Breadcrumbs.vue'

const pagesDefault = [
  { name: 'Users', href: '#', current: true },
]

import {
  PencilIcon
} from '@heroicons/vue/outline'

export default {
  name: 'UserList',
  components: {
    Layout,
    Breadcrumb,
    Pagination,
    PencilIcon,
    SearchInput
  },
  props: {
    users: {
      type: Array,
      default: () => []
    },
    count: {
      type: Number,
      default: () => 0,
    },
    paginateBy: {
      type: Number,
      default: () => 10
    },
    pages: {
      type: Number,
      default: () => 1
    },
    currentPage: {
      type: Number,
      default: () => 1
    },
    search: {
      type: String,
      default: () => ""
    }
  },
  data () {
    return {
      breadcrumpsPages: pagesDefault
    }
  },
  computed: {
    canCreateUser() {
      return this.$page.props.auth.user.permissions.includes("core.can_create_user");
    },
    canViewUserDetail() {
      return this.$page.props.auth.user.permissions.includes("core.can_view_user_detail");
    }
  }
}
</script>

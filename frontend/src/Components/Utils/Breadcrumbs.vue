<template>
  <nav
    class="flex"
    aria-label="Breadcrumb"
  >
    <ol class="flex items-center space-x-4">
      <li>
        <div>
          <inertia-link
            class="text-gray-400 hover:text-gray-500"
            :href="route('core:index')"
          >
            <HomeIcon
              class="flex-shrink-0 h-5 w-5"
              aria-hidden="true"
            />
            <span class="sr-only">Home</span>
          </inertia-link> 
        </div>
      </li>
      <li
        v-for="page in pages"
        :key="page.name"
      >
        <div class="flex items-center">
          <ChevronRightIcon
            class="flex-shrink-0 h-5 w-5 text-gray-400"
            aria-hidden="true"
          />
          <span v-if="!page.current">
            <inertia-link
              class="ml-4 text-sm font-medium text-gray-500 hover:text-gray-700"
              aria-current="page"
              :href="route(page.href)"
            >
              {{ $_(page.name) }}
            </inertia-link>
          </span>
          <span
            v-else
            class="ml-4 text-sm font-medium text-gray-500 hover:text-gray-700"
          >
            {{ $_(page.name) }}
          </span>
        </div>
      </li>
    </ol>
  </nav>
</template>

<script>
import { HomeIcon, ChevronRightIcon } from '@heroicons/vue/solid'

const pagesDefault = [
  { name: 'Easystart', href: '#', current: false },
  { name: 'Easystart Nero', href: '#', current: true },
]

export default {
  name: 'BreadCrumbs',
  components: {
    HomeIcon,
    ChevronRightIcon
  },
  props: {
    pages: {
      type: Array,
      default: () => pagesDefault
    }
  }
}
</script>
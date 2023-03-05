<template>
  <form
    class="w-full flex md:ml-0"
    @submit="onSubmit"
  >
    <div class="w-full max-w-4xl mx-auto md:px-8 xl:px-0">
      <div class="relative z-10 flex-shrink-0 h-16 bg-white border-b border-gray-200 flex">
        <div
          class="flex-1 flex justify-between px-4 md:px-0"
        >
          <div class="flex-1 flex">
            <label
              for="search"
              class="sr-only"
            >{{ $_("Search") }}</label>
            <div class="relative w-full text-gray-400 focus-within:text-gray-600">
              <input
                id="search"
                v-model="searchInput"
                name="search"
                autocomplete="off"
                class="h-full w-full hover:bg-white border-transparent py-2 pl-8 pr-3 text-base text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-0 focus:border-transparent focus:placeholder-gray-400"
                :placeholder="$_('Search')"
                type="search"
                @keypress.enter="onSubmit"
              >
            </div>
            <div class="ml-4 flex items-center md:ml-6">
              <button
                type="submit" 
                class="bg-white rounded-full p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-app-500"
              >
                <SearchIcon
                  class="flex-shrink-0 h-5 w-5"
                  aria-hidden="true"
                  @click="onSubmit"
                />
                <span class="sr-only">{{ $_("Submit search") }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </form>
</template>

<script>
import {
  SearchIcon
} from '@heroicons/vue/outline'

export default {
  components: {
    SearchIcon,
  },
  props: {
    search: {
      type: String,
      default: () => ""
    },
    link: {
      type: String,
      default: () => ""
    }
  },
  data () {
    return {
      searchInput: this.search ? this.search : ""
    }
  },
  methods: {
    onSubmit(event) {
      event.preventDefault();
      if(this.searchInput == ""){ 
        this.$inertia.get(this.link)
        return
      }
      let url = `${this.link}?search=${this.searchInput}`
      this.$inertia.get(url)
    },
  }
}


</script>
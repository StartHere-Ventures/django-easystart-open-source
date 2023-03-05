<template>
  <div
    v-show="show"
    class="rounded-md bg-green-50 p-4"
  >
    <div class="flex">
      <div class="flex-shrink-0">
        <ExclamationIcon
          class="h-5 w-5 text-green-400"
          aria-hidden="true"
        />
      </div>
      <div class="ml-3">
        <p class="text-sm font-medium text-green-800">
          <slot />
        </p>
      </div>
      <div class="ml-auto pl-3">
        <div class="-mx-1.5 -my-1.5">
          <button
            class="inline-flex bg-green-50 rounded-md p-1.5 text-green-500 hover:bg-green-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-green-50 focus:ring-green-600"
            @click="show = false"
          >
            <span class="sr-only">Dismiss</span>
            <XIcon
              class="h-5 w-5"
              aria-hidden="true"
            />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { ExclamationIcon, XIcon } from '@heroicons/vue/solid'

export default {
  components: {
    ExclamationIcon,
    XIcon
  },
  props: {
    text: {
      type: String,
      default: () => ""
    },
    time: {
      type: String,
      default: () => "10"
    }
  },
  data () {
    return {
      show: true
    }
  },
  mounted () {
    var vue = this;
    setTimeout(function(){ vue.show = false }, parseInt(this.time) * 1000);
  }
}
</script>
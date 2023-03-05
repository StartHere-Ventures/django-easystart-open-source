<template>
  <div>
    <div class="flex justify-between">
      <label
        :for="name1"
        class="block text-sm font-medium text-gray-700"
      >{{ $_(label) }}</label>
      <span
        id="password-show"
        class="text-sm text-gray-500"
      >
        <span
          v-if="!show"
          class="flex cursor-pointer"
          @click="show = true"
        >
          <EyeIcon class="flex-shrink-0 text-gray-500 flex h-5 w-5 mr-1" /> {{ $_("Show") }}
        </span>
        <span
          v-if="show"
          class="flex cursor-pointer"
          @click="show = false"
        >
          <EyeOffIcon class="flex-shrink-0 text-gray-500 flex h-5 w-5 mr-1" /> {{ $_("Hide") }}
        </span>
      </span>
    </div>
    <div class="mt-2 relative rounded-md shadow-sm">
      <input 
        v-show="!show"
        :id="name1"
        :value="value"
        :name="name1"
        type="password"
        class="mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
        :class="[error ? 
          'border-red-300 focus:ring-red-500 focus:border-red-500' : 
          'border-gray-300 focus:ring-app-500 focus:border-app-500']"
        @input="$emit('input-return', $event.target.value)"
        @blur="$emit('blur')"
      >
      <input 
        v-show="show"
        :id="name2"
        :value="value"
        :name="name2"
        type="text"
        class="mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
        :class="[error ? 
          'border-red-300 focus:ring-red-500 focus:border-red-500' : 
          'border-gray-300 focus:ring-app-500 focus:border-app-500']"
        @input="$emit('input-return', $event.target.value)"
        @blur="$emit('blur')"
      >
      <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
        <ExclamationCircleIcon
          v-show="error"
          class="h-5 w-5 text-red-500"
          aria-hidden="true"
        />
      </div>
    </div>
    <p
      v-for="text in textError"
      v-show="error"
      id="password-error"
      :key="text"
      class="mt-1 text-xs text-red-600"
    >
      {{ $_(text) }}
    </p>
  </div>
</template>

<script>
import { EyeIcon, EyeOffIcon } from '@heroicons/vue/outline'
import { ExclamationCircleIcon } from '@heroicons/vue/solid'
export default {
  components: {
    EyeIcon,
    EyeOffIcon,
    ExclamationCircleIcon
  },
  props: {
    label: {
      type: String,
      default: () => "Password"
    },
    name: {
      type: String,
      default: () => "password"
    },
    error: {
      type: Boolean,
      default: () => false
    },
    textError: {
      type: Array,
      default: () => ["This field is required"]
    },
    value: {
      type: String,
      default: () => ""
    }
  },
  emits: [
    'input-return',
    'blur'
  ],
  data () {
    return {
      show: false
    }
  },
  computed: {
    name1(){
      return this.name+"1"
    },
    name2(){
      return this.name+"2"
    }
  },
}
</script>
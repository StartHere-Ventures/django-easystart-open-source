<template>
  <div>
    <label
      v-if="label"
      :for="name"
      class="block text-sm font-medium text-gray-700"
    >{{ label }}</label>
    <div class="mt-2 relative rounded-md shadow-sm">
      <input 
        :id="name"
        :value="value"
        :name="name"
        :type="type"
        :maxlength="maxlength"
        :disabled="disabled"
        class="mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
        :class="[error ? 
          'border-red-300 focus:ring-red-500 focus:border-red-500' : 
          'border-gray-300 focus:ring-app-500 focus:border-app-500']"
        @keydown="handleOnKeyDown"
        @input="$emit('input-return', $event.target.value)"
        @blur="$emit('blur')"
        @change="$emit('change')"
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
      :key="text"
      class="mt-1 text-xs text-red-600"
    >
      {{ $_(text) }}
    </p>
  </div>
</template>

<script>
import { ExclamationCircleIcon } from '@heroicons/vue/solid'
export default {
  components: {
    ExclamationCircleIcon
  },
  props: {
    label: {
      type: String,
      default: () => ""
    },
    name: {
      type: String,
      default: () => ""
    },
    type: {
      type: String,
      default: () => "text"
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
    },
    maxlength: {
      type: String,
      default: () => "255"
    },
    inputmode: {
      type: String,
      default: () => ""
    },
    disabled: {
      type: Boolean,
      default: () => false
    }
  },
  emits: [
    'input-return',
    'blur',
    'change'
  ],
  methods: {
    handleOnKeyDown(event) {
      if(this.inputmode == "number"){
        // Only allow characters 0-9, DEL, Backspace and Pasting
        const keyEvent = (event) || window.event;
        const charCode = (keyEvent.which) ? keyEvent.which : keyEvent.keyCode;
        if (this.isCodeNumeric(charCode)
                  || (charCode === 8)
                  || (charCode === 86)
                  || (charCode === 46)) {
          return
        } else {
          keyEvent.preventDefault();
        }
      }
    },
    isCodeNumeric(charCode) {
      // numeric keys and numpad keys
      return (charCode >= 48 && charCode <= 57) || (charCode >= 96 && charCode <= 105);
    },
  },
}
</script>
<template>
  <div>
    <label
      v-if="label"
      :for="name"
      class="block text-sm font-medium text-gray-700"
    >{{ label }}</label>
    <div class="mt-2 relative rounded-md shadow-sm">
      <textarea 
        :id="name"
        :value="value"
        :name="name"
        class="mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
        :class="[error ? 
          'border-red-300 focus:ring-red-500 focus:border-red-500' : 
          'border-gray-300 focus:ring-app-500 focus:border-app-500']"
        :rows="rows"
        @input="$emit('input-return', $event.target.value)"
        @blur="$emit('blur')"
      />
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
export default {
  props: {
    label: {
      type: String,
      default: () => ""
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
    rows: {
      type: String,
      default: () => "3"
    },
    name: {
      type: String,
      default: () => "name"
    }
  },
  emits: [
    'input-return',
    'blur',
  ],
}
</script>
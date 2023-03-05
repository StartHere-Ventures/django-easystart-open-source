<template>
  <div>
    <label
      v-if="label"
      :for="label"
      class="block text-sm font-medium text-gray-700"
    >{{ label }}</label>
    <select
      :id="name"
      :name="name"
      v-model="selected"
      class="mt-1 block w-full pl-3 pr-10 py-2 text-base focus:outline-none sm:text-sm rounded-md"
      :class="[error ? 
        'border-red-300 focus:ring-red-500 focus:border-red-500' : 
        'border-gray-300 focus:ring-app-500 focus:border-app-500']"
      @change="$emit('change', selected)"
    >
      <option
        v-for="v, key in values"
        :key="key"
        :value="key"
      >
        {{ $_(v) }}
      </option>
    </select>
    <p
      v-for="text in textError"
      v-show="error"
      :key="text"
      class="mt-1 text-xs text-red-600"
    >
      {{ text }}
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
    name: {
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
    values: {
      type: Object,
      default: () => {}
    },
    valueSelect: {
      type: String,
      default: () => ""
    }
  },
  emits: [
    'change'
  ],
  data () {
    return {
      selected: this.valueSelect
    }
  }
}
</script>
<template>
  <div>
    <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
      <div class="space-y-1 text-center">
        <svg
          class="mx-auto h-12 w-12 text-gray-400"
          stroke="currentColor"
          fill="none"
          viewBox="0 0 48 48"
          aria-hidden="true"
        >
          <path
            d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
        <div class="flex text-sm justify-center text-center text-gray-600">
          <label
            for="file-upload"
            class="relative cursor-pointer bg-white rounded-md font-medium text-app-600 hover:text-app-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-app-500"
          >
            <span v-if="file.length == 0">{{ $_(label) }}</span>
            <span v-else>{{ file.name }}</span>
            <input
              id="file-upload"
              name="file-upload"
              type="file"
              class="sr-only"
              multiple
              @change="previewFile"
            >
          </label>
        </div>
        <div>
          <p class="text-xs text-gray-500">
            {{ $i_($_('%(ext)s up to %(size)s MB'), {ext: allowExt, size: size }, true) }}
          </p>
          <p
            v-for="text in textError"
            v-show="error"
            :key="text"
            class="mt-1 text-xs text-red-600"
          >
            {{ text }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    label: {
      type: String,
      default: () => "Upload a file"
    },
    error: {
      type: Boolean,
      default: () => false
    },
    textError: {
      type: Array,
      default: () => ["This field is required"]
    },
    ext: {
      type: Array,
      default: () => [".png", ".jpg", ".jpeg", ".pdf"]
    },
    size: {
      type: Number,
      default: 10
    }
  },
  emits: [
    'change'
  ],
  data() {
    return {
      file: []
    }
  },
  computed: {
    allowExt (){
      return this.ext.toString().replace(/[.]/gi, ' ').toUpperCase();
    }
  },
  methods: {
    previewFile (event) {
      this.file = event.target.files[0]
      this.$emit('change', this.file)
    }
  }
}
</script>
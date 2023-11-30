<template>
  <div>
    <form
      class="space-y-4"
      @submit="onSubmit"
    >
      <div class="sm:grid sm:grid-cols- sm:gap-4">
        <div>
          <label for="language" class="sr-only">{{ $_("Language") }}</label>
          <select-input
            name="language"
            :values="availableLanguages"
            :value-select="language"
            :error="fieldsErrors.language"
            :text-error="fieldsErrors.language ? textErrors.language: ['']"
            @change="value => updateSelect(value)"
          />
        </div>
      </div>
      <div class="sm:grid sm:grid-cols-2 sm:gap-4">
        <div>
          <button 
            class="w-full my-auto flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 bg-gray-600 hover:bg-gray-700 focus:ring-gray-500"
            @click="cancelUpdate"
          >
            {{ $_("Cancel") }}
          </button>
        </div>
        <div class="mt-2 sm:mt-0">
          <button 
            type="submit"
            :disabled="isDisableButtonForm"
            class="w-full my-auto flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2"
            :class="[isDisableButtonForm ? 
              'bg-app-200 hover:bg-app-200 focus:ring-app-200' : 
              'bg-app-600 hover:bg-app-700 focus:ring-app-500']"
          >
            <svg
              v-show="isSendingForm"
              class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              />
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            {{ $_("Update") }}
          </button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import SelectInput from './SelectInput.vue'

export default {
  components:{
    'select-input': SelectInput
  },
  props: {
    availableLanguages: {
      type: Object,
      default: () => {}
    },
    language: {
      type: String,
      default: ""
    },
    success: {
      type: Object,
      default: () => {},
    },
    errors: {
      type: Object,
      default: () => {},
    },
    url: {
      type: String,
      default: () => '/settings/change/language'
    }
  },
  emits: [
    'close-update-name',
    'show-notification',
    'text-notitication'
  ],
  data () {
    return {
      isSendingForm: false,
      form: {
        language: this.language,
      },
      fieldsErrors: {
        language: false,
      },
      textErrors: {
        language: [],

      },
    }
  },
  computed: {
    isValidForm(){
      return true
    },
    isDisableButtonForm (){
      if(!this.isValidForm || this.isSendingForm){ return true }
      return false
    },
  },
  methods: {
    updateSelect(value){
      this.form.language = value;
    },
    cancelUpdate(event) {
      event.preventDefault();
      this.$emit('close-update-name', true)
    },
    onSubmit(event) {
      event.preventDefault();
      this.$inertia.post(this.url, this.form, {
        onStart: () => this.isSendingForm = true,
        onFinish: () => {
          this.isSendingForm = false;
          this.$emit('show-notification', false)
          if(this.errors){
            for (const item in this.fieldsErrors) {
              if (this.errors[item]) {
                this.textErrors[item] = this.errors[item];
                this.fieldsErrors[item] = true
              }
            }
          }
          if(this.success) {
            this.$emit('text-notitication', this.success)
            this.$emit('show-notification', true)
            this.$emit('close-update-name', true)
            window.location.reload();
          }
        }
      })
    },
  }
}
</script>
<template>
  <div>
    <form
      class="space-y-4"
      @submit="onSubmit"
    >
      <div class="sm:grid sm:grid-cols- sm:gap-4">
        <div>
          <label for="job-title" class="sr-only">{{ $_("Job Title") }}</label>
          <basic-input
            name="job-title"
            :value="form.jobTitle"
            :error="fieldsErrors.jobTitle"
            :text-error="fieldsErrors.jobTitle ? textErrors.jobTitle: ['']"
            @input-return="value => form.jobTitle = value"
            @keypress="fieldsErrors.jobTitle = false"
            @blur="checkFieldsErrors('jobTitle')"
            @change="checkFieldsErrors('jobTitle')"
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
import useVuelidate from '@vuelidate/core'
import { required } from '@vuelidate/validators'
import BasicInput from './BasicInput.vue'

export default {
  components:{
    'basic-input': BasicInput
  },
  props: {
    job: {
      type: String,
      default: ""
    },
    flash: {
      type: Object,
      default: () => {},
    },
    errors: {
      type: Object,
      default: () => {},
    },
    url: {
      type: String,
      default: () => '/settings/change/job'
    }
  },
  emits: [
    'close-update-name',
    'show-notification',
    'text-notitication'
  ],
  setup () {
    return { v$: useVuelidate() }
  },
  validations () {
    return {
      form: {
        jobTitle: { required },
      },
    }
  },
  data () {
    return {
      isSendingForm: false,
      form: {
        jobTitle: this.job,
      },
      fieldsErrors: {
        jobTitle: false,
      },
      textErrors: {
        jobTitle: [],

      },
    }
  },
  computed: {
    isValidForm(){
      this.v$.$validate();
      if(this.v$.$error) return false
      return true
    },
    isDisableButtonForm (){
      if(!this.isValidForm || this.isSendingForm){ return true }
      return false
    }
  },
  methods: {
    checkFieldsErrors(field){
      this.fieldsErrors[field] = false;
      this.textErrors[field] = [];
      this.v$.$validate();
      if(this.v$.form[field].$errors.length){ 
        this.fieldsErrors[field] = true;
        this.textErrors[field].push(this.v$.form[field].$errors[0].$message)
      }
    },
    fieldsValidate() {
      let valid = true;
      this.checkFieldsErrors("jobTitle");
      for (const item in this.fieldsErrors) {
        if (this.fieldsErrors[item]) { valid = false }
      }
      return valid
    },
    onSubmit(event) {
      event.preventDefault();
      let valid = this.fieldsValidate();
      if(!valid) return;
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
          if(this.flash.success) {
            var vue = this;
            this.$emit('text-notitication', this.flash.success)
            this.$emit('show-notification', true)
            setTimeout(function () { vue.$emit('show-notification', false) }, 2000)
            this.$emit('close-update-name', true)
          }
        }
      })
    },
    cancelUpdate(event) {
      event.preventDefault();
      this.$emit('close-update-name', true)
    }
  }
}
</script>


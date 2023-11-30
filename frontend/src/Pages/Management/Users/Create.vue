<template>
  <layout nav-active="users">
    <template #content>
      <div class="px-4 sm:px-6 md:px-0">
        <h1 class="text-3xl font-extrabold text-gray-900">
          {{ $_("User Create") }}
        </h1>
      </div>
      <div class="px-4 pt-4 sm:px-6 md:px-0">
        <breadcrumb 
          :pages="pages"
        />
      </div>
      <div class="px-4 py-6 sm:px-6 md:px-0">
        <div class="mt-10 divide-y divide-gray-200">
          <div class="space-y-1">
            <h3 class="text-lg leading-6 font-medium text-gray-900">
              {{ $_("User") }}
            </h3>
          </div>
          <div class="mt-6">
            <form @submit="onSubmit">
              <div class="divide-y divide-gray-200">
                <slot name="general" />
                <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4">
                  <div class="text-sm font-medium text-gray-500">
                    <label for="first-name">{{ $_("First Name") }}</label>
                  </div>
                  <div class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    <span
                      class="flex-grow"
                    >
                      <basic-input 
                        name="first-name"
                        :value="form.firstName"
                        :error="fieldsErrors.firstName"
                        :text-error="fieldsErrors.firstName ? textErrors.firstName: ['']"
                        @input-return="value => form.firstName = value"
                        @keypress="fieldsErrors.firstName = false"
                        @blur="checkFieldsErrors('firstName')"
                        @change="checkFieldsErrors('firstName')"
                      />
                    </span>
                  </div>
                </div>
                <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4">
                  <div class="text-sm font-medium text-gray-500">
                    <label for="last-name">{{ $_("Last Name") }}</label>
                  </div>
                  <div class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    <span
                      class="flex-grow"
                    >
                      <basic-input 
                        name="last-name"
                        :value="form.lastName"
                        :error="fieldsErrors.lastName"
                        :text-error="fieldsErrors.lastName ? textErrors.lastName: ['']"
                        @input-return="value => form.lastName = value"
                        @keypress="fieldsErrors.lastName = false"
                        @blur="checkFieldsErrors('lastName')"
                        @change="checkFieldsErrors('lastName')"
                      />
                    </span>
                  </div>
                </div>
                <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4">
                  <div class="text-sm font-medium text-gray-500">
                    <label for="email">{{ $_("Email") }}</label>
                  </div>
                  <div class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    <span
                      class="flex-grow"
                    >
                      <basic-input 
                        name="email"
                        :value="form.email"
                        :error="fieldsErrors.email"
                        :text-error="fieldsErrors.email ? textErrors.email: ['']"
                        @input-return="value => form.email = value"
                        @keypress="fieldsErrors.email = false"
                        @blur="checkFieldsErrors('email')"
                        @change="checkFieldsErrors('email')"
                      />
                    </span>
                  </div>
                </div>
                <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4">  
                  <div class="text-sm font-medium text-gray-500">
                    <label for="group">{{ $_("User Role") }}</label>
                  </div>
                  <div class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    <span
                      class="flex-grow"
                    >
                      <select-input
                        name="group"
                        :values="availableGroups"
                        :value-select="form.group"
                        :error="fieldsErrors.group"
                        :text-error="fieldsErrors.group ? textErrors.group: ['']"
                        @change="value => updateGroup(value)"
                      />
                    </span>
                  </div>
                </div>
                <div class="py-4 sm:py-5 grid grid-cols-1 sm:gap-4">
                  <div class="mt-2 sm:mt-0">
                    <button 
                      type="submit"
                      :disabled="isDisableButtonForm"
                      class="w-full my-auto flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2"
                      :class="isDisableButtonForm ? 
                        'bg-app-200 hover:bg-app-200 focus:ring-app-200' : 
                        'bg-app-600 hover:bg-app-700 focus:ring-app-500'"
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
                          stroke-widivh="4"
                        />
                        <path
                          class="opacity-75"
                          fill="currentColor"
                          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                        />
                      </svg>
                      {{ $_("Create") }}
                    </button>
                  </div>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import useVuelidate from '@vuelidate/core'
import { required, email } from '@vuelidate/validators'
import Layout from '@components/Layouts/Layout.vue'
import Breadcrumb from '@components/Utils/Breadcrumbs.vue'
import BasicInput from '@components/Forms/BasicInput.vue'
import SelectInput from '@components/Forms/SelectInput.vue'

const pagesDefault = [
  { name: 'Users', href: 'management:users', current: false },
  { name: 'Create', href: '#', current: true },
]

export default {
  name: 'UserCreate',
  components: {
    Layout,
    Breadcrumb,
    BasicInput,
    SelectInput
  },
  props: {
    user: {
      type: Object,
      default: () => {}
    },
    error: {
      type: Object,
      default: () => { }
    },
    errors: {
      type: Object,
      default: () => { }
    },
    availableGroups: {
      type: Object,
      default: () => {}
    },
  },
  setup () {
    return { v$: useVuelidate() }
  },
  data () {
    return {
      pages: pagesDefault,
      isSendingForm: false,
      form: {
        firstName: '',
        lastName: '',
        email: '',
        group: 'customer',
      },
      fieldsErrors: {
        firstName: false,
        lastName: false,
        email: false,
        group: false,
      },
      textErrors: {
        firstName: [],
        lastName: [],
        email: [],
        group: [],
      },
    }
  },
  validations () {
    return {
      form: {
        firstName: { required },
        lastName: { required },
        email: { required, email },
        group: { required },
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
    updateGroup(value){
      this.form.group = value;
    },
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
      this.checkFieldsErrors("firstName");
      this.checkFieldsErrors("lastName");
      this.checkFieldsErrors("email");
      this.checkFieldsErrors("group");
      for (const item in this.fieldsErrors) {
        if (this.fieldsErrors[item]) { valid = false }
      }
      return valid
    },
    onSubmit(event) {
      event.preventDefault();
      let valid = this.fieldsValidate();
      if(!valid) return;
      this.$inertia.post(this.route('management:user_create'), this.form, {
        onStart: () => this.isSendingForm = true,
        onFinish: () => {
          this.isSendingForm = false;
          if(this.errors){
            for (const item in this.fieldsErrors) {
              if (this.errors[item]) {
                this.textErrors[item] = this.errors[item];
                this.fieldsErrors[item] = true
              }
            }
          }
          if(this.error) { this.errorLogin = true}
        }
      })
    },
  }
}
</script>

<template>
  <layout
    title="Register"
  >
    <div class="flex-1 flex flex-col justify-center py-12 px-4 sm:px-6 lg:flex-none lg:px-20 xl:px-24">
      <div
        v-show="errorRegister"
        class="pb-3 mx-auto w-full max-w-sm lg:w-96"
      >
        <message
          v-if="errorRegister"
          time="10"
        >
          {{ $_(error) }}
        </message>
      </div>
      <div class="mx-auto w-full max-w-sm lg:w-96">
        <div>
          <img
            class="h-20 w-auto"
            :src="$page.props.global_settings.appLogo"
            :alt="$page.props.global_settings.appName"
          >
          <h2 class="mt-6 text-2xl font-extrabold text-gray-900">
            {{ $_("Register a new account") }}
          </h2>
        </div>

        <div>
          <div class="mt-4">
            <form
              class="space-y-4"
              @submit="onSubmit"
            >
              <div class="grid grid-cols-2 gap-2">
                <basic-input 
                  name="first-name"
                  :label="$_('First Name')"
                  :value="form.firstName"
                  :error="fieldsErrors.firstName"
                  :text-error="fieldsErrors.firstName ? textErrors.firstName: ['']"
                  @input-return="value => form.firstName = value"
                  @keypress="fieldsErrors.firstName = false"
                  @blur="checkFieldsErrors('firstName')"
                  @change="checkFieldsErrors('firstName')"
                />

                <basic-input
                  name="last-name"
                  :label="$_('Last Name')"
                  :value="form.lastName"
                  :error="fieldsErrors.lastName"
                  :text-error="fieldsErrors.lastName ? textErrors.lastName: ['']"
                  @input-return="value => form.lastName = value"
                  @keypress="fieldsErrors.lastName = false"
                  @blur="checkFieldsErrors('lastName')"
                  @change="checkFieldsErrors('lastName')"
                />
              </div>

              <div>
                <basic-input 
                  name="email"
                  :label="$_('Email')"
                  type="email"
                  :value="form.email"
                  :error="fieldsErrors.email"
                  :text-error="fieldsErrors.email ? textErrors.email: ['']"
                  @input-return="value => form.email = value"
                  @keypress="fieldsErrors.email = false"
                  @blur="checkFieldsErrors('email')"
                  @change="checkFieldsErrors('email')"
                />
              </div>
                            
              <create-password
                :params-validator="paramsPasswordValidator"
                :value="form.password"
                :error="fieldsErrors.password"
                :text-error="fieldsErrors.password ? textErrors.password: ['']"
                @keypress="fieldsErrors.password = false"
                @error-password="error => passwordOk = error"
                @input-return="value => form.password = value"
                @blur="checkFieldsErrors('password')"
              />

              <div>
                <button 
                  type="submit"
                  :disabled="isDisableButtonForm"
                  class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2"
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
                  {{ $_('Register') }}
                </button>
              </div>
            </form>
            <p class="mt-4 text-sm text-gray-600">
              {{ $_('Already have an account?') }} {{ ' ' }}
              <inertia-link
                :href="route('accounts:login')"
                class="font-medium text-app-600 hover:text-app-500"
              >
                {{ $_('Sign in instead') }}
              </inertia-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </layout>
</template>

<script>
import useVuelidate from '@vuelidate/core'
import { required, email } from '@vuelidate/validators'
import Layout from '@components/Layouts/LayoutAuth.vue'
import BasicInput from '@components/Forms/BasicInput.vue'
import CreatePassword from '@components/Forms/CreatePassword.vue'
import Message from '@components/Utils/MessageError.vue'

export default {
  name: 'AuthRegister',
  components: {
    Layout,
    'basic-input': BasicInput,
    'create-password': CreatePassword,
    Message,
  },
  props: {
    paramsPasswordValidator: {
      type: Array,
      default: () => [ 'uppercase', 'lowercase', 'number', 'special', 'minimum' ]
    },
    error: {
      type: Object,
      default: () => {}
    },
    errors: {
      type: Object,
      default: () => {}
    },
  },
  setup () {
    return { v$: useVuelidate() }
  },
  data () {
    return {
      isSendingForm: false,
      errorRegister: false,
      form: {
        firstName: "",
        lastName: "",
        email: "",
        password: "",
        captcha: "",
      },
      fieldsErrors: {
        firstName: false,
        lastName: false,
        email: false,
        password: false,
        captcha: false,
      },
      textErrors: {
        firstName: [],
        lastName: [],
        email: [],
        password: [],
      },
      passwordOk: false
    }
  },
  computed: {
    isValidForm(){
      this.v$.$validate();
      if(this.v$.$error || !this.passwordOk) return false
      return true
    },
    isDisableButtonForm (){
      if(!this.isValidForm || this.isSendingForm){ return true }
      return false
    }
  },
  validations () {
    return {
      form: {
        firstName: { required },
        lastName: { required },
        email: { required, email },
        password: { required },
      },
    }
  },
  methods: {
    setPasswordErrors(){
      this.passwordOk = true;
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
      this.setPasswordErrors();
      this.checkFieldsErrors("firstName");
      this.checkFieldsErrors("lastName");
      this.checkFieldsErrors("email");
      if(!this.passwordOk){ this.fieldsErrors.password = true}
      for (const item in this.fieldsErrors) {
        if (this.fieldsErrors[item]) { valid = false }
      }
      return valid
    },
    onSubmit(event=null) {
      if(event) event.preventDefault();
      let valid = this.fieldsValidate();
      if(!valid) return;
      this.errorRegister = false;
      this.$inertia.post(this.route('accounts:register'), this.form, {
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
          if(this.error) { 
            this.errorRegister = true
          }
        }
      })
    },
  },
}
</script>
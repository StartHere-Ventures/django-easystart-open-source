<template>
  <layout title="Login">
    <div class="flex-1 flex flex-col justify-center py-12 px-4 sm:px-6 lg:flex-none lg:px-20 xl:px-24">
      <div class="mx-auto w-full max-w-sm lg:w-96">
        <div>
          <inertia-link
            :href="route('core:index')"
          >
            <img
              class="h-20 w-auto"
              :src="$page.props.globalSettings.appLogo"
              :alt="$page.props.globalSettings.appName"
            >
          </inertia-link>
          <h2 class="mt-6 text-2xl font-extrabold text-gray-900">
            {{ $_("Set Password") }}
          </h2>
        </div>

        <div class="mt-8">
          <div v-if="tokenInvalid">
            <p
              class="font-medium text-red-600 pb-4 leading-relaxed"
            >
              {{ $_("The password reset token was invalid.") }}
            </p>
            <button 
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 bg-app-600 hover:bg-app-700 focus:ring-app-500"
            >
              <inertia-link
                :href="route('accounts:login')"
              >
                {{ $_("Return to login") }}
              </inertia-link>
            </button>
          </div>
          <form 
            v-if="!tokenInvalid"
            class="space-y-4"
            @submit="onSubmit"
          >
            <create-password
              :params-validator="paramsPasswordPalidator"
              :value="form.password"
              :error="fieldsErrors.password"
              :text-error="fieldsErrors.password ? textErrors.password: ['']"
              @keypress="fieldsErrors.password = false"
              @error-password="error => passwordOk = error"
              @input-return="value => form.password = value"
              @blur="checkFieldsErrors('password')"
            />
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
              {{ $_("Reset Password") }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </layout>
</template>

<script>
import useVuelidate from '@vuelidate/core'
import { required } from '@vuelidate/validators'
import Layout from '../../Components/Layouts/LayoutAuth.vue'
import CreatePassword from '../../Components/Forms/CreatePassword.vue'

export default {
  components: {
    Layout,
    "create-password": CreatePassword
  },
  props: {
    auth: {
      type: Object,
      default: () => {}
    },
    flash: {
      type: Object,
      default: () => {}
    },
    errors: {
      type: Object,
      default: () => {}
    },
    tokenInvalid: {
      type: Boolean,
      default: () => false
    },
    paramsPasswordPalidator: {
      type: Array,
      default: () => [ 'uppercase', 'lowercase', 'number', 'special', 'minimum' ]
    },
    keyToken: {
      type: String,
      default: () => ""
    },
    uidb36: {
      type: String,
      default: () => ""
    }
  },
  setup () {
    return { v$: useVuelidate() }
  },
  data () {
    return {
      isSendingForm: false,
      form: {
        password: ""
      },
      fieldsErrors: {
        password: false
      },
      textErrors: {
        password: []
      },
      passwordOk: false
    }
  },
  validations () {
    return {
      form: {
        password: { required }
      }
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
  methods: {
    setPasswordErrors(){
      this.password = false;
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
      this.checkFieldsErrors("password");
      if(!this.passwordOk){ this.fieldsErrors.password = true}
      for (const item in this.fieldsErrors) {
        if (this.fieldsErrors[item]) { valid = false }
      }
      return valid
    },
    onSubmit(event) {
      event.preventDefault();
      let valid = this.fieldsValidate();
      if(!valid) return;
      this.errorRegister = false;
      this.$inertia.post(this.route('accounts:reset_password_from_key', this.uidb36, this.keyToken), this.form, {
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
        }
      })
    },
  },
}
</script>

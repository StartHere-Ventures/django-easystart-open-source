<template>
  <layout title="Login">
    <div class="flex-1 flex flex-col justify-center py-12 px-4 sm:px-6 lg:flex-none lg:px-20 xl:px-24">
      <div
        v-show="errorLogin"
        class="pb-3 mx-auto w-full max-w-sm lg:w-96"
      >
        <message
          v-if="errorLogin"
          time="10"
        >
          {{ $_(flash.error) }}
        </message>
      </div>
      <div
        v-show="flash.success"
        class="pb-3 mx-auto w-full max-w-sm lg:w-96"
      >
        <message-success
          v-if="flash.success"
          time="10"
        >
          {{ $_(flash.success) }}
        </message-success>
      </div>
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
            {{ $_("Sign in to your account") }}
          </h2>
          <span v-if="$page.props.globalSettings.activeRegistration">
            <p class="mt-2 text-sm text-gray-600">
              {{ $_("Or") }} {{ ' ' }}
              <inertia-link
                :href="route('accounts:register')"
                class="font-medium text-app-600 hover:text-app-500"
              >
                {{ $_("register a new account") }}
              </inertia-link>
            </p>
          </span>
        </div>

        <div class="mt-8">
          <div class="mt-6">
            <form
              class="space-y-4"
              @submit="onSubmit"
            >
              <basic-input
                name="email"
                :label="$_('Email')"
                :value="form.email"
                type="email"
                :text-error="fieldsErrors.email? textErrors.email : ['']"
                :error="fieldsErrors.email"
                @input-return="value => form.email = value"
                @keypress="fieldsErrors.email = false"
                @blur="checkFieldsErrors('email')"
                @change="checkFieldsErrors('email')"
              />

              <div class="space-y-1">
                <password-input
                  name="password"
                  :value="form.password"
                  :error="fieldsErrors.password"
                  :text-error="fieldsErrors.password ? textErrors.password : ['']"
                  @keypress="fieldsErrors.password = false"
                  @input-return="value => form.password = value"
                  @blur="checkFieldsErrors('password')"
                />
              </div>

              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <input
                    id="remember_me"
                    name="remember_me"
                    type="checkbox"
                    class="h-4 w-4 text-app-600 focus:ring-app-500 border-gray-300 rounded"
                  >
                  <label
                    for="remember_me"
                    class="ml-2 block text-sm text-gray-900"
                  >
                    {{ $_("Remember me") }}
                  </label>
                </div>

                <div class="text-sm">
                  <inertia-link
                    :href="route('accounts:reset_password')"
                    class="font-medium text-app-600 hover:text-app-500"
                  >
                    {{ $_("Forgot your password?") }}
                  </inertia-link>
                </div>
              </div>

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
                  {{ $_("Sign in") }}
                </button>
              </div>
            </form>
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
import PasswordInput from '@components/Forms/PasswordInput.vue'
import Message from '@components/Utils/MessageError.vue'
import MessageSuccess from '@components/Utils/MessageSuccess.vue'


export default {
  name: 'AuthLogin',
  components: {
    Layout,
    'basic-input': BasicInput,
    'password-input': PasswordInput,
    Message,
    'message-success': MessageSuccess,
  },
  props: {
    flash: {
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
      errorLogin: false,
      form: {
        email: "",
        password: "",
      },
      fieldsErrors: {
        email: false,
        password: false,
      },
      textErrors: {
        email: [],
        password: [],
      },
    }
  },
  computed: {
    isValidForm(){
      this.v$.$validate()
      if(this.v$.$error) return false
      return true
    },
    isDisableButtonForm (){
      if(!this.isValidForm || this.isSendingForm){ return true }
      return false
    }
  },
  created (){
    if(this.flash.error){
      this.errorLogin = true;
    }
  },
  validations () {
    return {
      form: {
        password: { required },
        email: { required, email },
      },
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
      this.checkFieldsErrors("password");
      this.checkFieldsErrors("email");
      for (const item in this.fieldsErrors) {
        if (this.fieldsErrors[item]) { valid = false }
      }
      return valid;
    },
    onSubmit(event=null) {
      if(event) event.preventDefault();
      let valid = this.fieldsValidate();
      if(!valid) return;
      this.errorLogin = false;
      this.$inertia.post(this.route('accounts:login'), this.form, {
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
          if(this.flash.error) {
            this.errorLogin = true
          }
        }
      })
    },
  }
}
</script>
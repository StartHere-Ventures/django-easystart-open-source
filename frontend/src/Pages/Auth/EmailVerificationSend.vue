<template>
  <layout title="Email Verification">
    <div class="flex-1 flex flex-col justify-center py-12 px-4 sm:px-6 lg:flex-none lg:px-20 xl:px-24">
      <div
        v-show="errorEmailVerification"
        class="pb-3 mx-auto w-full max-w-sm lg:w-96"
      >
        <message
          v-if="errorEmailVerification"
          time="10"
        >
          {{ error }}
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
            {{ $_("Email Verification") }}
          </h2>
        </div>

        <div class="mt-8">
          <p class="font-medium text-gray-600 leading-relaxed">
            {{ $_("Your email has not been verified.") }} 
            <span v-show="auth.emailAddress.emailMethod == 'mandatory'">
              {{ $_("Remember that to access our platform you must perform this step first.") }}
            </span>
          </p>
          <div class="pt-4">
            <form
              class="space-y-4"
              @submit="onSubmit"
            >
              <p class="text-gray-600 leading-normal">
                {{ $_("Enter the email associated with your account to resend the confirmation email.") }}
              </p>
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
                {{ $_("Resend") }}
              </button>
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
import Message from '@components/Utils/MessageError.vue'

export default {
  components: {
    Layout,
    'basic-input': BasicInput,
    Message
  },
  props: {
    auth: {
      type: Object,
      default: () => {}
    },
    error: {
      type: Object,
      default: () => {}
    },
    errors: {
      type: Object,
      default: () => {}
    }
  },
  setup () {
    return { v$: useVuelidate() }
  },
  data () {
    return {
      isSendingForm: false,
      errorEmailVerification: false,
      form: {
        email: "",
      },
      fieldsErrors: {
        email: false,
      },
      textErrors: {
        email: [],
      },
    }
  },
  validations () {
    return {
      form: {
        email: { required, email },
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
      this.checkFieldsErrors("email");
      for (const item in this.fieldsErrors) {
        if (this.fieldsErrors[item]) { valid = false }
      }
      return valid
    },
    onSubmit(event) {
      event.preventDefault();
      let valid = this.fieldsValidate();
      if(!valid) return;
      this.errorEmailVerification = false;
      this.$inertia.post(this.route('accounts:email_verification_sent'), this.form, {
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
          if(this.error) { this.errorEmailVerification = true}
        }
      })
    },
  },
}
</script>
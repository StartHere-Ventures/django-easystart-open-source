<template>
  <div>
    <div>
      <password-input
        :name="name"
        :label="label"
        :value="value"
        :error="error"
        :text-error="textError"
        @keyup="validatePassword"
        @input-return="val => password = val"
        @blur="$emit('blur')"
      />
    </div>
    <div class="col-span-12 sm:col-span-12 px-4 pb-2 pt-2 text-xs">
      <div class="grid grid-cols-2 gap-1">
        <div
          v-if="checkParams('lowercase')"
          class=""
        >
          <ul>
            <li
              class="list-disc"
              :class="errorLowerCase ? 'text-gray-500' : 'text-app-500'"
            >
              {{ $_("One lowercase character") }}
            </li>
          </ul>
        </div>
        <div
          v-if="checkParams('uppercase')"
          class=""
        >
          <ul>
            <li
              class="list-disc"
              :class="errorUpperCase ? 'text-gray-500' : 'text-app-500'"
            >
              {{ $_("One uppercase character") }}
            </li>
          </ul>
        </div>
        <div
          v-if="checkParams('special')"
          class=""
        >
          <ul>
            <li
              class="list-disc"
              :class="errorSpecial ? 'text-gray-500' : 'text-app-500'"
            >
              {{ $_("One special character") }}
            </li>
          </ul>
        </div>
        <div
          v-if="checkParams('number')"
          class=""
        >
          <ul>
            <li
              class="list-disc"
              :class="errorNumber ? 'text-gray-500' : 'text-app-500'"
            >
              {{ $_("One number character") }}
            </li>
          </ul>
        </div>

        <div
          v-if="checkParams('minimum')"
          class=""
        >
          <ul>
            <li
              class="list-disc"
              :class="errorMinimun ? 'text-gray-500' : 'text-app-500'"
            >
              {{ $_("8 characters minimun") }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PasswordInput from './PasswordInput.vue'

const numbers=/[0-9]/;
    const special = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/; // eslint-disable-line

export default {
  components: {
    'password-input': PasswordInput
  },
  props: {
    label: {
      type: String,
      default: () => "Password"
    },
    name: {
      type: String,
      default: () => "password"
    },
    textError: {
      type: Array,
      default: () => ["This field is required"]
    },
    value: {
      type: String,
      default: () => ""
    },
    paramsValidator: {
      type: Array,
      default: () => [ 'uppercase', 'lowercase', 'number', 'special', 'minimum' ]
    },
    error: {
      type: Boolean,
      default: () => false
    }
  },
  emits: [
    'input-return',
    'error-password',
    'blur'
  ],
  data () {
    return {
      password: '',
      passwordOK: true,
      errorUpperCase: true,
      errorLowerCase: true,
      errorSpecial: true,
      errorNumber: true,
      errorMinimun: true
    }
  },
  watch: {
    password(val){
      this.$emit('input-return', val)
      this.validatePassword();
    }
  },
  methods:{
    setPasswordErrors(){
      this.passwordOK = true;
      this.errorUpperCase = true;
      this.errorLowerCase = true;
      this.errorSpecial = true;
      this.errorNumber = true;
      this.errorMinimun = true;
    },
    validatePassword(){
      this.setPasswordErrors();
      if (this.password.length >= 8 || !this.checkParams('minimum')){ this.errorMinimun = false }
      if (numbers.test(this.password) || !this.checkParams('number')){ this.errorNumber = false }
      if (special.test(this.password) || !this.checkParams('special')){ this.errorSpecial = false }
      this.password.split("").map(item => {
        if(!special.test(item) && !numbers.test(item)){
          if(item === item.toUpperCase() || !this.checkParams('uppercase')){ this.errorUpperCase = false }
          if(item === item.toLowerCase() || !this.checkParams('lowercase')){ this.errorLowerCase = false }
        }
      });
      if(
        this.errorMinimun || this.errorNumber || this.errorSpecial ||
                    this.errorUpperCase || this.errorLowerCase
      ) { this.passwordOK = false }
      this.$emit('error-password', this.passwordOK);
    },
    checkParams(param){
      return this.paramsValidator.includes(param)
    }
  }
}
</script>

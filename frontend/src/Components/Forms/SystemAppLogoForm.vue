<template>
  <div>
    <form
      class="space-y-4"
      @submit="onSubmit"
    >
      <div class="sm:grid sm:grid-cols- sm:gap-4">
        <div>
          <file-input 
            ref="logo"
            :ext="allowExt"
            :size="size"
            :error="error"
            :text-error="textError"
            @change="value => updateFile(value)"
          />
          <p class="mt-2 text-xs text-gray-500">
            {{ $_('Recommended dimensions: 320 x 125') }}
          </p>
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
import FileInput from './FileInput.vue'

export default {
  components: {
    'file-input': FileInput
  },
  props: {
    appLogo: {
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
    allowExt: {
      type: Array,
      default:  () => [".png", ".jpg", ".jpeg"]
    },
    size: {
      type: String,
      default: "3"
    },
    url: {
      type: String,
      default: () => '/manage/settings/system/change/app-logo'
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
      logo: null,
      error: false,
      textError: []
    }
  },
  computed: {
    isValidForm(){
      if(!this.logo){ return false }
      this.fileValidate();
      if(this.error){ return false }
      return true
    },
    isDisableButtonForm (){
      if(!this.isValidForm || this.isSendingForm){ return true }
      return false
    }
  },
  methods: {
    validateSize(){
      let size = this.logo.size;
      let sizekiloByte = parseInt(size / 1024);
      if (sizekiloByte >  parseInt(this.size) * 1024) {
        this.error = true;
        this.textError.push("Maximun size is " + this.size + " MB")
      }
    },
    validateExtension(){
      var allow = false;
      var ext = (this.logo.name.substring(this.logo.name.lastIndexOf("."))).toLowerCase();
      for (var i = 0; i < this.allowExt.length; i++) {
        if (this.allowExt[i].toLowerCase() == ext.toLowerCase()) {
          allow = true;
          break;
        }
      } 
      if (!allow){
        this.error = true;
        this.textError.push("Invalid extension")
      }
    },
    fileValidate(){
      this.validateSize();
      this.validateExtension();
    },
    cancelUpdate(event) {
      event.preventDefault();
      this.$emit('close-update-name', true)
    },
    updateFile(value) {
      this.error = false;
      this.textError = [];
      this.logo = value;
    },
    onSubmit(event) {
      event.preventDefault();
      this.fileValidate();
      if(this.error) return;
      this.$inertia.post(this.url, {"logo": this.logo}, {
        onStart: () => this.isSendingForm = true,
        onFinish: () => {
          this.isSendingForm = false;
          this.$emit('show-notification', false)
          if(this.errors){
            if (this.errors["logo"]) {
              this.textError = this.errors["logo"];
              this.error = true
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
  }
}
</script>


<template>
  <div>
    <div v-show="showNotification">
      <notification-success
        v-if="showNotification"
        :primary-text="textNotification"
        @show-notification="value => showNotification = value"
      />
    </div>
    <div class="mt-10 divide-y divide-gray-200">
      <div class="space-y-1">
        <h2 class="text-lg leading-6 font-medium text-gray-900">
          {{ $_("Profile") }}
        </h2>
        <p class="max-w-2xl text-sm text-gray-500">
          {{ $_("This information will be displayed publicly so be careful what you share.") }}
        </p>
      </div>
      <div class="mt-6">
        <div class="divide-y divide-gray-200">
          <slot name="general" />
          <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:pt-5">
            <div class="text-sm font-medium text-gray-500">
              {{ $_("Email") }}
            </div>
            <div class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              <span 
                v-if="!editEmail"
                class="flex-grow"
              >
                {{ auth.user.email }}
                <p
                  v-if="unconfirmedEmail != ''"
                  class="text-xs text-indigo-500"
                >
                  {{ $_("Did not received confirmation email in") }} <span class="font-bold">{{ unconfirmedEmail }}</span>?
                  <br>
                  <span
                    :class="resendCode ? 'text-indigo-500 cursor-pointer underline' : 'text-gray-500'"
                    @click="resendEmail"
                  >
                    {{ $_("Resend email") }} 
                  </span>
                  <span
                    v-if="!resendCode"
                    class="text-gray-500"
                  >
                    (<countdown
                      :init-time="resendEmailTime"
                      @finish-time="value => resendCode = value"
                    />)
                  </span>
                  <span
                    v-if="unconfirmedEmail != auth.user.email"
                    class="ml-2 text-indigo-500 cursor-pointer underline"
                    @click="cancelChangeEmail"
                  >{{ $_("Cancel email change") }}</span>
                </p>
                <p 
                  v-if="errorSendConfirmEmail"
                  class="mt-1 text-xs text-red-600"
                >
                  {{ $_(errorSendConfirmEmail) }}
                </p>
              </span>
              <span 
                v-else
                class="flex-grow"
              >
                <email-form 
                  :user-email="auth.user.email"
                  :tfa="tfa"
                  :flash="flash"
                  :errors="errors"
                  @close-update-name="editEmail = false"
                  @show-notification="value => showNotification = value"
                  @text-notitication="text => textNotification = text"
                />
              </span>
              <span
                v-if="!editEmail"
                class="ml-4 flex-shrink-0 my-auto"
              >
                <button
                  type="button"
                  class="bg-white rounded-md font-medium text-app-600 hover:text-app-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-app-500"
                  @click="editEmail = !editEmail"
                >
                  <span>{{ $_("Change") }}</span>
                </button>
              </span>
            </div>
          </div>
          <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4">
            <div class="text-sm font-medium text-gray-500">
              {{ $_("Name") }}
            </div>
            <div class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              <span
                v-if="!editName"
                class="flex-grow"
              >
                {{ auth.user.firstName }} {{ auth.user.lastName }}
              </span>
              <span
                v-else
                class="flex-grow"
              >
                <names-form 
                  :name="auth.user.firstName"
                  :last="auth.user.lastName"
                  :flash="flash"
                  :errors="errors"
                  @close-update-name="editName = false"
                  @show-notification="value => showNotification = value"
                  @text-notitication="text => textNotification = text"
                />
              </span>
              <span
                v-if="!editName"
                class="ml-4 flex-shrink-0 my-auto"
              >
                <button
                  type="button"
                  class="bg-white rounded-md font-medium text-app-600 hover:text-app-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-app-500"
                  @click="editName = !editName"
                >
                  <span>{{ $_("Update") }}</span>
                </button>
              </span>
            </div>
          </div>
          <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:pt-5">
            <div class="text-sm font-medium text-gray-500">
              {{ $_("Photo") }}
            </div>
            <div class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              <span
                v-if="!editPhoto"
                class="flex-grow"
              >
                <img
                  v-if="!userProfile.photo"
                  class="h-8 w-8 rounded-full"
                  src="/static/img/photo_default.png"
                  alt="Photo"
                >
                <img
                  v-else
                  class="h-8 w-8 rounded-full"
                  :src="userProfile.photo"
                  alt="Photo"
                >
              </span>
              <span
                v-else
                class="flex-grow"
              >
                <photo-form 
                  :user-photo="userProfile.photo"
                  :flash="flash"
                  :errors="errors"
                  :size="maxSizeFile"
                  @close-update-name="editPhoto = false"
                  @show-notification="value => showNotification = value"
                  @text-notitication="text => textNotification = text"
                />
              </span>
              <span
                v-if="!editPhoto"
                class="ml-4 flex-shrink-0 flex items-start space-x-4"
              >
                <button
                  type="button"
                  class="bg-white rounded-md font-medium text-app-600 hover:text-app-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-app-500"
                  @click="editPhoto = true"
                >
                  {{ $_("Update") }}
                </button>
                <span
                  v-if="userProfile.photo"
                  class="text-gray-300"
                  aria-hidden="true"
                >|</span>
                <button
                  v-if="userProfile.photo"
                  type="button"
                  class="bg-white rounded-md font-medium text-app-600 hover:text-app-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-app-500"
                  @click="removePhoto"
                >
                  {{ $_("Remove") }}
                </button>
              </span>
            </div>
          </div>
          <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:border-b sm:border-gray-200">
            <div class="text-sm font-medium text-gray-500">
              {{ $_("Job title") }}
            </div>
            <div class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              <span
                v-if="!editJob"
                class="flex-grow"
              >{{ userProfile.job_title }}</span>
              <span
                v-else
                class="flex-grow"
              >
                <job-form 
                  :job="userProfile.job_title"
                  :flash="flash"
                  :errors="errors"
                  @close-update-name="editJob = false"
                  @show-notification="value => showNotification = value"
                  @text-notitication="text => textNotification = text"
                />
              </span>
              <span
                v-if="!editJob"
                class="ml-4 flex-shrink-0"
              >
                <button
                  type="button"
                  class="bg-white rounded-md font-medium text-app-600 hover:text-app-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-app-500"
                  @click="editJob = !editJob"
                >
                  {{ $_("Update") }}
                </button>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ProfileEmailForm from '@components/Forms/ProfileEmailForm.vue'
import ProfileNameForm from '@components/Forms/ProfileNameForm.vue'
import ProfileJobForm from '@components/Forms/ProfileJobForm.vue'
import ProfilePhotoForm from '@components/Forms/ProfilePhotoForm.vue'
import NotificationSuccess from '@components/Utils/NotificationSuccess.vue'
import Countdown from '@components/Utils/Countdown.vue'

export default {
  name: "GeneralProfile",
  components: {
    'notification-success': NotificationSuccess,
    'names-form': ProfileNameForm,
    'job-form': ProfileJobForm,
    'photo-form': ProfilePhotoForm,
    'email-form': ProfileEmailForm,
    Countdown
  },
  props: {
    auth: {
      type: Object,
      default: () => {}
    },
    tfa: {
      type: Object,
      default: () => {
        return {
          enabled: false,
          userSetup: false
        }
      }
    },
    flash: {
      type: Object,
      default: () => {}
    },
    errors: {
      type: Object,
      default: () => {}
    },
    unconfirmedEmail: {
      type: String,
      default: () => ""
    },
    userProfile: {
      type: Object,
      default: () => { }
    },
    maxSizeFile: {
      type: Number,
      default: 10
    },
    timeResendEmail: {
      type: Number,
      default: () => 0
    },
  },
        
  data () {
    return {
      errorSendConfirmEmail: "",
      showNotification: false,
      textNotification: "",
      editEmail: false,
      editName: false,
      editJob: false,
      editPhoto: false,
      resendCode: false,
      resendEmailTime: this.timeResendEmail
    }
  },
  mounted (){
    if(this.flash.success) {
      var vue = this;
      this.textNotification = this.flash.success;
      this.showNotification = true
      setTimeout(function () { vue.showNotification = false }, 2000)
    }
  },
  methods: {
    removePhoto (){
      if(this.userProfile.photo){
        this.$inertia.get(this.route('core:remove_photo'), {
          onStart: () => this.showNotification = false,
          onFinish: () => {
            if(this.flash.success) {
              var vue = this;
              this.textNotification = this.flash.success;
              this.showNotification = true
              setTimeout(function () { vue.showNotification = false }, 2000)
            }
          }
        })
      }
    },
    resendEmail(){
      if(!this.resendCode) { return }
      this.isSendingConfirmEmail = true;
      axios
        .get('/resend-email-verification')
        .then(response => {
          var vue = this;
          this.errorSendConfirmEmail = "";
          if(response.data.success){
            this.showNotification = true;
            this.textNotification = this.$_("Email send successfully");
            this.resendEmailTime = response.data.timeResendEmail;
            this.resendCode = false;
            setTimeout(function () { vue.showNotification = false }, 2000)
          }
          else if(response.data.error){
            vue.errorSendConfirmEmail = vue.$_(response.data.error);
            setTimeout(function () { vue.errorSendConfirmEmail = "" }, 10000)
          }
        })
    },
    cancelChangeEmail(){
      this.$inertia.post(this.route('core:cancel_change_email'), {"email": this.unconfirmedEmail}, {
        onStart: () => this.showNotification = false,
        onFinish: () => {
          if(this.flash.success) {
            var vue = this;
            this.textNotification = this.flash.success;
            this.showNotification = true
            setTimeout(function () { vue.showNotification = false }, 2000)
          }
        }
      })
    }
  }
}
</script>

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
              <span class="flex-grow">{{ user.email }}</span>
              <span class="ml-4 flex-shrink-0" />
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
                {{ user.firstName }} {{ user.lastName }}
              </span>
              <span
                v-else
                class="flex-grow"
              >
                <names-form 
                  :name="user.firstName"
                  :last="user.lastName"
                  :success="success"
                  :errors="errors"
                  :url="`/manage/user/${user.user_id}/change/names`"
                  @close-update-name="editName = false"
                  @show-notification="value => showNotification = value"
                  @text-notitication="text => textNotification = text"
                />
              </span>
              <span
                v-if="!editName && canEditUser"
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
                  :success="success"
                  :errors="errors"
                  :size="maxSizeFile"
                  :url="`/manage/user/${user.user_id}/change/photo`"
                  @close-update-name="editPhoto = false"
                  @show-notification="value => showNotification = value"
                  @text-notitication="text => textNotification = text"
                />
              </span>
              <span
                v-if="!editPhoto && canEditUser"
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
                  :success="success"
                  :errors="errors"
                  :url="`/manage/user/${user.user_id}/change/job`"
                  @close-update-name="editJob = false"
                  @show-notification="value => showNotification = value"
                  @text-notitication="text => textNotification = text"
                />
              </span>
              <span
                v-if="!editJob && canEditUser"
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
import ProfileNameForm from '@components/Forms/ProfileNameForm.vue'
import ProfileJobForm from '@components/Forms/ProfileJobForm.vue'
import ProfilePhotoForm from '@components/Forms/ProfilePhotoForm.vue'
import NotificationSuccess from '@components/Utils/NotificationSuccess.vue'

export default {
  components: {
    'notification-success': NotificationSuccess,
    'names-form': ProfileNameForm,
    'job-form': ProfileJobForm,
    'photo-form': ProfilePhotoForm
  },
  props: {
    user: {
      type: Object,
      default: () => {}
    },
    success: {
      type: Object,
      default: () => {}
    },
    errors: {
      type: Object,
      default: () => {}
    },
    userProfile: {
      type: Object,
      default: () => { }
    },
    maxSizeFile: {
      type: Number,
      default: 10
    }
  },
        
  data () {
    return {
      showNotification: false,
      textNotification: "",
      editName: false,
      editJob: false,
      editPhoto: false,
    }
  },
  computed: {
    canEditUser() {
      return this.$page.props.auth.user.permissions.includes("core.can_edit_user");
    }
  },
  mounted (){
    if(this.success) {
      var vue = this;
      this.textNotification = this.success;
      this.showNotification = true
      setTimeout(function () { vue.showNotification = false }, 2000)
    }
  },
  methods: {
    removePhoto (){
      if(this.userProfile.photo){
        this.$inertia.get(this.route('management:user_remove_photo', this.user.user_id), {
          onStart: () => this.showNotification = false,
          onFinish: () => {
            if(this.success) {
              var vue = this;
              this.textNotification = this.success;
              this.showNotification = true
              setTimeout(function () { vue.showNotification = false }, 2000)
            }
          }
        })
      }
    }
  }
}
</script>

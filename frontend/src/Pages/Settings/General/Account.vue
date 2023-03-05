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
          {{ $_("Account") }}
        </h2>
        <p class="max-w-2xl text-sm text-gray-500">
          {{ $_("Manage how information is displayed on your account.") }}
        </p>
      </div>
      <div class="mt-6">
        <div class="divide-y divide-gray-200">
          <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4">
            <div class="text-sm font-medium text-gray-500">
              {{ $_("Language") }}
            </div>
            <div class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              <span
                v-if="!editLanguage"
                class="flex-grow"
              >{{ $_(languageName) }}</span>
              <span
                v-else
                class="flex-grow"
              >
                <language-form 
                  :available-languages="availableLanguages"
                  :language="userProfile.language"
                  :flash="flash"
                  :errors="errors"
                  @close-update-name="editLanguage = false"
                  @show-notification="value => showNotification = value"
                  @text-notitication="text => textNotification = text"
                />
              </span>
              <span
                v-if="!editLanguage"
                class="ml-4 flex-shrink-0"
              >
                <button
                  type="button"
                  class="bg-white rounded-md font-medium text-app-600 hover:text-app-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-app-500"
                  @click="editLanguage = true"
                >
                  {{ $_("Update") }}
                </button>
              </span>
            </div>
          </div>
          <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4">
            <div class="text-sm font-medium text-gray-500">
              {{ $_("Country") }}
            </div>
            <div class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              <span
                v-if="!editCountry"
                class="flex-grow"
              >{{ countryName }}</span>
              <span
                v-else
                class="flex-grow"
              >
                <country-form 
                  :available-countries="availableCountries"
                  :country="userProfile.country"
                  :flash="flash"
                  :errors="errors"
                  @close-update-name="editCountry = false"
                  @show-notification="value => showNotification = value"
                  @text-notitication="text => textNotification = text"
                />
              </span>
              <span
                v-if="!editCountry"
                class="ml-4 flex-shrink-0"
              >
                <button
                  type="button"
                  class="bg-white rounded-md font-medium text-app-600 hover:text-app-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-app-500"
                  @click="editCountry = true"
                >
                  {{ $_("Update") }}
                </button>
              </span>
            </div>
          </div>
          <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:pt-5">
            <div class="text-sm font-medium text-gray-500">
              {{ $_("Date format") }}
            </div>
            <div class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              <span
                v-if="!editDateFormat"
                class="flex-grow"
              >{{ userProfile.date_format }}</span>
              <span
                v-else
                class="flex-grow"
              >
                <date-format-form 
                  :available-date-formats="availableDateFormats"
                  :date-format="userProfile.date_format"
                  :flash="flash"
                  :errors="errors"
                  @close-update-name="editDateFormat = false"
                  @show-notification="value => showNotification = value"
                  @text-notitication="text => textNotification = text"
                />
              </span>
              <span
                v-if="!editDateFormat"
                class="ml-4 flex-shrink-0"
              >
                <button
                  type="button"
                  class="bg-white rounded-md font-medium text-app-600 hover:text-app-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-app-500"
                  @click="editDateFormat = true"
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
import NotificationSuccess from '@components/Utils/NotificationSuccess.vue'
import AccountLanguageForm from '@components/Forms/AccountLanguageForm.vue'
import AccountCountryForm from '@components/Forms/AccountCountryForm.vue'
import AccountDateFormatForm from '@components/Forms/AccountDateFormatForm.vue'

export default {
  name: 'GeneralAccount',
  components: {
    'notification-success': NotificationSuccess,
    'language-form':AccountLanguageForm,
    'country-form': AccountCountryForm,
    'date-format-form': AccountDateFormatForm
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
    userProfile: {
      type: Object,
      default: () => { }
    },
    availableLanguages: {
      type: Object,
      default: () => {}
    },
    availableCountries: {
      type: Object,
      default: () => {}
    },
    availableDateFormats: {
      type: Object,
      default: () => {}
    }
  },
        
  data () {
    return {
      showNotification: false,
      textNotification: "",
      editLanguage: false,
      editCountry: false,
      editDateFormat: false,
    }
  },
  computed: {
    languageName (){
      return this.availableLanguages[this.userProfile.language]
    },
    countryName (){
      return this.availableCountries[this.userProfile.country]
    }
  }
}
</script>

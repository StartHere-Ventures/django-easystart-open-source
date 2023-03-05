<!-- This example requires Tailwind CSS v2.0+ -->
<template>
  <TransitionRoot
    as="template"
    :show="open"
  >
    <Dialog
      as="div"
      static
      class="fixed z-10 inset-0 overflow-y-auto"
      :open="open"
      @click="$emit('show-modal', false)"
    >
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <TransitionChild
          as="template"
          enter="ease-out duration-300"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="ease-in duration-200"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <DialogOverlay class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
        </TransitionChild>

        <!-- This element is to trick the browser into centering the modal contents. -->
        <span
          class="hidden sm:inline-block sm:align-middle sm:h-screen"
          aria-hidden="true"
        >&#8203;</span>
        <TransitionChild
          as="template"
          enter="ease-out duration-300"
          enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          enter-to="opacity-100 translate-y-0 sm:scale-100"
          leave="ease-in duration-200"
          leave-from="opacity-100 translate-y-0 sm:scale-100"
          leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
        >
          <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
            <div>
              <div class="mt-3 text-center sm:mt-5">
                <DialogTitle
                  as="h2"
                  class="text-lg leading-6 font-medium text-gray-900"
                >
                  {{ $_(title) }}
                </DialogTitle>
                <div class="mt-2">
                  <p class="text-sm text-gray-500">
                    {{ $_(text) }}
                  </p>
                </div>
              </div>
            </div>
            <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
              <a
                ref="cancelButtonRef"
                type="button"
                href="#"
                class="w-full mr-1 flex inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:mt-0 sm:col-start-1 sm:text-sm"
                @click="$emit('show-modal', false)"
              >
                {{ $_('Cancel') }}
              </a>
              <button
                type="button"
                class="w-full ml-1 flex inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-app-600 text-base font-medium text-white hover:bg-app-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-app-500 sm:col-start-2 sm:text-sm" 
                @click="$emit('confirm-action')"
              >
                {{ $_(buttonTitle) }}
              </button>
            </div>
          </div>
        </TransitionChild>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script>
import { Dialog, DialogOverlay, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue'

export default {
  components: {
    Dialog,
    DialogOverlay,
    DialogTitle,
    TransitionChild,
    TransitionRoot,
  },
  props: {
    open: {
      type: Boolean,
      default: () => false
    },
    title: {
      type: String,
      default: () => "Confirm"
    },
    text: {
      type: String,
      default: () => "Lorem ipsum, dolor sit amet consectetur adipisicing elit."
    },
    buttonTitle: {
      type: String,
      default: () => "Deactivate"
    }
  },
  emits: [
    'show-modal',
    'confirm-action',
  ],
}
</script>
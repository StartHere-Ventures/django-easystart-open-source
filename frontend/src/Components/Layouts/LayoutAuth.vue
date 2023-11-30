<template>
  <div class="min-h-screen bg-white flex">
    <slot />

    <div class="hidden lg:block relative w-0 flex-1">
      <img
        class="absolute inset-0 h-full w-full object-cover"
        src="https://images.unsplash.com/photo-1533090161767-e6ffed986c88?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1650&q=80"
        alt=""
      >
    </div>
  </div>
</template>

<script>
export default {
  created () {
    if(this.$page.props.user_language){
      this.$setlang(this.$page.props.user_language)
    }
  },
}
</script>

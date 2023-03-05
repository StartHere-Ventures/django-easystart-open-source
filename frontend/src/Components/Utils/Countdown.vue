<template>
  <span>{{ time }}</span>
</template>

<script>

export default {
  name: 'CountDown',
  props: {
    initTime: {
      type: Number,
      default: () => 0
    }
  },
  emits: [
    'finish-time'
  ],
  data () {
    return {
      minutes: 0,
      seconds: this.initTime,
      count: null
    }
  },
  computed: {
    time(){
      let remainingSeconds = parseInt(this.seconds % 60);
      if(remainingSeconds < 10){
        remainingSeconds = `0${remainingSeconds}`
      }
      return `${this.minutes}:${remainingSeconds}`;
    }
  },
  created(){
    var vue = this;
    this.secondPassed();
    this.count = setInterval(vue.secondPassed, 1000);
  },
  methods: {
    secondPassed() { 
      this.minutes = Math.round((this.seconds - 30)/60);
      if (this.seconds <= 0) {
        this.$emit('finish-time', true);
        clearInterval(this.count);
      } else {
        this.seconds--;
      }
    } 
  },
}
</script>
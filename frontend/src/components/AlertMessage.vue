<template>
  <div v-if="message" :class="`alert alert-${type}`" role="alert">
    {{ message }}
  </div>
</template>

<script>
export default {
  props: {
    message: String,
    type: {
      type: String,
      default: 'info'
    }
  }
}
</script>

<style scoped>
</style>
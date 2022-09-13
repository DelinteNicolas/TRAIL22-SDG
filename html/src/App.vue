<template>
  <main class="row">
    <FilePreview />
    <StatsComponent />
  </main>
</template>

<script>
import StatsComponent from './components/StatsComponent.vue'
import FilePreview from './components/FilePreview.vue'


export default {
  name: 'App',
  components: {
    StatsComponent,
    FilePreview
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>

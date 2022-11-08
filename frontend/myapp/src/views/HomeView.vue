<template>
  <div class="home">
    <home></home>
  </div>
</template>

<script>
// @ is an alias to /src
import home from "@/components/HomePage.vue";

export default {
  name: "HomeView",
  components: {
    home,
  },
};
</script>

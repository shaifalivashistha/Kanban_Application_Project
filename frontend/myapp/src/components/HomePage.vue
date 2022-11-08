<template>
  <div id="home">
    <p>
      <router-link to="/login"><button>Login</button></router-link>
    </p>
    <p>
      <router-link to="/register"><button>Sign Up</button></router-link>
    </p>
  </div>
</template>

<script>
export default {
  name: "HomePage",
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
h3 {
  margin: 40px 0 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>

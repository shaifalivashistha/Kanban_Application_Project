<template>
  <div id="home">
    <nav>
      <h2><strong><u>KanBan ToDo Application</u></strong></h2>
    </nav>
    <br>
    <div>
      <img src="../assets/kanban1.jpg" alt="KanBanAppImage" />
    </div>
    <br>
    <div>
      <h3>
        <router-link to="/login_page"><button class="btn btn-primary btn-lg btn-block">Login</button></router-link>
      </h3>
      <h3>
        <router-link to="/register"><button class="btn btn-primary btn-lg btn-block">Sign Up</button></router-link>
      </h3>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
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

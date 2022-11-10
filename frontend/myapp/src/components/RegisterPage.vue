<template>
  <div class="register">
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link> |
      <router-link to="/login">Login</router-link> |
      <router-link to="/register">SignUp</router-link>
    </nav>
    <p id="error_txt" class="alert alert-danger" role="alert" v-if="error_txt">
      {{ error_txt }}
    </p>
    <p
      id="success_msg"
      class="alert alert-success"
      role="alert"
      v-if="success_msg"
    >
      {{ success_msg }}
    </p>

    <body class="container">
      <form @submit.prevent="submitForm">
        <h3 class="form text-center mt-2 mb-4">Sign Up</h3>
        <div class="form-group">
          <label>Username</label>
          <input
            id="username"
            type="text"
            v-model="username"
            class="form-control form-control-lg"
            placeholder="Username"
            required
            autocomplete="off"
          />
        </div>
        <div class="form-group">
          <label>Email address</label>
          <input
            id="email"
            type="email"
            v-model="email"
            class="form-control form-control-lg"
            placeholder="email"
            pattern="^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
            required
            autocomplete="off"
          />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input
            id="password"
            type="password"
            v-model="password"
            class="form-control form-control-lg"
            placeholder="Password"
            pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
            required
            autocomplete="off"
          />
        </div>
        <div class="form-group">
          <label>Confirm Password</label>
          <input
            id="password_confirm"
            type="password"
            v-model="password_confirm"
            class="form-control form-control-lg"
            placeholder="Confirm Password"
            required
            autocomplete="off"
          />
        </div>
        <button id="submit" class="btn btn-dark btn-lg btn-block">
          Sign Up
        </button>
      </form>
    </body>
  </div>
</template>
<script>
const baseURL = "http://127.0.0.1:5000";
export default {
  name: "RegisterPage",
  data() {
    return {
      username: "",
      email: "",
      password: "",
      password_confirm: "",
      error_txt: "",
      success_msg: "",
    };
  },
  beforeMount() {
    sessionStorage.clear();
  },
  methods: {
    async submitForm() {
      const user_data = {
        username: this.username,
        email: this.email,
        password: this.password,
        password_confirm: this.password_confirm,
      };
      const requestOptions = {
        method: "POST",
        headers: {
          "Content-Type": "application/json;charset=utf-8",
          "Access-Control-Allow-Origin": "*",
        },
        body: JSON.stringify(user_data),
      };
      try {
        if (this.password == this.password_confirm) {
          await fetch(`${baseURL}/register`, requestOptions)
            .then(async (response) => {
              const myResp = await response.json();
              if (!response.ok) {
                throw Error(response.statusText);
              }
              if (myResp) {
                if (myResp.resp == "ok") {
                  this.success_msg = myResp.msg;
                  this.$router.go();
                  // this.$router.push({ path: "/login_page" });
                } else {
                  throw Error(myResp.msg);
                }
              } else {
                throw Error("something went wrong (data not received)");
              }
            })
            .catch((error) => {
              this.error_txt = error;
              console.log("Registration failed. Error: ", error);
            });
        } else {
          throw Error("Passwords do not match");
        }
      } catch (error) {
        this.error_txt = error;
        console.log("Registration failed. Error: ", error);
      }
    },
  },
};
</script>

<style scoped lang="scss">
h3 {
  text-align: center;
}

.invalid {
  color: red;
}

nav {
  background-color: skyblue;
  padding: 30px;
  text-decoration-color: black;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: red;
    }
  }
}
</style>

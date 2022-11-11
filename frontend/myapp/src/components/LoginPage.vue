<template>
  <div class="login">
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link> |
      <router-link to="/login">Login</router-link> |
      <router-link to="/register">SignUp</router-link>
    </nav>

    <body class="login_body_class">

      <body class="container">
        <br />
        <h3 class="form text-center mt-2 mb-4">Log in</h3>
        <div class="container">
          <p id="error_txt" class="alert alert-danger" role="alert" v-if="error_txt">
            {{ error_txt }}
          </p>
          <p id="success_msg" class="alert alert-success" role="alert" v-if="success_msg">
            {{ success_msg }}
          </p>
        </div>
        <form @submit.prevent="formLogin">
          <div class="form-group">
            <label>Email address</label>
            <input v-model="email" id="email" type="email" class="form-control form-control-lg" />
          </div>
          <div class="form-group">
            <label>Password</label>
            <input v-model="password" id="password" type="password" class="form-control form-control-lg" />
          </div>
          <button id="" class="btn btn-dark btn-lg btn-block">Log in</button>
          <p>New User? <router-link to="/register">Sign Up</router-link>
          </p>
        </form>
      </body>
    </body>
  </div>
</template>

<script>
const baseURL = "http://127.0.0.1:5000";
export default {
  name: "LoginPage",
  data() {
    return {
      email: "",
      password: "",
      username: "",
      error_txt: "",
      success_msg: "",
      auth_token: null,
      is_auth: false,
    };
  },
  beforeMount() {
    sessionStorage.clear();
  },
  methods: {
    async formLogin() {
      const user_data = {
        email: this.email,
        password: this.password,
      };
      const requestOptions = {
        method: "POST",
        headers: {
          "Content-Type": "application/json;charset=utf-8",
          "Access-Control-Allow-Origin": "*",
        },
        body: JSON.stringify(user_data),
      };

      await fetch(`${baseURL}/login?include_auth_token`, requestOptions)
        .then(async (response) => {
          const myResp = await response.json();
          if (!response.ok) {
            throw Error(response.statusText);
          }
          if (myResp) {
            this.auth_token = myResp.response.user.authentication_token;
            sessionStorage.setItem(
              "authentication-token",
              myResp.response.user.authentication_token
            );
            sessionStorage.setItem("email", this.email);
            this.myCallback();
          } else {
            throw Error("could not authenticate (data not received)");
          }
        })
        .catch((error) => {
          this.error_txt = error;
          console.log("Log in failed. Error	: ", error);
        });
    },

    myCallback: async function () {
      const user_data = {
        email: this.email,
        password: this.password,
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
        if (this.auth_token) {
          await fetch(`${baseURL}/login_page`, requestOptions)
            .then(async (response) => {
              const myResp = await response.json();
              if (!response.ok) {
                throw Error(response.statusText);
              }
              if (myResp) {
                if (myResp.resp == "not ok") {
                  throw Error(myResp.err);
                } else if (myResp.resp == "ok") {
                  this.success_msg = myResp.msg;
                  this.username = myResp.stuff;
                  sessionStorage.setItem("username", this.username);
                  this.$router.push({ path: `/dashboard/${this.username}` });
                } else {
                  throw Error(myResp.msg);
                }
              } else {
                throw Error("something went wrong (data not received)");
              }
            })
            .catch((error) => {
              this.error_txt = error;
              console.log("Login failed. Error: ", error);
            });
        } else {
          this.$router.go();
          // this.$router.push({ path: '/login_page' })
          throw Error("authentication failed");
        }
      } catch (error) {
        this.error_txt = error;
        console.log("Log in failed. Error: ", error);
      }
    },
  },
};
</script>
<style lang="scss">
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

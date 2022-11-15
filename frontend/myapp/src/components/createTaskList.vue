<template>
    <div id="task_list">
        <nav style="text-align: left; ">
            <button style=" margin-right:16px; font-size: medium;" class="btn btn-lg"><strong>{{
                    username
            }}</strong></button>
            <button class="btn btn-lg" style="font-size: medium; margin-right:16px"
                @click="goToDashboard()"><strong>Dashboard</strong></button>
            <button class="btn btn-lg" style="font-size: medium; margin-right:16px"
                @click="logout()"><strong>Logout</strong></button>
        </nav>
        <br>
        <div class="container">
            <p id="error_txt" class="alert alert-danger" role="alert" v-if="error_txt">
                {{ error_txt }}
            </p>
            <p id="success_msg" class="alert alert-success" role="alert" v-if="success_msg">
                {{ success_msg }}
            </p>
        </div>
        <br>

        <body class="container">
            <form @submit.prevent="addListSubmit">
                <h3 class="form text-center mt-2 mb-4">Create Your List here</h3>
                <div class="form-group">
                    <h5>List Name:</h5>
                    <!-- <input id="list_name" type="text" class="form-control form-control-lg" placeholder="List Name"
                        required autocomplete="off" /> -->
                    <input id="list_name" type="text" v-model="list_name" ref="list_name"
                        class="form-control form-control-lg" placeholder="List Name" required autocomplete="off" />
                </div>
                <div class="form-group">
                    <h5>Description:</h5>
                    <!-- <input id="list_des" type="text" class="form-control form-control-lg" placeholder="Description"
                        required autocomplete="off" /> -->
                    <input id="list_des" type="text" v-model="list_des" ref="list_des"
                        class="form-control form-control-lg" placeholder="Description" required autocomplete="off" />
                </div>
                <button type="submit" class="btn btn-dark btn-lg btn-block">
                    Save
                </button>
            </form>
        </body>
    </div>
</template>
  
<script>
const baseURL = "http://127.0.0.1:5000"
export default {
    name: "createTaskList",
    data() {
        return {
            username: "",
            auth_token: "",
            list_name: "",
            list_des: "",
            error_txt: "",
            success_msg: "",
        }
    },
    async created() {
        this.auth_token = sessionStorage.getItem("authentication-token");
        this.username = sessionStorage.getItem("username");

    },
    methods: {
        async addListSubmit() {
            const task_list_data = {
                list_name: this.list_name,
                list_des: this.list_des,
            }
            const addListRequestOptions = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json;charset=utf-8",
                    "Authentication-Token": `${this.auth_token}`,
                },
                body: JSON.stringify(task_list_data)
            }
            try {
                if (!!this.auth_token) {

                    await fetch(`${baseURL}/dashboard/${this.username}/create_list`, addListRequestOptions)
                        .then(async response => {
                            if (!response.ok) {
                                throw Error(response.statusText);
                            }
                            const myResp = await response.json();
                            if (!!myResp) {
                                if (myResp.resp == "ok") {
                                    this.success_msg = myResp.msg;
                                    sessionStorage.removeItem("listID")
                                    sessionStorage.removeItem("listName")
                                    this.$router.push({ path: `/dashboard/${this.username}` });
                                }
                                else {
                                    throw Error(myResp.msg);
                                }
                            }
                            else {
                                throw Error("something went wrong (data not received)");
                            }
                        })
                        .catch(error => {
                            this.error_txt = error;
                            console.log("Could not create tist. Error: ", error);
                        })
                }
                else {
                    throw Error("authentication failed");
                }
            }
            catch (error) {
                this.error_txt = error;
                console.log("List Request failed", err)
            }
        },
        async goToDashboard() {
            sessionStorage.removeItem("listID");
            sessionStorage.removeItem("listDescription");
            sessionStorage.removeItem("listName");
            sessionStorage.removeItem("cardID");
            sessionStorage.removeItem("cardTitle");
            sessionStorage.removeItem("cardContent")
            sessionStorage.removeItem("cardDeadline")
            sessionStorage.removeItem("cardStatus")
            sessionStorage.removeItem("checkStatus")
            this.$router.push({ path: `/dashboard/${this.username}` })
        },
        async logout() {
            const logoutRequestOptions = {
                method: "GET",
                headers: {
                    "Content-Type": "application/json;charset=utf-8",
                    "Authentication-Token": `${this.auth_token}`,
                },
            };
            await fetch(`${baseURL}/logout`, logoutRequestOptions)
                .then(async response => {
                    if (!response.ok) {
                        throw Error(response.statusText);
                    }
                    const myResp = await response.json();
                    this.success_msg = myResp.msg;
                })
                .catch(error => {
                    this.error_txt = error;
                    console.log("Could not log out. Error: ", error);
                });
            await fetch(`${baseURL}/logout_page`, logoutRequestOptions)
                .then(async response => {
                    if (!response.ok) {
                        throw Error(response.statusText);
                    }
                    const myResp = await response.json();
                    sessionStorage.clear()
                    this.success_msg = myResp.msg;
                    this.$router.push({ path: `/login_page` })
                })
                .catch(error => {
                    this.error_txt = error;
                    console.log("Could not log out. Error: ", error);
                });
        },
    }
};
</script>
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

.dropbtn {
    background-color: #008a57;
    color: white;
    padding: 10px;
    font-size: 16px;
}

.dropdown {
    position: relative;
    display: inline-block;
}

.dropdown-content {
    display: none;
    position: absolute;
    background-color: #ffffff;
    min-width: 100px;
    box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
    z-index: 1;
}

.dropdown-content a {
    color: black;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
}

.dropdown-content a:hover {
    background-color: rgb(117, 204, 255);
}

.dropdown:hover .dropdown-content {
    display: block;
}

.dropdown:hover .dropbtn {
    background-color: #3e8e41;
}
</style>
  
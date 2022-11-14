<template>
    <div id="cards">
        <nav style="text-align: left; ">
            <button class="btn btn-lg" style=" margin-right:16px; font-size: medium;" @click="pageRefresh()"><strong>{{
                    username
            }}</strong></button>
            <button class="btn btn-lg" style="font-size: medium; margin-right:16px"
                @click="goToDashboard()"><strong>Dashboard</strong></button>
            <button class="btn btn-lg" style="font-size: medium; margin-right:16px"
                @click="logout()"><strong>Logout</strong></button>
        </nav>
        <br>
        <!-- <div class="container">
            <p id="error_txt" class="alert alert-danger" role="alert" v-if="error_txt">
                {{ error_txt }}
            </p>
            <p id="success_msg" class="alert alert-success" role="alert" v-if="success_msg">
                {{ success_msg }}
            </p>
        </div> -->

        <body>
            <form @submit.prevent="updateCardMethod()">

                <h3 class="form text-center mt-2 mb-4">!!---Add Tasks to your Task list here---!!</h3>
                <!-- <div class="dropdown">
                    <button class="dropbtn">Select List</button>
                    <div class="dropdown-content">
                        <a v-for="name in taskList"><button class="btn btn-success btn-lg" @click="changeList(name)">
                                {{ name }}
                            </button>
                        </a>
                    </div>
                </div> -->
                <h5><label for="listName">Select List</label></h5>

                <select
                    style="background-color: lightblue; border-color: darkcyan; text-decoration: solid; text-decoration-color: black; font-size: large;"
                    id="selected_list_name" @click="changeList">
                    <option v-for="index in taskDict">{{ index.listName }}</option>

                </select>
                <h5>Title</h5>
                <input id="title" type="text" v-model="title" ref="title" class="form-control form-control-lg"
                    placeholder="Task title" required autocomplete="off" />

                <!-- <input id="title" type="text" class="form-control form-control-lg" placeholder="Task title" required
                    autocomplete="off" /> -->
                <h5>Content</h5>
                <input id="content" v-model="content" type="text" class="form-control form-control-lg"
                    placeholder="Task content" required autocomplete="off" />
                <h5>Deadline</h5>
                <input id="title" v-model="deadline" type="date" class="form-control form-control-lg"
                    placeholder="dd-mm-yyyy" required autocomplete="off" />
                <h5>Mark as Complete</h5>
                <label class="switch">
                    <input id="status_switch" @change="changeStatus" type="checkbox" v-model="checkStatus">
                    <span class="slider round"></span>
                </label>

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
    name: "updateCardPage",
    data() {
        return {
            cardID: null,
            listID: null,
            username: "",
            auth_token: "",
            taskDict: {},
            listName: "",
            title: "",
            content: "",
            deadline: "",
            status: "",
            checkStatus: "",
            error_txt: "",
            success_msg: "",
        }
    },
    async created() {
        this.auth_token = sessionStorage.getItem("authentication-token");
        this.username = sessionStorage.getItem("username");
        this.listID = sessionStorage.getItem("listID");
        this.listName = sessionStorage.getItem("listName")
        this.cardID = sessionStorage.getItem("cardID")
        this.title = sessionStorage.getItem("cardTitle")
        this.content = sessionStorage.getItem("cardContent")
        this.deadline = sessionStorage.getItem("cardDeadline")
        this.status = sessionStorage.getItem("cardStatus")
        this.checkStatus = sessionStorage.getItem("checkStatus")
        const getRequestOptions = {
            methods: "GET",
            headers: {
                "Content-Type": "application/json;charset=utf-8",
                "Authentication-Token": `${this.auth_token}`
            }
        }
        try {
            if (!!this.auth_token) {
                await fetch(`${baseURL}/${this.username}/create_card`, getRequestOptions)
                    .then(async response => {
                        if (!response.ok) {
                            throw Error(response.statusText);
                        }
                        const myResp = await response.json();
                        if (!!myResp) {
                            if (myResp.resp == "ok") {
                                this.success_msg = myResp.msg;
                                this.taskDict = myResp.stuff.taskDict
                                if (this.checkStatus) {
                                    document.getElementById("status_switch").value = this.checkStatus
                                }
                                else {
                                    document.getElementById("status_switch").value = ""
                                }
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
                        console.log("Could not retrieve tracker data. Error: ", error);
                    })
            }
            else {
                this.logout();
                throw Error("authentication failed.")
            }
        }
        catch (error) {
            this.error_txt = error;
            console.log("Could not retrieve tracker data. Error: ", error);
        }
    },
    methods: {
        async updateCardMethod() {
            const card_task_data = {
                cardID: this.cardID,
                listName: this.listName,
                title: this.title,
                content: this.content,
                deadline: this.deadline,
                status: this.status,
                checkStatus: this.checkStatus
            }
            console.log(this.cardID)
            const updateRequestOptions = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json;charset=utf-8",
                    "Authentication-Token": `${this.auth_token}`,
                },
                body: JSON.stringify(card_task_data)
            }
            try {
                if (!!this.auth_token) {
                    await fetch(`${baseURL}/${this.username}/update_card`, updateRequestOptions)
                        .then(async response => {
                            if (!response.ok) {
                                throw Error(response.statusText);
                            }
                            const myResp = await response.json();
                            if (!!myResp) {
                                if (myResp.resp == "ok") {
                                    this.success_msg = myResp.msg;
                                    sessionStorage.removeItem("listID");
                                    sessionStorage.removeItem("listName");
                                    sessionStorage.removeItem("cardID")
                                    sessionStorage.removeItem("cardTitle")
                                    sessionStorage.removeItem("cardContent")
                                    sessionStorage.removeItem("cardDeadline")
                                    sessionStorage.removeItem("cardStatus")
                                    sessionStorage.removeItem("checkStatus")
                                    this.$router.push({ path: `/dashboard/${this.username}` })
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
                            console.log("Could not update card. Error: ", error);
                        })
                }
                else {
                    this.logout();
                    throw Error("authentication failed.")
                }
            }
            catch (error) {
                this.error_txt = error;
                console.log("Could not update card. Error: ", error);
            }

        },
        async changeList() {
            var x = document.getElementById("selected_list_name").selectedIndex;
            document.getElementsByTagName("option")[x].value = this.taskDict[x].listName;
            this.listName = document.getElementsByTagName("option")[x].value
            // console.log(this.listName)
            sessionStorage.setItem("listName", this.listName)
            this.listID = this.taskDict[x].id
            sessionStorage.setItem("listID", this.listID)
            // console.log(this.listID)


        },
        async changeStatus() {

            var x = document.getElementById("status_switch")
            // console.log(x.value)
            if (x.value == "on") {
                // console.log("THE VALUE IS IN ON IF")
                x.value = "off"
                this.checkStatus = ""
                this.status = "Pending"
                sessionStorage.setItem("checkStatus", this.checkStatus)
                sessionStorage.setItem("cardStatus", this.status)
            }

            else if (x.value == "off") {
                // console.log("THE VALUE IS IN OFF IF ELSE")
                x.value = "on"
                this.checkStatus = "on"
                this.status = "Finished"
                sessionStorage.setItem("cardStatus", this.status)
                sessionStorage.setItem("checkStatus", this.checkStatus)
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
        async pageRefresh() {
            this.$router.push({ path: `/${this.username}/update_card` })
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
.switch {
    position: relative;
    display: inline-block;
    width: 60px;
    height: 34px;
}

.switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    -webkit-transition: .4s;
    transition: .4s;
    border-radius: 34px;
}

.slider:before {
    position: absolute;
    content: "";
    height: 26px;
    width: 26px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    -webkit-transition: .4s;
    transition: .4s;
    border-radius: 50%;
}

input:checked+.slider {
    background-color: #2196F3;
}

input:focus+.slider {
    box-shadow: 0 0 1px #2196F3;
}

input:checked+.slider:before {
    -webkit-transform: translateX(26px);
    -ms-transform: translateX(26px);
    transform: translateX(26px);
}
</style>
  
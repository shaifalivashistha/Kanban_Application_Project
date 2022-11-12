<template>
    <div id="cards">
        <nav>
            <router-link :to="`/dashboard/${username}/create_card`"><button>{{ username }}</button></router-link> |
            <router-link :to="`/dashboard/${username}`"><button>Dashboard</button></router-link> |
            <button @click="logout()">Logout</button>
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

        <body>
            <form @submit.prevent="addCardEntry()">

                <h3 class="form text-center mt-2 mb-4">!!---Add Tasks to your Task list here---!!</h3>
                <div class="dropdown">
                    <button class="dropbtn">Select List</button>
                    <div class="dropdown-content">
                        <a v-for="name in taskList"><button class="btn btn-success btn-lg" @click="changeList(name)">
                                {{ name }}
                            </button>
                        </a>
                    </div>
                </div>
                <h5>Title</h5>
                <input id="title" type="text" v-model="title" ref="title" class="form-control form-control-lg"
                    placeholder="Task title" required autocomplete="off" />

                <!-- <input id="title" type="text" class="form-control form-control-lg" placeholder="Task title" required
                    autocomplete="off" /> -->
                <h5>Content</h5>
                <input id="content" type="text" class="form-control form-control-lg" placeholder="Task content" required
                    autocomplete="off" />
                <h5>Deadline</h5>
                <input id="title" type="date" class="form-control form-control-lg" placeholder="dd-mm-yyyy" required
                    autocomplete="off" />
                <h5>Mark as Complete</h5>
                <label class="switch">
                    <input type="checkbox">
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
    name: "createTaskCard",
    data() {
        return {
            cardID: null,
            listID: null,
            username: "",
            auth_token: "",
            taskList: [],
            listName: "",
            title: "",
            card_data: {},
            deadline: "",
            status: "",
            file: "",
            error_txt: "",
            success_msg: "",
        }
    },
    async created() {
        this.auth_token = sessionStorage.getItem("authentication-token");
        this.username = sessionStorage.getItem("username");
        this.listID = sessionStorage.getItem("listID");
        const getRequestOptions = {
            methods: "GET",
            headers: {
                "Content-Type": "application/json;charset=utf-8",
                "Authentication-Token": `${this.auth_token}`
            }
        }
        try {
            if (!!this.auth_token) {
                console.log(this.listID)
                await fetch(`${baseURL}/${this.username}/${this.listID}/create_card`, getRequestOptions)
                    .then(async response => {
                        if (!response.ok) {
                            throw Error(response.statusText);
                        }
                        const myResp = await response.json();
                        if (!!myResp) {
                            if (myResp.resp == "ok") {
                                this.success_msg = myResp.msg;
                                this.card_data = myResp.stuff.cardData;
                                this.file = myResp.stuff.encodedImage;
                                this.taskList = myResp.stuff.taskList
                                console.log(myResp.stuff.taskList)
                                console.log(this.card_data)
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
                        console.log("Could not retrieve log data. Error: ", error);
                    })
            }
            else {
                this.logout();
                throw Error("authentication failed.")
            }
        }
        catch (error) {
            this.error_txt = error;
            console.log("Could not retrieve log data. Error: ", error);
        }
    },
    methods: {
        async addCardEntry() {
            const temp_data = {
                listID: this.listID,
                listName: this.listName,
                title: this.title,
                content: this.content,
                deadline: this.deadline,
                status: this.status
            }
            const addCardRequestOptions = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json;charset=utf-8",
                    "Authentication-Token": `${this.auth_token}`,
                },
                body: JSON.stringify(temp_data)
            }
            try {
                if (!!this.auth_token) {
                    await fetch(`${baseURL}/${this.username}/${this.listID}/bounce_card_cache`, addCardRequestOptions)
                        .then(async response => {
                            if (!response.ok) {
                                throw Error(response.statusText);
                            }
                            const myResp = await response.json();
                            if (!!myResp) {
                                if (myResp.resp == "ok") {
                                    this.success_msg = myResp.msg;
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
                            console.log("Could not add card to list. Error: ", error);
                        });
                    this.$router.go();
                }
                else {
                    this.logout();
                    throw Error("authentication failed.")
                }
            }
            catch (error) {
                this.error_txt = error;
                console.log("Could not add card to list. Error: ", error);
            }
        },
        async changeList(name) {
            console.log(this.listName)
            this.listName = name
            console.log(this.listName)
        },
        async updateLog(cardID, listName, title, content, deadline, status) {
            sessionStorage.setItem("cardID", cardID)
            sessionStorage.setItem("listName", listName)
            sessionStorage.setItem("title", title)
            sessionStorage.setItem("content", content)
            sessionStorage.setItem("deadline", deadline)
            sessionStorage.setItem("status", status)
        },
        async deleteLog(cardID) {
            const deleteRequestOptions = {
                methods: "GET",
                headers: {
                    "Content-Type": "application/json;charset=utf-8",
                    "Authentication-Token": `${this.auth_token}`,
                }
            }
            try {
                if (!!this.auth_token) {
                    await fetch(`${baseURL}/${this.username}/${this.listID}/${cardID}/delete`, deleteRequestOptions)
                        .then(async response => {
                            if (!response.ok) {
                                throw Error(response.statusText);
                            }
                            const myResp = await response.json();
                            if (!!myResp) {
                                if (myResp.resp == "ok") {
                                    this.success_msg = myResp.msg;
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
                            console.log("Could not delete entry from log. Error: ", error);
                        })
                    this.$router.go();
                }
                else {
                    this.logout();
                    throw Error("authentication failed.")
                }
            }
            catch (error) {
                this.error_txt = error;
                console.log("Could not delete entry from log. Error: ", error);
            }
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
        // async ExportEvents() {
        //     const temp_data = this.card_data
        //     const exportEventsRequestOptions = {
        //         method: "POST",
        //         headers: {
        //             "Content-Type": "application/json;charset=utf-8",
        //             "Authentication-Token": `${this.auth_token}`,
        //         },
        //         body: JSON.stringify(temp_data)
        //     }
        //     try {
        //         // console.log("trying to fetch")
        //         // console.log(post_req_opt.body)
        //         if (!!this.auth_token) {
        //             await fetch(`${baseURL}/${this.username}/${this.trackerID}/export_events`, exportEventsRequestOptions)
        //                 .then(async response => {
        //                     if (!response.ok) {
        //                         throw Error(response.statusText);
        //                     }
        //                     const myResp = await response.json();
        //                     if (!!myResp) {
        //                         if (myResp.resp == "ok") {
        //                             this.success_msg = myResp.msg;
        //                             this.$router.go();
        //                         }
        //                         else {
        //                             throw Error(myResp.msg);
        //                         }
        //                     }
        //                     else {
        //                         throw Error("something went wrong");
        //                     }
        //                 })
        //                 .catch(error => {
        //                     this.error_txt = error;
        //                     console.log("Failed to export. Error: ", error);
        //                 });
        //         }
        //         else {
        //             this.logout();
        //             throw Error("authentication failed");
        //         }
        //     }
        //     catch (error) {
        //         this.error_txt = error;
        //         console.log("Failed to export. Error: ", error)
        //     }
        // },
    }
}
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

table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
}

td {
    text-align: center;
}

th {
    border: 1px solid #dddddd;
    text-align: center;
    padding: 8px;
}

tr:nth-child(even) {
    background-color: #dddddd;
}

.dropbtn {
    background-color: #2fc4ff;
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
  
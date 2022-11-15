<template>
    <div id="dashboard">
        <nav style="text-align: left; ">
            <button style=" margin-right:16px; font-size: medium;" class="btn btn-lg"><strong>{{
                    username
            }}</strong></button>
            <button class="btn btn-lg" style="font-size: medium; margin-right:16px"
                @click="logout()"><strong>Logout</strong></button>
        </nav>
        <br>
        <div>
            <div>
                <button style="margin-right:16px" class="btn btn-primary btn-lg" @click="ExportPageSummary()">Export
                    Summary</button>
                <button style="margin-right:16px" class="btn btn-primary btn-lg" @click="ToSummaryPage">Summary
                    Page</button>

            </div>
            <br>
            <h2><strong>Hello!! {{ username }}</strong></h2>
            <h2>
                <strong>Welcome to the OnTime.</strong>
            </h2>
            <h4>
                welcome to your user dashboard.
                <strong> Keep your work on time</strong> with
                <strong> OnTime!!</strong>
            </h4>
            <br>
            <div class="container">
                <p id="error_txt" class="alert alert-danger" role="alert" v-if="error_txt">
                    {{ error_txt }}
                </p>
                <p id="success_msg" class="alert alert-success" role="alert" v-if="success_msg">
                    {{ success_msg }}
                </p>
            </div>
            <div v-if="Object.keys(this.task_list_data).length < 5">
                <router-link :to="`/dashboard/${username}/create_list`">
                    <button style="
                    border-radius: 50%;
                    font-size: 20px;
                    background-color: #4681f4;
                    margin: 4px 2px;
                    padding: 15px;
                    color: white;
                ">+</button>
                </router-link>
            </div>
        </div>
        <br />
        <div v-if="Object.keys(this.task_list_data).length">
            <h1>
                <strong>||------Task Board------||</strong>
            </h1>

            <div class="card1">
                <div style=" display: flex; flex-direction: row;">
                    <div v-for="task in task_list_data" style="border: solid 1px orange; flex: 0 0 29em; ">
                        <br>
                        <div class="dropdown">
                            <button
                                style="padding: 6px; text-decoration: double; background-color: khaki; font-size: medium; border-color: darkgoldenrod;">{{
                                        task.name
                                }}</button>
                            <div class="dropdown-content">
                                <a>
                                    <router-link :to="`/${username}/update_task_list`"><button
                                            class="btn btn-success btn-lg" style="font-size: medium;"
                                            @click="updateTaskList(task.id, task.name, task.description)">
                                            Update
                                        </button></router-link>
                                </a>
                                <a><button type="button" class="btn btn-danger btn-lg" style="font-size: medium;"
                                        @click="deleteTaskList(task.id)">Delete</button></a>
                            </div>
                        </div>
                        <br>
                        <br>
                        <div v-if="task.task_cards_data">
                            <div class="middle-column">

                                <div v-for="card in task.task_cards_data" id="cards">
                                    <br>
                                    <div class="dropdown">
                                        <button
                                            style="padding: 6px; text-decoration: double; background-color: lightskyblue; font-size: medium;">{{
                                                    card.title
                                            }}</button>
                                        <div class="dropdown-content">
                                            <router-link :to="`/${username}/update_card`">
                                                <a>
                                                    <button class="btn btn-success btn-lg" style="font-size: medium;"
                                                        @click="updateTaskCard(task.id, card.listName, card.id, card.title, card.content, card.deadline, card.status, card.checkStatus)">

                                                        Update

                                                    </button>

                                                </a>
                                            </router-link>
                                            <a><button type="button" class="btn btn-danger btn-lg"
                                                    style="font-size: medium;"
                                                    @click="deleteTaskCard(task.id, card.id)">Delete</button></a>
                                        </div>
                                    </div>
                                    <div>
                                        <h3> <u><strong>task-info:</strong></u> {{ card.content }}</h3>
                                        <br>
                                        <h4 style="text-align:end;"><u><strong>Deadline:</strong></u> {{ card.deadline
                                        }}</h4>
                                        <br>
                                        <h4 style="text-align:end;"><u><strong>Status:</strong></u> {{ card.status
                                        }}</h4>
                                    </div>
                                    <br>
                                </div>
                            </div>
                        </div>

                        <div v-else class="middle-column">
                            <h3><strong>No cards in the list Add using "+"</strong></h3>
                        </div>
                        <br>
                        <router-link :to="`/${username}/create_card`"> <button
                                style="border-radius: 50%; font-size: 20px; background-color: #4681f4; margin: 4px 2px; padding: 10px; color: white;"
                                @click="addCard(task.id, task.name)">+</button>
                        </router-link>
                        <br>
                        <button @click="ExportCard(task.id)">Export List</button>

                    </div>
                </div>
            </div>
        </div>
        <div v-else>
            <h1>!!------Task Board Empty------!!</h1>
            <h2>No Task List in your Board. To Add List tap <strong>'+'</strong>. </h2>
        </div>
    </div>
</template>

<script>
const baseURL = "http://127.0.0.1:5000"
export default {
    name: "DashboardPage",
    data() {
        return {
            username: "",
            auth_token: "",
            task_list_data: {},
            error_txt: "",
            success_msg: "",
            task_card_data: {},
            objLength: 0,
        };
    },
    async created() {
        this.auth_token = sessionStorage.getItem("authentication-token");
        this.username = sessionStorage.getItem("username");

        const requsetOptions = {
            methods: "GET",
            headers: {
                "Content-Type": "application/json;charset=utf-8",
                "Authentication-Token": `${this.auth_token}`,
            }
        };
        try {
            if (!!this.auth_token) {
                fetch(`${baseURL}/dashboard/${this.username}`, requsetOptions)
                    .then(async response => {
                        if (!response.ok) {
                            throw Error(response.statusText);
                        }
                        const myResp = await response.json();
                        if (!!myResp) {
                            this.success_msg = myResp.msg;
                            this.task_list_data = myResp.stuff;

                        }
                        else {
                            throw Error("something went wrong (data not received)");
                        }

                    })
                    .catch(error => {
                        this.error_txt = error;
                        console.log("Could not create dashboard. Error: ", error);
                    });
            }
            else {
                this.logout();
                throw Error("authentication failed");
            }
        }
        catch (error) {
            this.error_txt = error;
            console.log("Error: ", error);
        }
    },

    methods: {
        async deleteTaskList(listID) {
            const deleteRequestOptions = {
                methods: "GET",
                headers: {
                    "Content-Type": "application/json;charset=utf-8",
                    "Authentication-Token": `${this.auth_token}`,
                }
            };
            try {
                if (!!this.auth_token) {
                    await fetch(`${baseURL}/${this.username}/${listID}/delete`, deleteRequestOptions)
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
                            console.log("Could not delete task list. Error: ", error);
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
                console.log("Error: ", error);
            }
        },
        async ToSummaryPage() {
            this.$router.push({ path: `/${this.username}/summary_page` })
        },
        async deleteTaskCard(listID, cardID) {
            const deleteRequestOptions = {
                methods: "GET",
                headers: {
                    "Content-Type": "application/json;charset=utf-8",
                    "Authentication-Token": `${this.auth_token}`,
                }
            };
            try {
                if (!!this.auth_token) {
                    await fetch(`${baseURL}/${this.username}/${listID}/${cardID}/delete`, deleteRequestOptions)
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
                            console.log("Could not delete task list. Error: ", error);
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
                console.log("Error: ", error);
            }
        },
        async updateTaskList(listID, listName, listDescription) {
            sessionStorage.setItem("listID", listID);
            sessionStorage.setItem("listName", listName);
            sessionStorage.setItem("listDescription", listDescription);
        },
        async updateTaskCard(listID, listName, cardID, cardTitle, cardContent, cardDeadline, cardStatus, checkStatus) {
            sessionStorage.setItem("listID", listID);
            sessionStorage.setItem("listName", listName);
            sessionStorage.setItem("cardID", cardID)
            sessionStorage.setItem("cardTitle", cardTitle)
            sessionStorage.setItem("cardContent", cardContent)
            sessionStorage.setItem("cardDeadline", cardDeadline)
            sessionStorage.setItem("cardStatus", cardStatus)
            sessionStorage.setItem("checkStatus", String(checkStatus))
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
        async addCard(listID, listName) {
            sessionStorage.setItem("listID", listID);
            sessionStorage.setItem("listName", listName)
            sessionStorage.setItem("checkStatus", "")
        },
        async ExportPageSummary() {
            const temp_data = this.task_list_data
            const exportListSummaryRequestOptions = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json;charset=utf-8",
                    "Authentication-Token": `${this.auth_token}`,
                },
                body: JSON.stringify(temp_data)
            }
            try {
                if (!!this.auth_token) {
                    await fetch(`${baseURL}/${this.username}/export_summary`, exportListSummaryRequestOptions)
                        .then(async response => {
                            if (!response.ok) {
                                throw Error(response.statusText);
                            }
                            const myResp = await response.json();
                            if (!!myResp) {
                                if (myResp.resp == "ok") {
                                    this.success_msg = myResp.msg;
                                    this.$router.go();
                                }
                                else {
                                    throw Error(myResp.msg);
                                }
                            }
                            else {
                                throw Error("something went wrong");
                            }
                        })
                        .catch(error => {
                            this.error_txt = error;
                            console.log("Failed to export. Error: ", error);
                        });
                }
                else {
                    this.logout();
                    throw Error("authentication failed");
                }
            }
            catch (error) {
                this.error_txt = error;
                console.log("Failed to export. Error: ", error)
            }
        },

        async ExportCard(listID) {
            const temp_data = this.card_data
            const exportEventsRequestOptions = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json;charset=utf-8",
                    "Authentication-Token": `${this.auth_token}`,
                },
                body: JSON.stringify(temp_data)
            }
            try {
                if (!!this.auth_token) {
                    await fetch(`${baseURL}/${this.username}/${listID}/export_card`, exportEventsRequestOptions)
                        .then(async response => {
                            if (!response.ok) {
                                throw Error(response.statusText);
                            }
                            const myResp = await response.json();
                            if (!!myResp) {
                                if (myResp.resp == "ok") {
                                    this.success_msg = myResp.msg;
                                    this.$router.go();
                                }
                                else {
                                    throw Error(myResp.msg);
                                }
                            }
                            else {
                                throw Error("something went wrong");
                            }
                        })
                        .catch(error => {
                            this.error_txt = error;
                            console.log("Failed to export. Error: ", error);
                        });
                }
                else {
                    this.logout();
                    throw Error("authentication failed");
                }
            }
            catch (error) {
                this.error_txt = error;
                console.log("Failed to export. Error: ", error)
            }
        },
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

nav {
    background-color: skyblue;
    padding: 20px;
    text-decoration-color: black;

    a {
        font-weight: bold;
        color: #2c3e50;

        &.router-link-exact-active {
            color: red;
        }
    }
}

.card1 {
    display: flex;
    flex-direction: column;
    text-align: center;
    width: 100%;
    position: relative;
}

.middle-column {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
}

.middle-column div {
    flex-grow: 1;
    margin: 0 8px;
    border: solid 1px black;
}

.middle-column div+div {
    margin-top: 8px
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
    background-color: rgb(126, 225, 255);
}

.dropdown:hover .dropdown-content {
    display: block;
}

.dropdown:hover .dropbtn {
    background-color: #3e8e41;
}
</style>

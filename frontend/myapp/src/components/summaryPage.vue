<template>
    <div id="summary">
        <nav style="text-align: left; ">
            <button class="btn btn-lg" style="font-size: medium; margin-right:16px" @click="goToDashboard()"><strong>{{
                    username
            }}</strong></button>

            <button class="btn btn-lg" style="font-size: medium; margin-right:16px"
                @click="logout()"><strong>Logout</strong></button>
        </nav>
        <br>
        <div>
            <div>
                <button class="btn btn-primary btn-lg" @click="ExportPageSummary()">Export Summary</button>

            </div>
            <br>
            <h2><strong>Hello!! {{ username }}</strong></h2>
            <h2>
                <strong>This is your Task summary of All time.</strong>
            </h2>
            <br>
            <div class="container">
                <p id="error_txt" class="alert alert-danger" role="alert" v-if="error_txt">
                    {{ error_txt }}
                </p>
                <p id="success_msg" class="alert alert-success" role="alert" v-if="success_msg">
                    {{ success_msg }}
                </p>
            </div>
        </div>
        <br />
        <h1>
            <strong>||------Task Board------||</strong>
        </h1>

        <div class="card1">
            <div style=" display: flex; flex-direction: row;">
                <div v-for="task in task_list_data" style="border: solid 1px orange; flex: 0 0 29em; ">
                    <br>
                    <div>
                        <button
                            style="padding: 6px; text-decoration: double; background-color: khaki; font-size: medium; border-color: darkgoldenrod;">{{
                                    task.name
                            }}</button>
                    </div>
                    <br>
                    <br>
                    <div>
                        <div class="middle-column">

                            <div id="cards">
                                <br>

                                <br>
                                <div
                                    style="padding: 6px; text-decoration: double; background-color: lightskyblue; font-size: medium; border-color:blue;">
                                    Task Completed: {{ task.completed }}/{{ Object.keys(task.task_cards_data).length }}
                                </div>
                                <div
                                    style="padding: 6px; text-decoration: double; background-color: lightcoral; font-size: medium; border-color:blue;">
                                    Deadlines Passed: {{ task.passed }}/{{ Object.keys(task.task_cards_data).length }}
                                </div>
                                <br>
                                <div>
                                    <!-- <h4> <u><strong><img img src="../assets/test/2.png" width="200" -->
                                    <!-- height="200"></strong></u></h4> -->
                                    <h4> <u><strong><img width="200"
                                                    :src="'data:image/png;base64,' + task.encoded_img" /></strong></u>
                                    </h4>
                                </div>
                                <br>


                                <br>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>
</template>

<script>
const baseURL = "http://127.0.0.1:5000"
export default {
    name: "summaryPage",
    data() {
        return {
            username: "",
            auth_token: "",
            task_list_data: {},
            error_txt: "",
            success_msg: "",
            file: "",
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
                fetch(`${baseURL}/${this.username}/summary_page`, requsetOptions)
                    .then(async response => {
                        if (!response.ok) {
                            throw Error(response.statusText);
                        }
                        const myResp = await response.json();
                        if (!!myResp) {
                            this.success_msg = myResp.msg;
                            this.task_list_data = myResp.stuff;
                            // this.file = this.task_list_data..encoded_img;
                            console.log(this.task_list_data)
                            // console.log(this.file)

                        }
                        else {
                            throw Error("something went wrong (data not received)");
                        }

                    })
                    .catch(error => {
                        this.error_txt = error;
                        console.log("Could not create Summary Page. Error: ", error);
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
        async goToDashboard() {
            sessionStorage.removeItem("listID");
            sessionStorage.removeItem("listDescription");
            sessionStorage.removeItem("listName");
            sessionStorage.removeItem("cardID");
            sessionStorage.removeItem("cardTitle");
            sessionStorage.removeItem("cardContent")
            sessionStorage.removeItem("cardDeadline")
            sessionStorage.removeItem("cardStatus")
            console.log("here")
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
                    await fetch(`${baseURL}/${this.username}/export_trackers`, exportListSummaryRequestOptions)
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
</style>

<template>
    <div id="dashboard">
        <nav>
            <router-link to="/dashboard">USERNAME</router-link> |
            <router-link to="#">Logout</router-link>
        </nav>
        <br>
        <div>
            <div>
                <!-- <button @click="ExportTrackers()">Export Trackers</button> -->
                <button>Export Summary</button>
            </div>
            <br>
            <h2>Welcome to the OnTime.</h2>
            <!-- <h2>Hello!!</h2> -->
            <h4>
                Hi USERNAME, welcome to your user dashboard.
                <strong> Keep your work done on time</strong> with
                <strong> OnTime!!</strong>
            </h4>
            <br>
            <!-- <div class="container">
                    <p id="error_txt" class="alert alert-danger" role="alert" v-if="error_txt">
                        {{ error_txt }}
                    </p>
                    <p id="success_msg" class="alert alert-success" role="alert" v-if="success_msg">
                        {{ success_msg }}
                    </p>
                </div> -->

            <router-link :to="`/dashboard/create_list`">
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
        <br />
        <div>
            <h1>||------Task Board------||</h1>
            <div style="display: flex; flex-direction: column; text-align: center; width: 100%;">
                <div style=" display: flex; flex-direction: row;">
                    <div style="border: solid 1px orange; flex-grow: 1;">
                        <div class="dropdown">
                            <button class="dropbtn">Dropdown</button>
                            <div class="dropdown-content">
                                <a href="#">Update</a>
                                <a href="#">Delete</a>
                            </div>
                        </div>
                        <br>
                        <div class="middle-column">
                            <div id="box5">
                                Box 5
                            </div>
                            <div id="box6">
                                Box 6
                            </div>
                            <div id="box7">
                                Box 7
                            </div>
                        </div>
                        <p> <button
                                style="border-radius: 50%; font-size: 20px; background-color: #4681f4; margin: 4px 2px; padding: 10px; color: white;">+</button>
                        </p>
                    </div>
                    <div style="border: solid 1px orange; flex-grow: 1;">
                        <div class="dropdown">
                            <button class="dropbtn">List</button>
                            <div class="dropdown-content">
                                <a href="#">Update</a>
                                <a href="#">Delete</a>
                            </div>
                        </div>
                        <br>
                        <div class="middle-column">
                            <div id="box5">
                                Box 5
                            </div>
                            <div id="box6">
                                Box 6
                            </div>
                            <div id="box7">
                                Box 7
                            </div>
                        </div>
                        <p> <button
                                style="border-radius: 50%; font-size: 20px; background-color: #4681f4; margin: 4px 2px; padding: 10px; color: white;">+</button>
                        </p>
                    </div>
                    <div style="border: solid 1px orange; flex-grow: 1;">
                        <div class="dropdown">
                            <button class="dropbtn">List</button>
                            <div class="dropdown-content">
                                <a href="#">Update</a>
                                <a href="#">Delete</a>
                            </div>
                        </div>
                        <br>
                        <div class="middle-column">
                            <div id="box5">
                                Box 5
                            </div>
                            <div id="box6">
                                Box 6
                            </div>
                            <div id="box7">
                                Box 7
                            </div>
                        </div>
                        <p> <button
                                style="border-radius: 50%; font-size: 20px; background-color: #4681f4; margin: 4px 2px; padding: 10px; color: white;">+</button>
                        </p>
                    </div>
                    <div style="border: solid 1px orange; flex-grow: 1;">
                        <div class="dropdown">
                            <button class="dropbtn">List</button>
                            <div class="dropdown-content">
                                <a href="#">Update</a>
                                <a href="#">Delete</a>
                            </div>
                        </div>
                        <br>
                        <div class="middle-column">
                            <div id="box5">
                                Box 5
                            </div>
                            <div id="box6">
                                Box 6
                            </div>
                            <div id="box7">
                                Box 7
                            </div>
                        </div>
                        <p> <button
                                style="border-radius: 50%; font-size: 20px; background-color: #4681f4; margin: 4px 2px; padding: 10px; color: white;">+</button>
                        </p>
                    </div>
                    <div style="border: solid 1px orange; flex-grow: 1;">
                        <div class="dropdown">
                            <button type="dropdown" class="dropbtn">List</button>
                            <div class="dropdown-content">
                                <a href="#">Update</a>
                                <a href="#">Delete</a>
                            </div>
                        </div>
                        <br>
                        <div>
                            <div class="middle-column">
                                <div id="box5">
                                    Box 5
                                </div>
                                <div id="box6">
                                    Box 6
                                </div>
                                <div id="box7">
                                    Box 7
                                </div>
                            </div>
                        </div>
                        <p> <button
                                style="border-radius: 50%; font-size: 20px; background-color: #4681f4; margin: 4px 2px; padding: 10px; color: white;">+</button>
                        </p>

                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
// const baseURL = "http://127.0.0.1:5000"
// export default {
//     name: "DashboardPage",
//     data() {
//         return {
//             username: "",
//             auth_token: "",
//             tracker_data: {},
//             error_txt: "",
//             success_msg: "",
//         };
//     },
//     async created() {
//         this.auth_token = sessionStorage.getItem("authentication-token");
//         this.username = sessionStorage.getItem("username");

//         const requsetOptions = {
//             methods: "GET",
//             headers: {
//                 "Content-Type": "application/json;charset=utf-8",
//                 "Authentication-Token": `${this.auth_token}`,
//             }
//         };
//         try {
//             if (!!this.auth_token) {
//                 fetch(`${baseURL}/dashboard/${this.username}`, requsetOptions)
//                     .then(async response => {
//                         if (!response.ok) {
//                             throw Error(response.statusText);
//                         }
//                         const myResp = await response.json();
//                         if (!!myResp) {
//                             this.success_msg = myResp.msg;
//                             this.tracker_data = myResp.stuff;
//                         }
//                         else {
//                             throw Error("something went wrong (data not received)");
//                         }

//                     })
//                     .catch(error => {
//                         this.error_txt = error;
//                         console.log("Could not create dashboard. Error: ", error);
//                     });
//             }
//             else {
//                 this.logout();
//                 throw Error("authentication failed");
//             }
//         }
//         catch (error) {
//             this.error_txt = error;
//             console.log("Error: ", error);
//         }
//     },

//     methods: {
//         async deleteTracker(trackerID) {
//             const deleteRequestOptions = {
//                 methods: "GET",
//                 headers: {
//                     "Content-Type": "application/json;charset=utf-8",
//                     "Authentication-Token": `${this.auth_token}`,
//                 }
//             };
//             try {
//                 if (!!this.auth_token) {
//                     await fetch(`${baseURL}/${this.username}/${trackerID}/delete`, deleteRequestOptions)
//                         .then(async response => {
//                             if (!response.ok) {
//                                 throw Error(response.statusText);
//                             }
//                             const myResp = await response.json();
//                             if (!!myResp) {
//                                 if (myResp.resp == "ok") {
//                                     this.success_msg = myResp.msg;
//                                 }
//                                 else {
//                                     throw Error(myResp.msg);
//                                 }
//                             }
//                             else {
//                                 throw Error("something went wrong (data not received)");
//                             }

//                         })
//                         .catch(error => {
//                             this.error_txt = error;
//                             console.log("Could not delete tracker. Error: ", error);
//                         });
//                     this.$router.go();
//                 }
//                 else {
//                     this.logout();
//                     throw Error("authentication failed.")
//                 }
//             }
//             catch (error) {
//                 this.error_txt = error;
//                 console.log("Error: ", error);
//             }
//         },
//         async updateTracker(trackerID, trackerName, trackerDescription) {
//             sessionStorage.setItem("trackerID", trackerID);
//             sessionStorage.setItem("trackerName", trackerName);
//             sessionStorage.setItem("trackerDescription", trackerDescription);
//         },
//         async addNumTrackerLogs(trackerID) {
//             sessionStorage.setItem("trackerID", trackerID);
//         },
//         async addBoolTrackerLogs(trackerID) {
//             sessionStorage.setItem("trackerID", trackerID);
//         },
//         async logout() {
//             const logoutRequestOptions = {
//                 method: "GET",
//                 headers: {
//                     "Content-Type": "application/json;charset=utf-8",
//                     "Authentication-Token": `${this.auth_token}`,
//                 },
//             };
//             await fetch(`${baseURL}/logout`, logoutRequestOptions)
//                 .then(async response => {
//                     if (!response.ok) {
//                         throw Error(response.statusText);
//                     }
//                     const myResp = await response.json();
//                     this.success_msg = myResp.msg;
//                 })
//                 .catch(error => {
//                     this.error_txt = error;
//                     console.log("Could not log out. Error: ", error);
//                 });
//             await fetch(`${baseURL}/logout_page`, logoutRequestOptions)
//                 .then(async response => {
//                     if (!response.ok) {
//                         throw Error(response.statusText);
//                     }
//                     const myResp = await response.json();
//                     sessionStorage.clear()
//                     this.success_msg = myResp.msg;
//                     this.$router.push({ path: `/login_page` })
//                 })
//                 .catch(error => {
//                     this.error_txt = error;
//                     console.log("Could not log out. Error: ", error);
//                 });
//         },
//         async ExportTrackers() {
//             const temp_data = this.tracker_data
//             const exportTrackersRequestOptions = {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json;charset=utf-8",
//                     "Authentication-Token": `${this.auth_token}`,
//                 },
//                 body: JSON.stringify(temp_data)
//             }
//             try {
//                 if (!!this.auth_token) {
//                     await fetch(`${baseURL}/${this.username}/export_trackers`, exportTrackersRequestOptions)
//                         .then(async response => {
//                             if (!response.ok) {
//                                 throw Error(response.statusText);
//                             }
//                             const myResp = await response.json();
//                             if (!!myResp) {
//                                 if (myResp.resp == "ok") {
//                                     this.success_msg = myResp.msg;
//                                     this.$router.go();
//                                 }
//                                 else {
//                                     throw Error(myResp.msg);
//                                 }
//                             }
//                             else {
//                                 throw Error("something went wrong");
//                             }
//                         })
//                         .catch(error => {
//                             this.error_txt = error;
//                             console.log("Failed to export. Error: ", error);
//                         });
//                 }
//                 else {
//                     this.logout();
//                     throw Error("authentication failed");
//                 }
//             }
//             catch (error) {
//                 this.error_txt = error;
//                 console.log("Failed to export. Error: ", error)
//             }
//         },
//     }
// }
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

.middle-column {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
}

.middle-column div {
    flex-grow: 1;
    margin: 0 8px;
    border: solid 1px red;
}

.middle-column div+div {
    margin-top: 8px
}

.dropbtn {
    background-color: #008a57;
    color: white;
    padding: 10px;
    font-size: 12px;
}

.dropdown {
    position: relative;
    display: inline-block;
}

.dropdown-content {
    display: none;
    position: absolute;
    background-color: #f1f1f1;
    min-width: 160px;
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
    background-color: #ddd;
}

.dropdown:hover .dropdown-content {
    display: block;
}

.dropdown:hover .dropbtn {
    background-color: #3e8e41;
}
</style>

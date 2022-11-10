<template>
    <div id="Numerical">
        <nav>
            <router-link to="/dashboard/create_card">USERNAME</router-link> |
            <router-link to="/dashboard">Dashboard</router-link> |
            <router-link to="#">Logout</router-link>
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
            <!-- <form @submit.prevent="addLogEntry()"> -->
            <form>
                <h3 class="form text-center mt-2 mb-4">!!---Add Tasks to your Task list here---!!</h3>
                <div class="dropdown">
                    <button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">
                        Select List
                        <span class="caret"></span></button>
                    <ul class="dropdown-menu">
                        <li><a href="#">List 1</a></li>
                        <li><a href="#">List 2</a></li>
                        <li><a href="#">List 3</a></li>
                    </ul>
                </div>
                <h5>Title</h5>
                <!-- <input id="title" type="text" v-model="title" ref="title" class="form-control form-control-lg"
                    placeholder="Task title" required autocomplete="off" /> -->

                <input id="title" type="text" class="form-control form-control-lg" placeholder="Task title" required
                    autocomplete="off" />
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
// const baseURL = "http://127.0.0.1:5000"
// export default {
//     name: "addNumLogPage",
//     data() {
//         return {
//             logID: null,
//             trackerID: null,
//             username: "",
//             auth_token: "",
//             log_value: null,
//             log_note: "",
//             log_data: {},
//             file: "",
//             error_txt: "",
//             success_msg: "",
//         }
//     },
//     async created() {
//         this.auth_token = sessionStorage.getItem("authentication-token");
//         this.username = sessionStorage.getItem("username");
//         this.trackerID = sessionStorage.getItem("trackerID");
//         const getRequestOptions = {
//             methods: "GET",
//             headers: {
//                 "Content-Type": "application/json;charset=utf-8",
//                 "Authentication-Token": `${this.auth_token}`
//             }
//         }
//         try {
//             if (!!this.auth_token) {
//                 await fetch(`${baseURL}/${this.username}/${this.trackerID}/logs`, getRequestOptions)
//                     .then(async response => {
//                         if (!response.ok) {
//                             throw Error(response.statusText);
//                         }
//                         const myResp = await response.json();
//                         if (!!myResp) {
//                             if (myResp.resp == "ok") {
//                                 this.success_msg = myResp.msg;
//                                 this.log_data = myResp.stuff.logData;
//                                 this.file = myResp.stuff.encodedImage;
//                             }
//                             else {
//                                 throw Error(myResp.msg);
//                             }
//                         }
//                         else {
//                             throw Error("something went wrong (data not received)");
//                         }
//                     })
//                     .catch(error => {
//                         this.error_txt = error;
//                         console.log("Could not retrieve log data. Error: ", error);
//                     })
//             }
//             else {
//                 this.logout();
//                 throw Error("authentication failed.")
//             }
//         }
//         catch (error) {
//             this.error_txt = error;
//             console.log("Could not retrieve log data. Error: ", error);
//         }
//     },
//     methods: {
//         async addLogEntry() {
//             const temp_data = {
//                 trackerID: this.trackerID,
//                 log_value: this.log_value,
//                 log_note: this.log_note,
//             }
//             const addLogEntryRequestOptions = {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json;charset=utf-8",
//                     "Authentication-Token": `${this.auth_token}`,
//                 },
//                 body: JSON.stringify(temp_data)
//             }
//             try {
//                 if (!!this.auth_token) {
//                     await fetch(`${baseURL}/${this.username}/${this.trackerID}/bounce_log_cache`, addLogEntryRequestOptions)
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
//                             console.log("Could not add entry to log. Error: ", error);
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
//                 console.log("Could not add entry to log. Error: ", error);
//             }
//         },
//         async updateLog(logID, trackerType, value, note) {
//             sessionStorage.setItem("logID", logID)
//             sessionStorage.setItem("trackerType", trackerType)
//             sessionStorage.setItem("log_value", value)
//             sessionStorage.setItem("log_note", note)
//         },
//         async deleteLog(logID) {
//             const deleteRequestOptions = {
//                 methods: "GET",
//                 headers: {
//                     "Content-Type": "application/json;charset=utf-8",
//                     "Authentication-Token": `${this.auth_token}`,
//                 }
//             }
//             try {
//                 if (!!this.auth_token) {
//                     await fetch(`${baseURL}/${this.username}/${this.trackerID}/${logID}/delete`, deleteRequestOptions)
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
//                             console.log("Could not delete entry from log. Error: ", error);
//                         })
//                     this.$router.go();
//                 }
//                 else {
//                     this.logout();
//                     throw Error("authentication failed.")
//                 }
//             }
//             catch (error) {
//                 this.error_txt = error;
//                 console.log("Could not delete entry from log. Error: ", error);
//             }
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
//         async ExportEvents() {
//             const temp_data = this.log_data
//             const exportEventsRequestOptions = {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json;charset=utf-8",
//                     "Authentication-Token": `${this.auth_token}`,
//                 },
//                 body: JSON.stringify(temp_data)
//             }
//             try {
//                 // console.log("trying to fetch")
//                 // console.log(post_req_opt.body)
//                 if (!!this.auth_token) {
//                     await fetch(`${baseURL}/${this.username}/${this.trackerID}/export_events`, exportEventsRequestOptions)
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
</style>
  
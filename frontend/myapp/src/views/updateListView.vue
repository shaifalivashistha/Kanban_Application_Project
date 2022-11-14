<template>
    <div class="updateTaskList">
        <updateListPage></updateListPage>
    </div>
</template>
  
<script>
// @ is an alias to /src
import updateListPage from "@/components/updateListPage.vue";

export default {
    name: "updateListView",
    components: {
        updateListPage,
    },
};
</script>
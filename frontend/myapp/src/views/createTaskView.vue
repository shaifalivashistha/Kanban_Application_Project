<template>
    <div class="create_list">
        <createTaskList></createTaskList>
    </div>
</template>
  
<script>
// @ is an alias to /src
import createTaskList from "@/components/createTaskList.vue";

export default {
    name: "createTrackerView",
    components: {
        createTaskList,
    },
};
</script>
  
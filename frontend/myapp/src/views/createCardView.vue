<template>
    <div class="taskCardView">
        <createTaskCard></createTaskCard>
    </div>
</template>
  
<script>
// @ is an alias to /src
import createTaskCard from "@/components/createTaskCard.vue";

export default {
    name: "createCardView",
    components: {
        createTaskCard,
    },
};
</script>
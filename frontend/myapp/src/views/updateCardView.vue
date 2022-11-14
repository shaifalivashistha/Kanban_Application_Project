<template>
    <div class="updateCard">
        <updateCardPage></updateCardPage>
    </div>
</template>
  
<script>
// @ is an alias to /src
import updateCardPage from "@/components/updateCardPage.vue";

export default {
    name: "updateCardView",
    components: {
        updateCardPage,
    },
};
</script>
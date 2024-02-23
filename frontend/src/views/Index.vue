<template>
    <div class="index">
        <a-row>
            <a-col :span="6"> </a-col>
            <a-col :span="12">
                <img alt="Vue logo" src="@/assets/vue.svg" />
                <ConfigPanel />
            </a-col>
            <a-col :span="6"> </a-col>
        </a-row>
    </div>
</template>
  
<script lang="ts">
import ConfigPanel from "@/components/ConfigPanel.vue";

export default {
    name: "Home",
    components: {
        ConfigPanel,
    },
};
</script>
  
<style>
.index {
    text-align: center;
}
</style>
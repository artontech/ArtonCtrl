<template>
    <div class="ctrl">
        <iframe :src="`${address}/hls/mystream?token=${token}`"></iframe>
        <!-- <video ref="videoPlayer" class="video-js vjs-default-skin vjs-big-play-centered vjs-16-9"></video> -->
    </div>
</template>

<script lang="ts" setup>
import videojs from 'video.js';
import type Player from 'video.js/dist/types/player';
import { onMounted, onUnmounted, ref } from "vue";
import { useStore } from "vuex";
import "video.js/dist/video-js.css";

const store = useStore();
const { address, token } = store.state.user;
const options = {
    autoplay: true,
    controls: true,
    sources: [
        {
            src: `${address}/hls/mystream/index.m3u8`,
            type: "application/x-mpegURL",
        }
    ],
};
const videoPlayer = ref();
let player: Player;

onMounted(() => {
    (videojs as any).Vhs.xhr.onRequest((options) => {
        if (!options.headers) {
            options.headers = {}
        }
        options.headers["token"] = token
    });
    player = videojs(videoPlayer.value, options, () => {
        console.log('PlayerReady');
    });
});

onUnmounted(() => {
    player.dispose();
});
</script>
  
<style></style>
<template>
    <div class="ctrl">
        <video ref="videoPlayer"></video>
    </div>
</template>

<script lang="ts" setup>
import { onMounted, onUnmounted, ref } from "vue";
import { useStore } from "vuex";
import Hls from 'hls.js';
import { get } from "@/api";

const store = useStore();
const { address, token } = store.state.user;
const videoPlayer = ref();

const retryPause = 2000, url = `${address}/hls/mystream/index.m3u8`;

const loadStream = () => {
    // always prefer hls.js over native HLS.
    // this is because some Android versions support native HLS
    // but don't support fMP4s.
    if (Hls.isSupported()) {
        const hls = new Hls({
            maxLiveSyncPlaybackRate: 1.5,
            xhrSetup: (xhr, _url) => {
                console.log("xhrSetup", _url)
                xhr.setRequestHeader("token", token);
            }
        });

        hls.on(Hls.Events.ERROR, (_evt, data) => {
            if (data.fatal) {
                hls.destroy();

                if (data.details === 'manifestIncompatibleCodecsError') {
                    console.error('stream makes use of codecs which are incompatible with this browser or operative system');
                } else if (data.response && data.response.code === 404) {
                    console.error('stream not found, retrying in some seconds');
                } else {
                    console.error(data.error + ', retrying in some seconds');
                }

                setTimeout(() => loadStream(), retryPause);
            }
        });

        hls.on(Hls.Events.MEDIA_ATTACHED, () => {
            hls.loadSource(url);
        });

        hls.on(Hls.Events.MANIFEST_PARSED, () => {
            videoPlayer.value.play();
        });

        hls.attachMedia(videoPlayer.value);

    } else if (videoPlayer.value.canPlayType('application/vnd.apple.mpegurl')) {
        // since it's not possible to detect timeout errors in iOS,
        // wait for the playlist to be available before starting the stream
        get(url, store)
            .then(() => {
                videoPlayer.value.src = url;
                videoPlayer.value.play();
            });
    }
};

onMounted(() => {
    loadStream();
});

onUnmounted(() => {
});
</script>
  
<style></style>
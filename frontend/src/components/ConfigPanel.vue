<template>
    <a-form :model="formState" name="basic" autocomplete="off" @finish="onFinish" @finishFailed="onFinishFailed">
        <a-form-item label="Address" name="address" :rules="[{ required: true, message: 'Please input your address!' }]">
            <a-input v-model:value="formState.address" />
        </a-form-item>

        <a-form-item label="Username" name="username" :rules="[{ required: true, message: 'Please input your username!' }]">
            <a-input v-model:value="formState.username" />
        </a-form-item>

        <a-form-item label="Password" name="password" :rules="[{ required: true, message: 'Please input your password!' }]">
            <a-input-password v-model:value="formState.password" />
        </a-form-item>

        <a-form-item name="cache" :wrapper-col="{ offset: 4, span: 16 }">
            <a-checkbox v-model:checked="formState.cache">Remember</a-checkbox>
        </a-form-item>

        <a-form-item :wrapper-col="{ offset: 4, span: 16 }">
            <a-button type="primary" html-type="submit">Login</a-button>
        </a-form-item>
    </a-form>
</template>
<script lang="ts" setup>
import { message } from "ant-design-vue";
import { reactive } from 'vue';
import { useRouter } from "vue-router";
import { useStore } from "vuex";

import user from "@/api/user";

interface UserState {
    address: string;
    username: string;
    password: string;
    cache: boolean;
}

const router = useRouter();
const store = useStore();
const formState = reactive<UserState>(store.state.user);
const onFinish = (values: any) => {
    user
        .login(store, values)
        .then((data) => {
            store.commit("user", {
                ...values,
                token: data.token,
            });
            console.log("Success:", values, data);
            router.push("ctrl");
        })
        .catch((err) => {
            switch (err?.data) {
                case "no_user":
                    message.error("No valid user");
                    break;
                default:
                    if (err.message) message.error(err.message);
                    else if (err.name) message.error(err.name);
                    else if (err.code) message.error(err.code);
                    console.log(err);
            }
        });
};

const onFinishFailed = (errorInfo: any) => {
    console.log('Failed:', errorInfo);
};
</script>
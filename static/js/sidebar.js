const app = Vue.createApp({
    data() {
        return {
            registered_users: 0,
            active_users: 0,
        }
    },
    methods: {
        handleLogout() {
            axios.post("/logout")
            .then((res) => {
                location.reload();
            })
        }
    }
});

app.mount("#sidebar")
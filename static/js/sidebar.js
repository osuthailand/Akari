const app = Vue.createApp({
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
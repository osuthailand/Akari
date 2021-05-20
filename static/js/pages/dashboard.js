const dashboard = Vue.createApp({
    delimiters: ["[[", "]]"],
    data() {
        return {
            registered_users: 0,
            active_users: 0,
        }
    },
    mounted() {
        axios.get("https://c.ainu.pw/api/v2/bancho/stats")
        .then((res) => {
            console.log(res.data);
            this.registered_users = res.data.registered_users;
            this.active_users = res.data.online_users;
        })
    }
});

dashboard.mount("#dashboard")
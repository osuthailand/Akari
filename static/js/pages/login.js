const app = Vue.createApp({
    delimiters: ["[[", "]]"],
    data() {
        return {
            username: "",
            password: "",
            error: {
                username: false,
                password: false,
                message: "hiii",
                enabled: false,
            }
        }
    },
    methods: {
        handleSubmit() {
            if(!this.username || !this.password) {
                return;
            }

            let fd = new FormData();
            fd.append("user", this.username);
            fd.append("pwd", this.password);

            this.error.username = false;
            this.error.password = false;

            axios.post("/submit/login", fd, {headers: { "Content-Type": "multipart/form-data" }}).then((res) => {
                switch(res.data) {
                    case "OK":
                        location.replace("/");
                        break;

                    case "NOT FOUND":
                        this.error.username = true;
                        this.error.message = "Username doesn't exist in our database.";
                        break;

                    case "PASSWORD INCORRECT":
                        this.error.password = true;
                        this.error.message = "Password doesn't match... sus.";
                        break;

                    case "NO ACCESS":
                        location.replace("https://ainu.pw");
                        break;
                }
            })
        }
    }
});

app.mount("#root")
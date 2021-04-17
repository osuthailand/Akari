const manual = Vue.createApp({
    delimiters: ["[[", "]]"],
    data() {
        return {
            input: "",
            beatmaps: null,
            loading: false,
        }
    },
    methods: {
        fetchBeatmaps() {
            if (this.loading || !this.input) return;

            this.loading = true;
            axios.get("https://api.chimu.moe/v1/search?query="+this.input).then(res => {
                console.log(res.data.data);
                this.beatmaps = res.data.data;

                this.loading = false;
            }).catch(error => {
                console.log(error);
                this.loading = false;
            })
        },

        get_diff_color(stars, modee) {
            if(stars == 0) return;
            result = "";

            mode = ""
            switch(modee) {
                case 0:
                    mode = "osu";
                    break;
                case 1:
                    mode = "taiko";
                    break;
                case 2:
                    mode = "fruits";
                    break;
                case 3:
                    mode = "mania";
                    break;
            }

            if(stars>=5.25)
                result = "diff-expert";
            else if(stars>=3.75)
                result = "diff-insane";   
            else if(stars>=2.25)
                result = "diff-hard";
            else if(stars>=1.5)
                result = "diff-normal";
            else if(stars>0)
                result = "diff-easy";

            return result+" mode-"+mode;
        }
    }
});

manual.mount("#rank_manual");
// N'utiliser qu'une seul vue par fichier, éviter les Vue multiple
const app_vue = new Vue({
    el: '#app',
    data: {
        co2_rate_all_data : []
    },
    methods: {
        fetch_last_n_elements_to_display() {
            let self = this;
            let get_url = "api/LastElementsData/"
            axios.get(get_url,{}
            ).then(function (response) {
                self.co2_rate_all_data = response.data;
                console.log('SUCCESS!!');
            }).catch(function (response) {
                console.error(JSON.stringify(response.message));
                console.log('FAILURE!!');
            });
        },
    },
    delimiters: ["<%", "%>"]
});
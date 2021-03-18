// N'utiliser qu'une seul vue par fichier, éviter les Vue multiple
const app_vue = new Vue({
    el: '#app',
    data: {
        co2_rate_all_data: [],
        co2_rate_all_data_last_n: [],
        numb_values_to_display: 20,
    },
    methods: {
        fetch_elements() {
            let self = this;
            let get_url = "api/LastElementsData/"
            axios.get(get_url, {}
            ).then(function (response) {
                self.co2_rate_all_data = response.data;
                self.co2_rate_all_data_last_n = self.co2_rate_all_data.slice(-self.numb_values_to_display);
                console.log('SUCCESS!!');
            }).catch(function (response) {
                console.error(JSON.stringify(response.message));
                console.log('FAILURE!!');
            });
        },
    },
    watch: {
        numb_values_to_display: function(val){
            if (val > 0){
                this.co2_rate_all_data_last_n = this.co2_rate_all_data.slice(-val);
            }

        }
    },
    delimiters: ["<%", "%>"]
});
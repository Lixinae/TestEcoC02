// N'utiliser qu'une seul vue par fichier, éviter les Vue multiple
const app_vue = new Vue({
    el: '#app',
    data: {
        data_size: 20,
        real_data: [],
        interpolated_data: [],
        difference_data: [],
    },
    methods: {
        fetch_last_n_elements_to_display() {
            let self = this;
            let get_url = "api/LastElementsData/"
            axios.get(get_url,
                {
                    params:
                        {size: this.data_size}
                }
            ).then(function (response) {
                self.real_data = response.data.real_data;
                self.interpolated_data = response.data.interpolated_data;
                self.difference_data = response.data.difference_data;
                console.log('SUCCESS!!');
            }).catch(function (response) {
                console.error(JSON.stringify(response.message));
                console.log('FAILURE!!');
            });
        },
    },
    delimiters: ["<%", "%>"]
});